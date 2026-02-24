"""The main fritzhome handling class."""
# -*- coding: utf-8 -*-

from __future__ import print_function

import hashlib
import logging
import time
import json
from xml.etree import ElementTree

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from requests import exceptions, Session

from .errors import InvalidError, LoginError, NotLoggedInError
from .fritzhomedevice import FritzhomeDevice
from .fritzhomedevice import FritzhomeUnit
from .fritzhomedevice import FritzhomeTemplate
from .fritzhomedevice import FritzhomeTrigger
from typing import Dict, Optional

_LOGGER = logging.getLogger(__name__)


class Fritzhome(object):
    """Fritzhome object to communicate with the device."""

    _sid = None
    _session = None
    _units: Dict[str, FritzhomeUnit]
    _devices: Dict[str, FritzhomeDevice]
    _templates: Optional[Dict[str, FritzhomeTemplate]] = None
    _triggers: Optional[Dict[str, FritzhomeTrigger]] = None

    def __init__(self, host, user, password, port=None, ssl_verify=True, timeout=10, force_aha_api=False, use_testdata=False):
        """Create a fritzhome object."""
        self._user = user
        self._password = password
        self._session = Session()
        self._ssl_verify = ssl_verify
        self._timeout = timeout
        self._has_getdeviceinfos = True
        self._has_txbusy = True
        self._devices = {}
        self._units = {}
        self._use_aha = force_aha_api
        self._use_testdata = use_testdata
        if host.startswith("https://") or host.startswith("http://"):
            self.base_url = f"{host}:{port}" if port else host
        else:
            self.base_url = f"http://{host}:{port}" if port else f"http://{host}"
        self.rest_url = f"{self.base_url}/api/v0/smarthome"

    def _request(self, url, params=None, headers=None):
        """Send a request with parameters."""
        rsp = self._session.get(
            url, params=params, headers=headers, timeout=self._timeout, verify=self._ssl_verify
        )
        rsp.raise_for_status()
        return rsp.text.strip()

    def _request2(self, url, params=None, headers=None, timeout=10):
        """Send a request with parameters."""
        rsp = self._session.get(
            url, params=params, headers=headers, timeout=timeout, verify=self._ssl_verify
        )
        rsp.raise_for_status()
        return rsp

    def _put(self, url, data, params=None, headers=None, timeout=10):
        """Send a request with parameters."""
        rsp = self._session.put(
            url, params=params, headers=headers, timeout=timeout, verify=self._ssl_verify,
            json=data
        )
        rsp.raise_for_status()
        return rsp.text.strip()

    def _login_request(self, username=None, secret=None):
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
        blocktime = int(dom.findtext("BlockTime"))
        challenge = dom.findtext("Challenge")

        return (sid, challenge, blocktime)

    def _logout_request(self):
        """Send a logout request."""
        _LOGGER.debug("logout")
        url = f"{self.base_url}/login_sid.lua"
        params = {"security:command/logout": "1", "sid": self._sid}

        self._request(url, params)

    @staticmethod
    def _create_login_secrete_pbkdf2(challenge, password):
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
    def _create_login_secret_md5(challenge, password):
        """Create a login secret."""
        to_hash = (challenge + "-" + password).encode("UTF-16LE")
        hashed = hashlib.md5(to_hash).hexdigest()
        return "{0}-{1}".format(challenge, hashed)

    def _aha_request(self, cmd, ain=None, param=None, rf=str):
        """Send an AHA request."""
        url = f"{self.base_url}/webservices/homeautoswitch.lua"

        _LOGGER.debug("self._sid:%s", self._sid)

        if not self._sid:
            raise NotLoggedInError

        params = {"switchcmd": cmd, "sid": self._sid}
        if param:
            params.update(param)
        if ain:
            params["ain"] = ain

        plain = self._request(url, params)
        if plain == "inval":
            raise InvalidError

        if rf == bool:
            return bool(int(plain))
        return rf(plain)

    def _rest_request(self, endpoint, param=None):
        """Send an REST API request"""
        if self._use_testdata:
            return json.load(open(f"testdata/{endpoint.replace("/", "_")}.json.txt", "r"))
        url = f"{self.rest_url}/{endpoint}"

        _LOGGER.debug("self._sid:%s", self._sid)

        if not self._sid:
            raise NotLoggedInError

        params = {"Authorization": f"AVM-SID {self._sid}"}
        if param:
            params.update(param)

        response = self._request2(url, headers=params)
        if response.ok:
            return response.json()

        return None

    def login(self):
        """Login and get a valid session ID."""
        if self._use_testdata:
            return
        (sid, challenge, blocktime) = self._login_request()
        _LOGGER.info("sid:%s, challenge:%s, blocktime:%s", sid, challenge, blocktime)
        if sid == "0000000000000000":
            if blocktime > 0:
                time.sleep(blocktime)
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

    def logout(self):
        """Logout."""
        self._logout_request()
        self._sid = None

    def _update_unit_from_node(self, node):
        ain = node["ain"]
        if unit := self._units.get(ain):
            _LOGGER.info("Updating already existing unit " + ain)
            unit._update_from_node(node)
        else:
            _LOGGER.info("Adding new unit " + ain)
            unit = FritzhomeUnit(self, node=node)
            self._units[ain] = unit
        return unit

    def put_unit(self, ain, node):
        if self._units is None:
            self._units = {}

        _LOGGER.info("put units ...\n" + json.dumps(node))
        params = {"Authorization": f"AVM-SID {self._sid}"}
        data = self._put(f"{self.rest_url}/configuration/units/{ain}", node, headers=params)

    def _update_device_from_node(self, node):
        ain = node["ain"]
        if device := self._devices.get(ain):
            _LOGGER.info("Updating already existing device " + ain)
            device._update_from_node(node)
        else:
            _LOGGER.info("Adding new device " + ain)
            device = FritzhomeDevice(self, node=node)
            self._devices[ain] = device
        return device

    def _update_device_units(self, ain, unit_ains):
        if self._units is None:
            self._units = {}

        for unit_ain in unit_ains:
            self._update_unit_from_node(self.get_unit_element(unit_ain))
            if unit := self._units.get(unit_ain):
                self._devices[ain].add_or_update_unit(unit)
            else:
                _LOGGER.warning(f"Unknown unit {unit_ain}")

    def update_device(self, ain):
        """Update the device."""
        _LOGGER.info(f"Updating Device {ain}  ...")
        if node := self._rest_request(f"overview/devices/{ain}"):
            self._update_device_from_node(element)
            for unit_ain in node["unitUids"]:
                if node := self._rest_request(f"overview/unit/{unit_ain}"):
                    self._update_device_from_node(node)
                    return True
        return False

    def _update_device_config(self, ain):
        """Update the device, using its configuration endpoint."""
        _LOGGER.info(f"Updating Device {ain}  ...")
        device = None
        units = []
        if node := self._rest_request(f"configuration/devices/{ain}"):
            units = node.pop("units")
            device = self._update_device_from_node(node)
        for node in units:
            unit = self._update_unit_from_node(node)
            device.add_or_update_unit(unit)
        return device

    def update_devices(self, ignore_removed=True):
        """Update the device."""
        _LOGGER.info("Updating Devices ...")
        devices = self._rest_request("overview/devices")
        for node in devices:
            self._update_device_from_node(node)
        units = self._rest_request("overview/units")
        for node in units:
            self._update_unit_from_node(node)

        for device in self._devices.values():
            units = device.node["unitUids"]
            for unit_ain in units:
                if unit := self._units.get(unit_ain):
                    device.add_or_update_unit(unit)

        if not ignore_removed:
            for ain in list(self._devices.keys()):
                if ain not in [
                    element.attrib["ain"] for element in devices
                ]:
                    _LOGGER.info("Removing no more existing device " + ain)
                    self._devices.pop(ain)
            for ain in list(self._units.keys()):
                if ain not in [
                    element.attrib["ain"] for element in units
                ]:
                    _LOGGER.info("Removing no more existing device " + ain)
                    self._units.pop(ain)

        return True

    def update_units_devices(self, ignore_removed=True, with_units=False):
        """Update the device."""
        _LOGGER.info("Updating Devices ...")
        device_elements = self.get_device_elements()
        for element in device_elements:
            ain = element["ain"]
            self._update_device_from_node(element)
            if with_units:
                self._devices[ain].clear_units()
                self._update_device_units(ain, element["unitUids"])

        if not ignore_removed:
            for identifier in list(self._devices.keys()):
                if identifier not in [
                    element.attrib["identifier"] for element in device_elements
                ]:
                    _LOGGER.info("Removing no more existing device " + identifier)
                    self._devices.pop(identifier)

        return True

    def _get_listinfo_elements(self, entity_type):
        """Get the DOM elements for the entity list."""
        plain = self._aha_request("get" + entity_type + "listinfos")
        dom = ElementTree.fromstring(plain)
        _LOGGER.debug(dom)
        return dom.findall("*")

    def wait_device_txbusy(self, ain, retries=10):
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
                dom = self.get_device_element(ain)

            txbusy = dom.findall("txbusy")
            if not txbusy:
                # txbusy was added in FritzOS 7.20
                self._has_txbusy = False
                return True

            if txbusy[0].text == "0":
                return True

            time.sleep(0.2)
        return False

    def get_device_elements(self):
        """Get the JSON elements for the device list."""
        return self._rest_request("overview/devices")

    def get_devices(self):
        """Get the list of all known devices."""
        return list(self.get_devices_as_dict().values())

    def get_devices_as_dict(self):
        """Get the list of all known devices."""
        if not self._devices:
            self.update_devices()
        return self._devices

    def get_device_by_ain(self, ain):
        """Return a device specified by the AIN."""
        return self.get_devices_as_dict()[ain]

    def get_device_infos(self, ain):
        """Get the device infos."""
        return self._aha_request("getdeviceinfos", ain=ain)

    def get_device_present(self, ain):
        """Get the device presence."""
        if self._use_aha:
            return self._aha_request("getswitchpresent", ain=ain)
        return self._update_device_config(ain).is_connected

    def get_device_name(self, ain):
        """Get the device name."""
        if self._use_aha:
            return self._aha_request("getswitchname", ain=ain)
        return self._update_device_config(ain).name

    def get_switch_state(self, ain):
        """Get the switch state."""
        if self._use_aha:
            return self._aha_request("getswitchstate", ain=ain, rf=bool)
        if dev := self._update_device_config(ain):
            if not dev.has_switch:
                _LOGGER.error(f"Device {dev.name} is not a switch")
                return None
            return dev.switch_state

    def set_switch_state_on(self, ain, wait=False):
        """Set the switch to on state."""
        if self.update_device(ain):
            self._devices[ain].set_switch_state_on()
        return None

    def set_switch_state_off(self, ain, wait=False):
        """Set the switch to off state."""
        if self.update_device(ain):
            self._devices[ain].set_switch_state_off()
        return None

    def set_switch_state_toggle(self, ain, wait=False):
        """Toggle the switch state."""
        if self.update_device(ain):
            self._devices[ain].set_switch_state_toggle()
        return None

    def get_switch_power(self, ain):
        """Get the switch power consumption."""
        if self._use_aha:
            return self._aha_request("getswitchpower", ain=ain, rf=int)
        if dev := self._update_device_config(ain):
            if not dev.has_powermeter:
                _LOGGER.error(f"Device {dev.name} is not a powermeter")
                return None
            return dev.power

    def get_switch_energy(self, ain):
        """Get the switch energy."""
        if self._use_aha:
            return self._aha_request("getswitchenergy", ain=ain, rf=int)
        if dev := self._update_device_config(ain):
            if not dev.has_powermeter:
                _LOGGER.error(f"Device {dev.name} is not a powermeter")
                return None
            return dev.energy

    def get_temperature(self, ain):
        """Get the device temperature sensor value."""
        if self._use_aha:
            return self._aha_request("gettemperature", ain=ain, rf=float) / 10.0
        if dev := self._update_device_config(ain):
            if not dev.has_temperature_sensor:
                _LOGGER.error(f"Device {dev.name} is not a thermometer")
                return None
            return float(dev.temperature)

    def _get_temperature(self, ain, name):
        plain = self._aha_request(name, ain=ain, rf=float)
        return plain / 2

    def get_target_temperature(self, ain):
        """Get the thermostate target temperature."""
        if self._use_aha:
            return self._get_temperature(ain, "gethkrtsoll")
        if dev := self._update_device_config(ain):
            if not dev.has_temperature_sensor:
                _LOGGER.error(f"Device {dev.name} is not a thermometer")
                return None
            return float(dev.temperature)

    def set_target_temperature(self, ain, temperature, wait=False):
        """Set the thermostate target temperature."""
        temp = int(temperature * 2)

        if temp < 16:
            temp = 253
        elif temp > 56:
            temp = 254

        self._aha_request("sethkrtsoll", ain=ain, param={"param": temp})
        wait and self.wait_device_txbusy(ain)

    def set_window_open(self, ain, seconds, wait=False):
        """Set the thermostate target temperature."""
        endtimestamp = int(time.time() + seconds)

        self._aha_request(
            "sethkrwindowopen", ain=ain, param={"endtimestamp": endtimestamp}
        )
        wait and self.wait_device_txbusy(ain)

    def set_boost_mode(self, ain, seconds, wait=False):
        """Set the thermostate to boost mode."""
        endtimestamp = int(time.time() + seconds)

        self._aha_request("sethkrboost", ain=ain, param={"endtimestamp": endtimestamp})
        wait and self.wait_device_txbusy(ain)

    def get_comfort_temperature(self, ain):
        """Get the thermostate comfort temperature."""
        return self._get_temperature(ain, "gethkrkomfort")

    def get_eco_temperature(self, ain):
        """Get the thermostate eco temperature."""
        return self._get_temperature(ain, "gethkrabsenk")

    def get_device_statistics(self, ain):
        """Get device statistics."""
        if self._use_aha:
            return self._aha_request("getbasicdevicestats", ain=ain)
        stats = {"statistics":[]}
        for unit in self._update_device_config(ain).units():
            if s := unit.statistics:
                stats["statistics"].append(s)
        return json.dumps(stats)

    # Lightbulb-related commands

    def set_state_off(self, ain, wait=False):
        """Set the switch/actuator/lightbulb to on state."""
        self._aha_request("setsimpleonoff", ain=ain, param={"onoff": 0})
        wait and self.wait_device_txbusy(ain)

    def set_state_on(self, ain, wait=False):
        """Set the switch/actuator/lightbulb to on state."""
        self._aha_request("setsimpleonoff", ain=ain, param={"onoff": 1})
        wait and self.wait_device_txbusy(ain)

    def set_state_toggle(self, ain, wait=False):
        """Toggle the switch/actuator/lightbulb state."""
        self._aha_request("setsimpleonoff", ain=ain, param={"onoff": 2})
        wait and self.wait_device_txbusy(ain)

    def set_level(self, ain, level, wait=False):
        """Set level/brightness/height in interval [0,255]."""
        if level < 0:
            level = 0  # 0%
        elif level > 255:
            level = 255  # 100 %

        self._aha_request("setlevel", ain=ain, param={"level": int(level)})
        wait and self.wait_device_txbusy(ain)

    def set_level_percentage(self, ain, level, wait=False):
        """Set level/brightness/height in interval [0,100]."""
        if level < 0:
            level = 0
        elif level > 100:
            level = 100

        self._aha_request("setlevelpercentage", ain=ain, param={"level": int(level)})
        wait and self.wait_device_txbusy(ain)

    def _get_colordefaults(self, ain):
        plain = self._aha_request("getcolordefaults", ain=ain)
        return ElementTree.fromstring(plain)

    def get_colors(self, ain):
        """Get colors (HSV-space) supported by this lightbulb."""
        colordefaults = self._get_colordefaults(ain)
        colors = {}
        for hs in colordefaults.iter("hs"):
            name = hs.find("name").text.strip()
            values = []
            for st in hs.iter("color"):
                values.append((st.get("hue"), st.get("sat"), st.get("val")))
            colors[name] = values
        return colors

    def set_color(self, ain, hsv, duration=0, mapped=True, wait=False):
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

    def get_color_temps(self, ain):
        """Get temperatures supported by this lightbulb."""
        colordefaults = self._get_colordefaults(ain)
        temperatures = []
        for temp in colordefaults.iter("temp"):
            temperatures.append(temp.get("value"))
        return temperatures

    def set_color_temp(self, ain, temperature, duration=0, wait=False):
        """Set color temperature.

        temperature: temperature element obtained from get_temperatures()
        duration: Speed of change in seconds, 0 = instant
        """
        params = {"temperature": int(temperature), "duration": int(duration) * 10}
        self._aha_request("setcolortemperature", ain=ain, param=params)
        wait and self.wait_device_txbusy(ain)

    # blinds
    # states: open, close, stop
    def _set_blind_state(self, ain, state):
        self._aha_request("setblind", ain=ain, param={"target": state})

    def set_blind_open(self, ain, wait=False):
        """Set the blind state to open."""
        self._set_blind_state(ain, "open")
        wait and self.wait_device_txbusy(ain)

    def set_blind_close(self, ain, wait=False):
        """Set the blind state to close."""
        self._set_blind_state(ain, "close")
        wait and self.wait_device_txbusy(ain)

    def set_blind_stop(self, ain, wait=False):
        """Set the blind state to stop."""
        self._set_blind_state(ain, "stop")
        wait and self.wait_device_txbusy(ain)

    # Template-related commands

    def has_templates(self):
        """Check if the Fritz!Box supports smarthome templates."""
        plain = self._aha_request("gettemplatelistinfos")
        try:
            ElementTree.fromstring(plain)
        except ElementTree.ParseError:
            return False
        return True

    def update_templates(self, ignore_removed=True):
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

    def get_template_elements(self):
        """Get the DOM elements for the template list."""
        return self._get_listinfo_elements("template")

    def get_templates(self):
        """Get the list of all known templates."""
        return list(self.get_templates_as_dict().values())

    def get_templates_as_dict(self):
        """Get the list of all known templates."""
        if self._templates is None:
            self.update_templates()
        return self._templates

    def get_template_by_ain(self, ain):
        """Return a template specified by the AIN."""
        return self.get_templates_as_dict()[ain]

    def apply_template(self, ain):
        """Appliy a template."""
        self._aha_request("applytemplate", ain=ain)

    # Trigger-related commands

    def has_triggers(self):
        """Check if the Fritz!Box supports smarthome triggers."""
        plain = self._aha_request("gettriggerlistinfos")
        try:
            ElementTree.fromstring(plain)
        except ElementTree.ParseError:
            return False
        return True

    def update_triggers(self, ignore_removed=True):
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

    def get_trigger_elements(self):
        """Get the DOM elements for the trigger list."""
        return self._get_listinfo_elements("trigger")

    def get_triggers(self):
        """Get the list of all known triggers."""
        return list(self.get_triggers_as_dict().values())

    def get_triggers_as_dict(self):
        """Get all known triggers as dictionary."""
        if self._triggers is None:
            self.update_triggers()
        return self._triggers

    def get_trigger_by_ain(self, ain):
        """Return a trigger specified by the AIN."""
        return self.get_triggers_as_dict()[ain]

    def _set_trigger_state(self, ain, state):
        self._aha_request("settriggeractive", ain=ain, param={"active": state})

    def set_trigger_active(self, ain):
        """Set the trigger to active state."""
        self._set_trigger_state(ain, "1")

    def set_trigger_inactive(self, ain):
        """Set the trigger to inactive state."""
        self._set_trigger_state(ain, "0")
