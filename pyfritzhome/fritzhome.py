# -*- coding: utf-8 -*-

from __future__ import print_function

import hashlib
import logging
from xml.etree import ElementTree

from requests import Session

from .errors import InvalidError, LoginError
from .fritzhomedevice import FritzhomeDevice
from typing import Dict

_LOGGER = logging.getLogger(__name__)


class Fritzhome(object):
    """Fritzhome object to communicate with the device."""

    _sid = None
    _session = None
    _devices: Dict[str, FritzhomeDevice] = None

    def __init__(self, host, user, password):
        self._host = host
        self._user = user
        self._password = password
        self._session = Session()

    def _request(self, url, params=None, timeout=10):
        """Send a request with parameters."""
        rsp = self._session.get(url, params=params, timeout=timeout)
        rsp.raise_for_status()
        return rsp.text.strip()

    def _login_request(self, username=None, secret=None):
        """Send a login request with paramerters."""
        url = self.get_prefixed_host() + "/login_sid.lua"
        params = {}
        if username:
            params["username"] = username
        if secret:
            params["response"] = secret

        plain = self._request(url, params)
        dom = ElementTree.fromstring(plain)
        sid = dom.findtext("SID")
        challenge = dom.findtext("Challenge")

        return (sid, challenge)

    def _logout_request(self):
        """Send a logout request."""
        _LOGGER.debug("logout")
        url = self.get_prefixed_host() + "/login_sid.lua"
        params = {"security:command/logout": "1", "sid": self._sid}

        self._request(url, params)

    @staticmethod
    def _create_login_secret(challenge, password):
        """Create a login secret."""
        to_hash = (challenge + "-" + password).encode("UTF-16LE")
        hashed = hashlib.md5(to_hash).hexdigest()
        return "{0}-{1}".format(challenge, hashed)

    def _aha_request(self, cmd, ain=None, param=None, rf=str):
        """Send an AHA request."""
        url = self.get_prefixed_host() + "/webservices/homeautoswitch.lua"
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
        try:
            (sid, challenge) = self._login_request()
            if sid == "0000000000000000":
                secret = self._create_login_secret(challenge, self._password)
                (sid2, challenge) = self._login_request(
                    username=self._user, secret=secret
                )
                if sid2 == "0000000000000000":
                    _LOGGER.warning("login failed %s", sid2)
                    raise LoginError(self._user)
                self._sid = sid2
        except Exception:
            raise LoginError(self._user)

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

    def update_devices(self):
        _LOGGER.info("Updating Devices ...")
        if self._devices is None:
            self._devices = {}

        for element in self.get_device_elements():
            if element.attrib["identifier"] in self._devices.keys():
                _LOGGER.info(
                    "Updating already existing Device " + element.attrib["identifier"]
                )
                self._devices[element.attrib["identifier"]]._update_from_node(element)
            else:
                _LOGGER.info("Adding new Device " + element.attrib["identifier"])
                device = FritzhomeDevice(self, node=element)
                self._devices[device.ain] = device
        return True

    def get_device_elements(self):
        """Get the DOM elements for the device list."""
        plain = self._aha_request("getdevicelistinfos")
        dom = ElementTree.fromstring(plain)
        _LOGGER.debug(dom)
        return dom.findall("device")

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
        """Returns a device specified by the AIN."""
        return self.get_devices_as_dict()[ain]

    def get_device_present(self, ain):
        """Get the device presence."""
        return self._aha_request("getswitchpresent", ain=ain, rf=bool)

    def get_device_name(self, ain):
        """Get the device name."""
        return self._aha_request("getswitchname", ain=ain)

    def get_switch_state(self, ain):
        """Get the switch state."""
        return self._aha_request("getswitchstate", ain=ain, rf=bool)

    def set_switch_state_on(self, ain):
        """Set the switch to on state."""
        return self._aha_request("setswitchon", ain=ain, rf=bool)

    def set_switch_state_off(self, ain):
        """Set the switch to off state."""
        return self._aha_request("setswitchoff", ain=ain, rf=bool)

    def set_switch_state_toggle(self, ain):
        """Toggle the switch state."""
        return self._aha_request("setswitchtoggle", ain=ain, rf=bool)

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
        return (plain - 16) / 2 + 8

    def get_target_temperature(self, ain):
        """Get the thermostate target temperature."""
        return self._get_temperature(ain, "gethkrtsoll")

    def set_target_temperature(self, ain, temperature):
        """Set the thermostate target temperature."""
        temp = int(16 + ((float(temperature) - 8) * 2))

        if temp < min(range(16, 56)):
            temp = 253
        elif temp > max(range(16, 56)):
            temp = 254

        self._aha_request("sethkrtsoll", ain=ain, param={'param': temp})

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

    def set_state_off(self, ain):
        """Set the switch/actuator/lightbulb to on state."""
        self._aha_request("setsimpleonoff", ain=ain, param={'onoff': 0})

    def set_state_on(self, ain):
        """Set the switch/actuator/lightbulb to on state."""
        self._aha_request("setsimpleonoff", ain=ain, param={'onoff': 1})

    def set_state_toggle(self, ain):
        """Toggle the switch/actuator/lightbulb state."""
        self._aha_request("setsimpleonoff", ain=ain, param={'onoff': 2})

    def set_level(self, ain, level):
        """Set level/brightness/height in interval [0,255] """

        if level < 0:
            level = 0      # 0%
        elif level > 255:
            level = 255    # 100 %

        self._aha_request("setlevel", ain=ain, param={'level': int(level)})

    def set_level_percentage(self, ain, level):
        """Set level/brightness/height in interval [0,100] """

        # Scale percentage to [0,255] interval
        self.set_level(ain, int(level*2.55))

    def _get_colordefaults(self, ain):
        plain = self._aha_request("getcolordefaults", ain=ain)
        return ElementTree.fromstring(plain)

    def get_colors(self, ain):
        """Get colors (HSV-space) supported by this lightbulb"""
        colordefaults = self._get_colordefaults(ain)
        colors = {}
        for hs in colordefaults.iter('hs'):
            name = hs.find("name").text.strip()
            values = []
            for st in hs.iter("color"):
                values.append(
                    (
                        st.get("hue"),
                        st.get("sat"),
                        st.get("val")
                    )
                )
            colors[name] = values
        return colors

    def set_color(self, ain, hsv, duration=0):
        """Set hue and saturation
        hsv: HUE colorspace element obtained from get_colors()
        duration: Speed of change in seconds, 0 = instant
        """
        params = {
            'hue': int(hsv[0]),
            'saturation': int(hsv[1]),
            "duration": int(duration)*10
        }
        self._aha_request("setcolor", ain=ain, param=params)

    def get_color_temps(self, ain):
        """Get temperatures supported by this lightbulb"""
        colordefaults = self._get_colordefaults(ain)
        temperatures = []
        for temp in colordefaults.iter('temp'):
            temperatures.append(temp.get("value"))
        return temperatures

    def set_color_temp(self, ain, temperature, duration=0):
        """Set color temperature
        temperature: temperature element obtained from get_temperatures()
        duration: Speed of change in seconds, 0 = instant
        """
        params = {
            'temperature': int(temperature),
            "duration": int(duration)*10
        }
        self._aha_request("setcolortemperature", ain=ain, param=params)
