# -*- coding: utf-8 -*-

from __future__ import print_function

import logging
from array import array
from xml.etree import ElementTree

from pyfritzhome.fritzhomebutton import FritzhomeButton

from .fritzhomedevicefeatures import FritzhomeDeviceFeatures

_LOGGER = logging.getLogger(__name__)


def get_node_value(elem, node):
    return elem.findtext(node)


def get_node_value_as_int(elem, node) -> int:
    return int(get_node_value(elem, node))


def get_node_value_as_int_as_bool(elem, node) -> bool:
    return bool(get_node_value_as_int(elem, node))


def get_temp_from_node(elem, node):
    return float(get_node_value(elem, node)) / 2


class FritzhomeDevice(object):
    """The Fritzhome Device class."""

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
    buttons = None
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

    def _has_feature(self, feature: FritzhomeDeviceFeatures) -> bool:
        return feature in FritzhomeDeviceFeatures(self._functionsbitmask)

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

        if self.has_alarm:
            self._update_alarm_from_node(node)
        if self.has_powermeter:
            self._update_powermeter_from_node(node)
        if self.has_switch:
            self._update_switch_from_node(node)
        if self.has_button:
            self._update_button_from_node(node)
        if self.has_temperature_sensor:
            self._update_temperature_from_node(node)
        if self.has_thermostat:
            self._update_hkr_from_node(node)

    # region General
    def get_present(self):
        """Check if the device is present."""
        return self._fritz.get_device_present(self.ain)
    # endregion General

    # region Thermostat
    @property
    def has_thermostat(self):
        """Check if the device has thermostat function."""
        return self._has_feature(FritzhomeDeviceFeatures.THERMOSTAT)

    def _update_hkr_from_node(self, node):
        hkr_element = node.find("hkr")

        try:
            self.actual_temperature = get_temp_from_node(hkr_element, "tist")
        except ValueError:
            pass

        self.target_temperature = get_temp_from_node(hkr_element, "tsoll")
        self.eco_temperature = get_temp_from_node(hkr_element, "absenk")
        self.comfort_temperature = get_temp_from_node(hkr_element, "komfort")

        # optional value
        try:
            self.device_lock = get_node_value_as_int_as_bool(hkr_element, "devicelock")
            self.lock = get_node_value_as_int_as_bool(hkr_element, "lock")
            self.error_code = get_node_value_as_int(hkr_element, "errorcode")
            self.battery_low = get_node_value_as_int_as_bool(hkr_element, "batterylow")
            self.battery_level = int(get_node_value_as_int(hkr_element, "battery"))
            self.window_open = get_node_value_as_int_as_bool(
                hkr_element, "windowopenactiv"
            )
            self.summer_active = get_node_value_as_int_as_bool(
                hkr_element, "summeractive"
            )
            self.holiday_active = get_node_value_as_int_as_bool(
                hkr_element, "holidayactive"
            )
        except Exception:
            pass

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
    # endregion Thermostat

    # region Buttons
    @property
    def has_button(self):
        """Check if the device has button(s) function."""
        return self._has_feature(FritzhomeDeviceFeatures.BUTTON)

    def _update_button_from_node(self, mainNode):
        self.buttons = []
        for element in mainNode.findall("button"):
            button = FritzhomeButton(node=element)
            self.buttons.append(button)
    # endregion Buttons

    # region Switch
    @property
    def has_switch(self):
        """Check if the device has switch function."""
        return self._has_feature(FritzhomeDeviceFeatures.SWITCH)

    def _update_switch_from_node(self, node):
        val = node.find("switch")
        self.switch_state = get_node_value_as_int_as_bool(val, "state")
        self.switch_mode = get_node_value(val, "mode")
        self.lock = bool(get_node_value(val, "lock"))
        # optional value
        try:
            self.device_lock = get_node_value_as_int_as_bool(val, "devicelock")
        except Exception:
            pass

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
    # endregion Switch

    # region Power Meter
    @property
    def has_powermeter(self):
        """Check if the device has powermeter function."""
        return self._has_feature(FritzhomeDeviceFeatures.POWER_METER)

    def _update_powermeter_from_node(self, node):
        val = node.find("powermeter")
        self.power = int(val.findtext("power"))
        self.energy = int(val.findtext("energy"))
        try:
            self.voltage = float(int(val.findtext("voltage")) / 1000)
        except Exception:
            pass

    def get_switch_power(self):
        """ the switch state."""
        return self._fritz.get_switch_power(self.ain)

    def get_switch_energy(self):
        """Get the switch energy."""
        return self._fritz.get_switch_energy(self.ain)
    # endregion Power Meter

    # region Temperature
    @property
    def has_temperature_sensor(self):
        """Check if the device has temperature function."""
        return self._has_feature(FritzhomeDeviceFeatures.TEMPERATURE)

    def _update_temperature_from_node(self, node):
        temperature_element = node.find("temperature")
        try:
            self.offset = get_node_value_as_int(temperature_element, "offset") / 10.0
        except ValueError:
            pass

        try:
            self.temperature = (
                get_node_value_as_int(temperature_element, "celsius") / 10.0
            )
        except ValueError:
            pass
    # endregion Temperature

    # region Alarm
    @property
    def has_alarm(self):
        """Check if the device has alarm function."""
        return self._has_feature(FritzhomeDeviceFeatures.ALARM)

    def _update_alarm_from_node(self, node):
        val = node.find("alert")
        try:
            self.alert_state = get_node_value_as_int_as_bool(val, "state")
        except (Exception, ValueError):
            pass
    # endregion Alarm

    # region Repeater
    @property
    def has_repeater(self):
        """Check if the device has repeater function."""
        return self._has_feature(FritzhomeDeviceFeatures.DECT_REPEATER)
    # endregion Repeater
