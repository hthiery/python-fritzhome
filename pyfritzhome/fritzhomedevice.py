# -*- coding: utf-8 -*-

from __future__ import print_function

import logging
from xml.etree import ElementTree

_LOGGER = logging.getLogger(__name__)


def get_node_value(elem, node):
    return elem.findtext(node)


def bits(value):
    while value:
        bit = value & (~value + 1)
        yield bit
        value ^= bit


class FritzhomeDevice(object):
    """The Fritzhome Device class."""

    ALARM_MASK = 0x010
    UNKNOWN_MASK = 0x020
    THERMOSTAT_MASK = 0x040
    POWER_METER_MASK = 0x080
    TEMPERATURE_MASK = 0x100
    SWITCH_MASK = 0x200
    DECT_REPEATER_MASK = 0x400
    MICROPHONE_UNIT = 0x800
    HANFUN_UNIT = 0x2000

    ain = None
    identifier = None
    fw_version = None
    manufacturer = None
    productname = None
    actual_temperature = None
    target_temperature = None
    eco_temperature = None
    comfort_temperature = None
    battery_level = None
    window_open = None
    summer_active = None
    holiday_active = None
    lock = None
    device_lock = None
    error_code = None
    battery_low = None
    switch_state = None
    switch_mode = None
    power = None
    energy = None
    voltage = None
    offset = None
    temperature = None
    alert_state = None

    def __init__(self, fritz=None, node=None):
        if fritz is not None:
            self._fritz = fritz
        if node is not None:
            self._update_from_node(node)

    def _update_from_node(self, node):
        _LOGGER.debug(ElementTree.tostring(node))
        self.ain = node.attrib["identifier"]
        self.identifier = node.attrib["id"]
        self._functionsbitmask = int(node.attrib["functionbitmask"])
        self.fw_version = node.attrib["fwversion"]
        self.manufacturer = node.attrib["manufacturer"]
        self.productname = node.attrib["productname"]

        self.name = node.findtext("name")
        self.present = bool(int(node.findtext("present")))

        if self.present is False:
            return

        for bit in bits(self._functionsbitmask):
            try:
                fct = {
                    self.ALARM_MASK: self._update_alarm_from_node,
                    self.POWER_METER_MASK: self._update_powermeter_from_node,
                    self.SWITCH_MASK: self._update_switch_from_node,
                    self.TEMPERATURE_MASK: self._update_temperature_from_node,
                    self.THERMOSTAT_MASK: self._update_hkr_from_node,
                }[bit]
                fct(node)
            except KeyError:
                pass

    def _get_temp_from_node(self, elem, node):
        return float(get_node_value(elem, node)) / 2

    def _update_hkr_from_node(self, node):
        val = node.find("hkr")

        try:
            self.actual_temperature = self._get_temp_from_node(val, "tist")
        except ValueError:
            pass

        self.target_temperature = self._get_temp_from_node(val, "tsoll")
        self.eco_temperature = self._get_temp_from_node(val, "absenk")
        self.comfort_temperature = self._get_temp_from_node(val, "komfort")

        # optional value
        try:
            self.device_lock = bool(int(get_node_value(val, "devicelock")))
        except Exception:
            pass

        try:
            self.lock = bool(int(get_node_value(val, "lock")))
        except Exception:
            pass

        try:
            self.error_code = int(get_node_value(val, "errorcode"))
        except Exception:
            pass

        try:
            self.battery_low = bool(int(get_node_value(val, "batterylow")))
        except Exception:
            pass

        try:
            self.battery_level = int(int(get_node_value(val, "battery")))
        except Exception:
            pass

        try:
            self.window_open = bool(int(get_node_value(val, "windowopenactiv")))
        except Exception:
            pass

        try:
            self.summer_active = bool(int(get_node_value(val, "summeractive")))
        except Exception:
            pass

        try:
            self.holiday_active = bool(int(get_node_value(val, "holidayactive")))
        except Exception:
            pass

    def _update_switch_from_node(self, node):
        val = node.find("switch")
        self.switch_state = bool(int(get_node_value(val, "state")))
        self.switch_mode = get_node_value(val, "mode")
        self.lock = bool(get_node_value(val, "lock"))
        # optional value
        try:
            self.device_lock = bool(int(get_node_value(val, "devicelock")))
        except Exception:
            pass

    def _update_powermeter_from_node(self, node):
        val = node.find("powermeter")
        self.power = int(val.findtext("power"))
        self.energy = int(val.findtext("energy"))
        try:
            self.voltage = float(int(val.findtext("voltage")) / 1000)
        except Exception:
            pass

    def _update_temperature_from_node(self, node):
        val = node.find("temperature")
        try:
            self.offset = int(get_node_value(val, "offset")) / 10.0
        except ValueError:
            pass

        try:
            self.temperature = int(get_node_value(val, "celsius")) / 10.0
        except ValueError:
            pass

    def _update_alarm_from_node(self, node):
        val = node.find("alert")
        try:
            self.alert_state = bool(int(get_node_value(val, "state")))
        except (Exception, ValueError):
            pass

    def __repr__(self):
        """Return a string."""
        return "{ain} {identifier} {manuf} {prod} {name}".format(
            ain=self.ain,
            identifier=self.identifier,
            manuf=self.manufacturer,
            prod=self.productname,
            name=self.name,
        )

    def update(self):
        """Update the device values."""
        node = self._fritz.get_device_element(self.ain)
        self._update_from_node(node)

    @property
    def has_alarm(self):
        """Check if the device has alarm function."""
        return bool(self._functionsbitmask & self.ALARM_MASK)

    @property
    def has_thermostat(self):
        """Check if the device has thermostat function."""
        return bool(self._functionsbitmask & self.THERMOSTAT_MASK)

    @property
    def has_powermeter(self):
        """Check if the device has powermeter function."""
        return bool(self._functionsbitmask & self.POWER_METER_MASK)

    @property
    def has_temperature_sensor(self):
        """Check if the device has temperature function."""
        return bool(self._functionsbitmask & self.TEMPERATURE_MASK)

    @property
    def has_switch(self):
        """Check if the device has switch function."""
        return bool(self._functionsbitmask & self.SWITCH_MASK)

    @property
    def has_repeater(self):
        """Check if the device has repeater function."""
        return bool(self._functionsbitmask & self.DECT_REPEATER_MASK)

    def get_present(self):
        """Check if the device is present."""
        return self._fritz.get_device_present(self.ain)

    def get_switch_state(self):
        """Get the switch state."""
        return self._fritz.get_switch_state(self.ain)

    def set_switch_state_on(self):
        """Set the switch state to on."""
        return self._fritz.set_switch_state_on(self.ain)

    def set_switch_state_off(self):
        """Set the switch state to off."""
        return self._fritz.set_switch_state_off(self.ain)

    def set_switch_state_toggle(self):
        """Toggle the switch state."""
        return self._fritz.set_switch_state_toggle(self.ain)

    def get_switch_power(self):
        """ the switch state."""
        return self._fritz.get_switch_power(self.ain)

    def get_switch_energy(self):
        """Get the switch energy."""
        return self._fritz.get_switch_energy(self.ain)

    def get_temperature(self):
        """Get the device temperature value."""
        return self._fritz.get_temperature(self.ain)

    def get_target_temperature(self):
        """Get the thermostate target temperature."""
        return self._fritz.get_target_temperature(self.ain)

    def set_target_temperature(self, temperature):
        """Set the thermostate target temperature."""
        return self._fritz.set_target_temperature(self.ain, temperature)

    def get_comfort_temperature(self):
        """Get the thermostate comfort temperature."""
        return self._fritz.get_comfort_temperature(self.ain)

    def get_eco_temperature(self):
        """Get the thermostate eco temperature."""
        return self._fritz.get_eco_temperature(self.ain)

    def get_hkr_state(self):
        """Get the thermostate state."""
        self.update()
        try:
            return {
                126.5: "off",
                127.0: "on",
                self.eco_temperature: "eco",
                self.comfort_temperature: "comfort",
            }[self.target_temperature]
        except KeyError:
            return "manual"

    def set_hkr_state(self, state):
        """Set the state of the thermostat.

        Possible values for state are: 'on', 'off', 'comfort', 'eco'.
        """
        try:
            value = {
                "off": 0,
                "on": 100,
                "eco": self.eco_temperature,
                "comfort": self.comfort_temperature,
            }[state]
        except KeyError:
            return

        self.set_target_temperature(value)
