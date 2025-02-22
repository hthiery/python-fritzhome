"""The main fritzhome handling class."""
# -*- coding: utf-8 -*-

from __future__ import print_function

import hashlib
import logging
import time
from xml.etree import ElementTree

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from requests import exceptions, Session

from .errors import InvalidError, LoginError, NotLoggedInError
from .fritzhomedevice import FritzhomeDevice
from .fritzhomedevice import FritzhomeTemplate
from typing import Dict

_LOGGER = logging.getLogger(__name__)


class Fritzhome(object):
    """Fritzhome object to communicate with the device."""

    _sid = None
    _session = None
    _devices: Dict[str, FritzhomeDevice] = None
    _templates: Dict[str, FritzhomeTemplate] = None

    def __init__(self, host, user, password, ssl_verify=True):
        """Create a fritzhome object."""
        self._host = host
        self._user = user
        self._password = password
        self._session = Session()
        self._ssl_verify = ssl_verify
        self._has_getdeviceinfos = True
        self._has_txbusy = True

    def _request(self, url, params=None, timeout=10):
        """Send a request with parameters."""
        rsp = self._session.get(
            url, params=params, timeout=timeout, verify=self._ssl_verify
        )
        rsp.raise_for_status()
        return rsp.text.strip()

    def _login_request(self, username=None, secret=None):
        """Send a login request with paramerters."""
        url = self.get_prefixed_host() + "/login_sid.lua?version=2"
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
        url = self.get_prefixed_host() + "/login_sid.lua"
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
        url = self.get_prefixed_host() + "/webservices/homeautoswitch.lua"

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

    def login(self):
        """Login and get a valid session ID."""
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

    def get_prefixed_host(self):
        """Choose the correct protocol prefix for the host.

        Supports three input formats:
        - https://<host>(requests use strict certificate validation by default)
        - http://<host> (unecrypted)
        - <host> (unencrypted)
        """
        host = self._host
        if host.startswith("https://") or host.startswith("http://"):
            return host
        else:
            return "http://" + host

    def update_devices(self, ignore_removed=True):
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
        """Get the DOM elements for the device list."""
        return self._get_listinfo_elements("device")

    def get_device_element(self, ain):
        """Get the DOM element for the specified device."""
        elements = self.get_device_elements()
        for element in elements:
            if element.attrib["identifier"] == ain:
                return element
        return None

    def get_devices(self):
        """Get the list of all known devices."""
        return list(self.get_devices_as_dict().values())

    def get_devices_as_dict(self):
        """Get the list of all known devices."""
        if self._devices is None:
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
        return self._aha_request("getswitchpresent", ain=ain, rf=bool)

    def get_device_name(self, ain):
        """Get the device name."""
        return self._aha_request("getswitchname", ain=ain)

    def get_switch_state(self, ain):
        """Get the switch state."""
        return self._aha_request("getswitchstate", ain=ain, rf=bool)

    def set_switch_state_on(self, ain, wait=False):
        """Set the switch to on state."""
        result = self._aha_request("setswitchon", ain=ain, rf=bool)
        wait and self.wait_device_txbusy(ain)
        return result

    def set_switch_state_off(self, ain, wait=False):
        """Set the switch to off state."""
        result = self._aha_request("setswitchoff", ain=ain, rf=bool)
        wait and self.wait_device_txbusy(ain)
        return result

    def set_switch_state_toggle(self, ain, wait=False):
        """Toggle the switch state."""
        result = self._aha_request("setswitchtoggle", ain=ain, rf=bool)
        wait and self.wait_device_txbusy(ain)
        return result

    def get_switch_power(self, ain):
        """Get the switch power consumption."""
        return self._aha_request("getswitchpower", ain=ain, rf=int)

    def get_switch_energy(self, ain):
        """Get the switch energy."""
        return self._aha_request("getswitchenergy", ain=ain, rf=int)

    def get_temperature(self, ain):
        """Get the device temperature sensor value."""
        return self._aha_request("gettemperature", ain=ain, rf=float) / 10.0

    def _get_temperature(self, ain, name):
        plain = self._aha_request(name, ain=ain, rf=float)
        return plain / 2

    def get_target_temperature(self, ain):
        """Get the thermostate target temperature."""
        return self._get_temperature(ain, "gethkrtsoll")

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
        plain = self._aha_request("getbasicdevicestats", ain=ain)
        return plain

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
