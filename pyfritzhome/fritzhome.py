"""The main fritzhome handling class."""

from __future__ import print_function

import hashlib
import json
import logging
import time
from urllib.parse import urlparse
from xml.etree import ElementTree

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from requests import exceptions, Session

from .errors import InvalidError, LoginError, NotLoggedInError
from .fritzhomedevice import FritzhomeDevice
from .devicetypes import FritzhomeTemplate, FritzhomeTrigger
from typing import Dict, Mapping, Optional, Sequence, SupportsInt, Union, overload

_LOGGER: logging.Logger = logging.getLogger(__name__)


class Fritzhome(object):
    """Fritzhome object to communicate with the device."""

    _sid: Optional[str] = None
    _session: Session
    _devices: Optional[Dict[str, FritzhomeDevice]] = None
    _templates: Optional[Dict[str, FritzhomeTemplate]] = None
    _triggers: Optional[Dict[str, FritzhomeTrigger]] = None

    def __init__(
        self,
        host: str,
        user: str,
        password: str,
        port: Optional[int] = None,
        ssl_verify: bool = True,
        timeout: int = 10,
    ) -> None:
        """Create a fritzhome object."""
        self._user: str = user
        self._password: str = password
        self._session = Session()
        self._ssl_verify: bool = ssl_verify
        self._timeout: int = timeout
        self._has_getdeviceinfos: bool = True
        self._has_txbusy: bool = True
        if host.startswith("https://") or host.startswith("http://"):
            self.base_url: str = f"{host}:{port}" if port else host
        else:
            self.base_url = f"http://{host}:{port}" if port else f"http://{host}"

    def _request(
        self,
        url: str,
        params: Optional[Mapping[str, Union[str, int, None]]] = None,
    ) -> str:
        """Send a request with parameters."""
        rsp = self._session.get(
            url, params=params, timeout=self._timeout, verify=self._ssl_verify
        )
        rsp.raise_for_status()
        return rsp.text.strip()

    def _login_request(
        self, username: Optional[str] = None, secret: Optional[str] = None
    ) -> tuple[Optional[str], Optional[str], int]:
        """Send a login request with paramerters."""
        url = f"{self.base_url}/login_sid.lua?version=2"
        params = {}
        if username:
            params["username"] = username
        if secret:
            params["response"] = secret

        plain = self._request(url, params)
        dom = ElementTree.fromstring(plain)
        sid = dom.findtext("SID")
        blocktime = int(dom.findtext("BlockTime") or 0)
        challenge = dom.findtext("Challenge")

        return (sid, challenge, blocktime)

    def has_smarthome_capabilities(self) -> Optional[bool]:
        """Check if the device offers smart home capabilities.

        Tries the TR-064 device description first and, if that could not be
        retrieved or parsed, falls back to the REST API description. Returns
        True if a smart home service/endpoint is present, False if a
        description was retrieved but does not list one, and None if neither
        description could be retrieved or parsed.
        """
        host = urlparse(self.base_url).hostname
        if host and ":" in host:
            # re-add brackets stripped by urlparse for IPv6 literals
            host = f"[{host}]"

        try:
            plain = self._request(f"http://{host}:49000/tr64desc.xml")
            dom = ElementTree.fromstring(plain)
        except (exceptions.RequestException, ElementTree.ParseError) as ex:
            _LOGGER.debug(
                "could not determine smarthome capabilities via TR-064: %s", ex
            )
        else:
            for service_type in dom.iter("{urn:dslforum-org:device-1-0}serviceType"):
                if service_type.text and "X_AVM-DE_Homeauto" in service_type.text:
                    return True
            return False

        try:
            plain = self._request(f"http://{host}/rest_api_desc.json")
            endpoints = json.loads(plain).get("endpoints", [])
            return any(
                "/smarthome" in endpoint.get("path", "") for endpoint in endpoints
            )
        except (
            exceptions.RequestException,
            ValueError,
            AttributeError,
            TypeError,
        ) as ex:
            _LOGGER.debug(
                "could not determine smarthome capabilities via REST API: %s", ex
            )
            return None

    def _logout_request(self) -> None:
        """Send a logout request."""
        _LOGGER.debug("logout")
        url = f"{self.base_url}/login_sid.lua"
        params = {"security:command/logout": "1", "sid": self._sid}

        self._request(url, params)

    @staticmethod
    def _create_login_secrete_pbkdf2(challenge: str, password: str) -> str:
        challenge_parts = challenge.split("$")
        # Extract all necessary values encoded into the challenge
        iter1 = int(challenge_parts[1])
        salt1 = bytes.fromhex(challenge_parts[2])
        iter2 = int(challenge_parts[3])
        salt2 = bytes.fromhex(challenge_parts[4])
        # Hash twice, once with static salt...
        # hash1 = hashlib.pbkdf2_hmac("sha256", password.encode(), salt1, iter1)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(), length=32, salt=salt1, iterations=iter1
        )
        hash1 = kdf.derive(password.encode())
        # Once with dynamic salt.
        # hash2 = hashlib.pbkdf2_hmac("sha256", hash1, salt2, iter2)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(), length=32, salt=salt2, iterations=iter2
        )
        hash2 = kdf.derive(hash1)
        return f"{challenge_parts[4]}${hash2.hex()}"

    @staticmethod
    def _create_login_secret_md5(challenge: str, password: str) -> str:
        """Create a login secret."""
        to_hash = (challenge + "-" + password).encode("UTF-16LE")
        hashed = hashlib.md5(to_hash).hexdigest()
        return "{0}-{1}".format(challenge, hashed)

    @overload
    def _aha_request(
        self,
        cmd: str,
        ain: Optional[str] = None,
        param: Optional[Mapping[str, Union[str, int]]] = None,
        rf: type[str] = str,
    ) -> str: ...

    @overload
    def _aha_request(
        self,
        cmd: str,
        ain: Optional[str] = None,
        param: Optional[Mapping[str, Union[str, int]]] = None,
        rf: type[bool] = bool,
    ) -> bool: ...

    @overload
    def _aha_request(
        self,
        cmd: str,
        ain: Optional[str] = None,
        param: Optional[Mapping[str, Union[str, int]]] = None,
        rf: type[int] = int,
    ) -> int: ...

    @overload
    def _aha_request(
        self,
        cmd: str,
        ain: Optional[str] = None,
        param: Optional[Mapping[str, Union[str, int]]] = None,
        rf: type[float] = float,
    ) -> float: ...

    def _aha_request(
        self,
        cmd: str,
        ain: Optional[str] = None,
        param: Optional[Mapping[str, Union[str, int]]] = None,
        rf: Union[type[str], type[bool], type[int], type[float]] = str,
    ) -> Union[str, bool, int, float]:
        """Send an AHA request."""
        url = f"{self.base_url}/webservices/homeautoswitch.lua"

        _LOGGER.debug("self._sid:%s", self._sid)

        if not self._sid:
            raise NotLoggedInError

        params: Dict[str, Union[str, int]] = {"switchcmd": cmd, "sid": self._sid}
        if param:
            for key, value in param.items():
                params[key] = value
        if ain:
            params["ain"] = ain

        plain = self._request(url, params)
        if plain == "inval":
            raise InvalidError

        if rf == bool:
            return bool(int(plain))
        return rf(plain)

    def login(self) -> None:
        """Login and get a valid session ID."""
        (sid, challenge, blocktime) = self._login_request()
        _LOGGER.info("sid:%s, challenge:%s, blocktime:%s", sid, challenge, blocktime)
        if sid == "0000000000000000":
            if blocktime > 0:
                time.sleep(blocktime)
            if challenge is None:
                raise LoginError(self._user, "challenge missing from login response")
            # PBKDF2 (FRITZ!OS 7.24 or later)
            if challenge.startswith("2$"):
                secret = self._create_login_secrete_pbkdf2(challenge, self._password)
            # fallback to MD5
            else:
                secret = self._create_login_secret_md5(challenge, self._password)
            (sid2, challenge, _) = self._login_request(
                username=self._user, secret=secret
            )
            if sid2 == "0000000000000000":
                _LOGGER.warning("login failed %s", sid2)
                raise LoginError(self._user)
            self._sid = sid2

    def logout(self) -> None:
        """Logout."""
        self._logout_request()
        self._sid = None

    def update_devices(self, ignore_removed: bool = True) -> bool:
        """Update the device."""
        _LOGGER.info("Updating Devices ...")
        if self._devices is None:
            self._devices = {}

        device_elements = self.get_device_elements()
        for element in device_elements:
            if element.attrib["identifier"] in self._devices.keys():
                _LOGGER.info(
                    "Updating already existing Device " + element.attrib["identifier"]
                )
                self._devices[element.attrib["identifier"]]._update_from_node(element)
            else:
                _LOGGER.info("Adding new Device " + element.attrib["identifier"])
                device = FritzhomeDevice(self, node=element)
                self._devices[device.ain] = device

        if not ignore_removed:
            for identifier in list(self._devices.keys()):
                if identifier not in [
                    element.attrib["identifier"] for element in device_elements
                ]:
                    _LOGGER.info("Removing no more existing device " + identifier)
                    self._devices.pop(identifier)

        return True

    def _get_listinfo_elements(self, entity_type: str) -> list[ElementTree.Element]:
        """Get the DOM elements for the entity list."""
        plain = self._aha_request("get" + entity_type + "listinfos")
        dom = ElementTree.fromstring(plain)
        _LOGGER.debug(dom)
        return dom.findall("*")

    def wait_device_txbusy(self, ain: str, retries: int = 10) -> bool:
        """Wait for device to finish command execution."""
        if not self._has_txbusy:
            return True

        for _ in range(retries):
            if self._has_getdeviceinfos:
                try:
                    # getdeviceinfos was added in FritzOS 7.24
                    plain = self.get_device_infos(ain)
                    dom = ElementTree.fromstring(plain)
                except exceptions.HTTPError:
                    _LOGGER.debug("fallback to getdevicelistinfos")
                    self._has_getdeviceinfos = False

            if not self._has_getdeviceinfos:
                fallback_dom = self.get_device_element(ain)
                if fallback_dom is None:
                    return False
                dom = fallback_dom

            txbusy = dom.findall("txbusy")
            if not txbusy:
                # txbusy was added in FritzOS 7.20
                self._has_txbusy = False
                return True

            if txbusy[0].text == "0":
                return True

            time.sleep(0.2)
        return False

    def get_device_elements(self) -> list[ElementTree.Element]:
        """Get the DOM elements for the device list."""
        return self._get_listinfo_elements("device")

    def get_device_element(self, ain: str) -> Optional[ElementTree.Element]:
        """Get the DOM element for the specified device."""
        elements = self.get_device_elements()
        for element in elements:
            if element.attrib["identifier"] == ain:
                return element
        return None

    def get_devices(self) -> list[FritzhomeDevice]:
        """Get the list of all known devices."""
        return list(self.get_devices_as_dict().values())

    def get_devices_as_dict(self) -> Dict[str, FritzhomeDevice]:
        """Get the list of all known devices."""
        if self._devices is None:
            self.update_devices()
            assert self._devices is not None
        return self._devices

    def get_device_by_ain(self, ain: str) -> FritzhomeDevice:
        """Return a device specified by the AIN."""
        return self.get_devices_as_dict()[ain]

    def get_device_infos(self, ain: str) -> str:
        """Get the device infos."""
        return self._aha_request("getdeviceinfos", ain=ain)

    def get_device_present(self, ain: str) -> bool:
        """Get the device presence."""
        return self._aha_request("getswitchpresent", ain=ain, rf=bool)

    def get_device_name(self, ain: str) -> str:
        """Get the device name."""
        return self._aha_request("getswitchname", ain=ain)

    def get_switch_state(self, ain: str) -> bool:
        """Get the switch state."""
        return self._aha_request("getswitchstate", ain=ain, rf=bool)

    def set_switch_state_on(self, ain: str, wait: bool = False) -> bool:
        """Set the switch to on state."""
        result = self._aha_request("setswitchon", ain=ain, rf=bool)
        wait and self.wait_device_txbusy(ain)
        return result

    def set_switch_state_off(self, ain: str, wait: bool = False) -> bool:
        """Set the switch to off state."""
        result = self._aha_request("setswitchoff", ain=ain, rf=bool)
        wait and self.wait_device_txbusy(ain)
        return result

    def set_switch_state_toggle(self, ain: str, wait: bool = False) -> bool:
        """Toggle the switch state."""
        result = self._aha_request("setswitchtoggle", ain=ain, rf=bool)
        wait and self.wait_device_txbusy(ain)
        return result

    def get_switch_power(self, ain: str) -> int:
        """Get the switch power consumption."""
        return self._aha_request("getswitchpower", ain=ain, rf=int)

    def get_switch_energy(self, ain: str) -> int:
        """Get the switch energy."""
        return self._aha_request("getswitchenergy", ain=ain, rf=int)

    def get_temperature(self, ain: str) -> float:
        """Get the device temperature sensor value."""
        return self._aha_request("gettemperature", ain=ain, rf=float) / 10.0

    def _get_temperature(self, ain: str, name: str) -> float:
        plain = self._aha_request(name, ain=ain, rf=float)
        return plain / 2

    def get_target_temperature(self, ain: str) -> float:
        """Get the thermostate target temperature."""
        return self._get_temperature(ain, "gethkrtsoll")

    def set_target_temperature(
        self, ain: str, temperature: float, wait: bool = False
    ) -> None:
        """Set the thermostate target temperature."""
        temp = int(temperature * 2)

        if temp < 16:
            temp = 253
        elif temp > 56:
            temp = 254

        self._aha_request("sethkrtsoll", ain=ain, param={"param": temp})
        wait and self.wait_device_txbusy(ain)

    def set_window_open(self, ain: str, seconds: float, wait: bool = False) -> None:
        """Set the thermostate target temperature."""
        endtimestamp = int(time.time() + seconds)

        self._aha_request(
            "sethkrwindowopen", ain=ain, param={"endtimestamp": endtimestamp}
        )
        wait and self.wait_device_txbusy(ain)

    def set_boost_mode(self, ain: str, seconds: float, wait: bool = False) -> None:
        """Set the thermostate to boost mode."""
        endtimestamp = int(time.time() + seconds)

        self._aha_request("sethkrboost", ain=ain, param={"endtimestamp": endtimestamp})
        wait and self.wait_device_txbusy(ain)

    def get_comfort_temperature(self, ain: str) -> float:
        """Get the thermostate comfort temperature."""
        return self._get_temperature(ain, "gethkrkomfort")

    def get_eco_temperature(self, ain: str) -> float:
        """Get the thermostate eco temperature."""
        return self._get_temperature(ain, "gethkrabsenk")

    def get_device_statistics(self, ain: str) -> str:
        """Get device statistics."""
        plain = self._aha_request("getbasicdevicestats", ain=ain)
        return plain

    # Lightbulb-related commands

    def set_state_off(self, ain: str, wait: bool = False) -> None:
        """Set the switch/actuator/lightbulb to on state."""
        self._aha_request("setsimpleonoff", ain=ain, param={"onoff": 0})
        wait and self.wait_device_txbusy(ain)

    def set_state_on(self, ain: str, wait: bool = False) -> None:
        """Set the switch/actuator/lightbulb to on state."""
        self._aha_request("setsimpleonoff", ain=ain, param={"onoff": 1})
        wait and self.wait_device_txbusy(ain)

    def set_state_toggle(self, ain: str, wait: bool = False) -> None:
        """Toggle the switch/actuator/lightbulb state."""
        self._aha_request("setsimpleonoff", ain=ain, param={"onoff": 2})
        wait and self.wait_device_txbusy(ain)

    def set_level(self, ain: str, level: float, wait: bool = False) -> None:
        """Set level/brightness/height in interval [0,255]."""
        if level < 0:
            level = 0  # 0%
        elif level > 255:
            level = 255  # 100 %

        self._aha_request("setlevel", ain=ain, param={"level": int(level)})
        wait and self.wait_device_txbusy(ain)

    def set_level_percentage(self, ain: str, level: float, wait: bool = False) -> None:
        """Set level/brightness/height in interval [0,100]."""
        if level < 0:
            level = 0
        elif level > 100:
            level = 100

        self._aha_request("setlevelpercentage", ain=ain, param={"level": int(level)})
        wait and self.wait_device_txbusy(ain)

    def _get_colordefaults(self, ain: str) -> ElementTree.Element:
        plain = self._aha_request("getcolordefaults", ain=ain)
        return ElementTree.fromstring(plain)

    def get_colors(
        self, ain: str
    ) -> dict[str, list[tuple[Optional[str], Optional[str], Optional[str]]]]:
        """Get colors (HSV-space) supported by this lightbulb."""
        colordefaults = self._get_colordefaults(ain)
        colors = {}
        for hs in colordefaults.iter("hs"):
            name_element = hs.find("name")
            if name_element is None or name_element.text is None:
                continue
            name = name_element.text.strip()
            values = []
            for st in hs.iter("color"):
                values.append((st.get("hue"), st.get("sat"), st.get("val")))
            colors[name] = values
        return colors

    def set_color(
        self,
        ain: str,
        hsv: Sequence[Union[str, SupportsInt]],
        duration: int = 0,
        mapped: bool = True,
        wait: bool = False,
    ) -> None:
        """Set hue and saturation.

        hsv: HUE colorspace element obtained from get_colors()
        duration: Speed of change in seconds, 0 = instant
        """
        params = {
            "hue": int(hsv[0]),
            "saturation": int(hsv[1]),
            "duration": int(duration) * 10,
        }
        if mapped:
            self._aha_request("setcolor", ain=ain, param=params)
        else:
            # available since Fritz!OS 7.39
            self._aha_request("setunmappedcolor", ain=ain, param=params)
        wait and self.wait_device_txbusy(ain)

    def get_color_temps(self, ain: str) -> list[Optional[str]]:
        """Get temperatures supported by this lightbulb."""
        colordefaults = self._get_colordefaults(ain)
        temperatures = []
        for temp in colordefaults.iter("temp"):
            temperatures.append(temp.get("value"))
        return temperatures

    def set_color_temp(
        self,
        ain: str,
        temperature: Union[str, int, float],
        duration: int = 0,
        wait: bool = False,
    ) -> None:
        """Set color temperature.

        temperature: temperature element obtained from get_temperatures()
        duration: Speed of change in seconds, 0 = instant
        """
        params = {"temperature": int(temperature), "duration": int(duration) * 10}
        self._aha_request("setcolortemperature", ain=ain, param=params)
        wait and self.wait_device_txbusy(ain)

    # blinds
    # states: open, close, stop
    def _set_blind_state(self, ain: str, state: str) -> None:
        self._aha_request("setblind", ain=ain, param={"target": state})

    def set_blind_open(self, ain: str, wait: bool = False) -> None:
        """Set the blind state to open."""
        self._set_blind_state(ain, "open")
        wait and self.wait_device_txbusy(ain)

    def set_blind_close(self, ain: str, wait: bool = False) -> None:
        """Set the blind state to close."""
        self._set_blind_state(ain, "close")
        wait and self.wait_device_txbusy(ain)

    def set_blind_stop(self, ain: str, wait: bool = False) -> None:
        """Set the blind state to stop."""
        self._set_blind_state(ain, "stop")
        wait and self.wait_device_txbusy(ain)

    # Template-related commands

    def has_templates(self) -> bool:
        """Check if the Fritz!Box supports smarthome templates."""
        plain = self._aha_request("gettemplatelistinfos")
        try:
            ElementTree.fromstring(plain)
        except ElementTree.ParseError:
            return False
        return True

    def update_templates(self, ignore_removed: bool = True) -> bool:
        """Update the template."""
        _LOGGER.info("Updating Templates ...")
        if self._templates is None:
            self._templates = {}

        template_elements = self.get_template_elements()
        for element in template_elements:
            if element.attrib["identifier"] in self._templates.keys():
                _LOGGER.info(
                    "Updating already existing Template " + element.attrib["identifier"]
                )
                self._templates[element.attrib["identifier"]]._update_from_node(element)
            else:
                _LOGGER.info("Adding new Template " + element.attrib["identifier"])
                template = FritzhomeTemplate(self, node=element)
                self._templates[template.ain] = template

        if not ignore_removed:
            for identifier in list(self._templates.keys()):
                if identifier not in [
                    element.attrib["identifier"] for element in template_elements
                ]:
                    _LOGGER.info("Removing no more existing template " + identifier)
                    self._templates.pop(identifier)

        return True

    def get_template_elements(self) -> list[ElementTree.Element]:
        """Get the DOM elements for the template list."""
        return self._get_listinfo_elements("template")

    def get_templates(self) -> list[FritzhomeTemplate]:
        """Get the list of all known templates."""
        return list(self.get_templates_as_dict().values())

    def get_templates_as_dict(self) -> Dict[str, FritzhomeTemplate]:
        """Get the list of all known templates."""
        if self._templates is None:
            self.update_templates()
            assert self._templates is not None
        return self._templates

    def get_template_by_ain(self, ain: str) -> FritzhomeTemplate:
        """Return a template specified by the AIN."""
        return self.get_templates_as_dict()[ain]

    def apply_template(self, ain: str) -> None:
        """Appliy a template."""
        self._aha_request("applytemplate", ain=ain)

    # Trigger-related commands

    def has_triggers(self) -> bool:
        """Check if the Fritz!Box supports smarthome triggers."""
        plain = self._aha_request("gettriggerlistinfos")
        try:
            ElementTree.fromstring(plain)
        except ElementTree.ParseError:
            return False
        return True

    def update_triggers(self, ignore_removed: bool = True) -> bool:
        """Update the triger."""
        _LOGGER.info("Updating Trigers ...")
        if self._triggers is None:
            self._triggers = {}

        trigger_elements = self.get_trigger_elements()
        for element in trigger_elements:
            if element.attrib["identifier"] in self._triggers.keys():
                _LOGGER.info(
                    "Updating already existing Trigger " + element.attrib["identifier"]
                )
                self._triggers[element.attrib["identifier"]]._update_from_node(element)
            else:
                _LOGGER.info("Adding new Trigger " + element.attrib["identifier"])
                trigger = FritzhomeTrigger(self, node=element)
                self._triggers[trigger.ain] = trigger

        if not ignore_removed:
            for identifier in list(self._triggers.keys()):
                if identifier not in [
                    element.attrib["identifier"] for element in trigger_elements
                ]:
                    _LOGGER.info("Removing no more existing trigger " + identifier)
                    self._triggers.pop(identifier)

        return True

    def get_trigger_elements(self) -> list[ElementTree.Element]:
        """Get the DOM elements for the trigger list."""
        return self._get_listinfo_elements("trigger")

    def get_triggers(self) -> list[FritzhomeTrigger]:
        """Get the list of all known triggers."""
        return list(self.get_triggers_as_dict().values())

    def get_triggers_as_dict(self) -> Dict[str, FritzhomeTrigger]:
        """Get all known triggers as dictionary."""
        if self._triggers is None:
            self.update_triggers()
            assert self._triggers is not None
        return self._triggers

    def get_trigger_by_ain(self, ain: str) -> FritzhomeTrigger:
        """Return a trigger specified by the AIN."""
        return self.get_triggers_as_dict()[ain]

    def _set_trigger_state(self, ain: str, state: str) -> None:
        self._aha_request("settriggeractive", ain=ain, param={"active": state})

    def set_trigger_active(self, ain: str) -> None:
        """Set the trigger to active state."""
        self._set_trigger_state(ain, "1")

    def set_trigger_inactive(self, ain: str) -> None:
        """Set the trigger to inactive state."""
        self._set_trigger_state(ain, "0")
