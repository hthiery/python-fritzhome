"""The powermeter device class."""
# -*- coding: utf-8 -*-

import logging

from .interfacebase import FritzhomeInterfaceBase

_LOGGER = logging.getLogger(__name__)


class FritzhomeThermostatInterface(FritzhomeInterfaceBase):
    """The Fritzhome Device class."""

    def __init__(self, unit, type, node):
        super().__init__(unit, type, node)
        if type == "thermostatInterface":
            FritzhomeInterfaceBase.node_property("setPointTemperature", "celsius")
            FritzhomeInterfaceBase.node_property("comfortTemperature", "celsius")
            FritzhomeInterfaceBase.node_property("reducedTemperature", "celsius")

    @property
    def is_thermostat(self):
        return self.type == "thermostatInterface"

    def _update_from_node(self, node):
        super()._update_from_node(node)
        _LOGGER.debug(f"update {self.type}")

    @property
    def target_temperature(self):
        if self._node["setPointTemperature"]["mode"] == "temperature":
            return self._node["setPointTemperature"]["celsius"]
        return None

    @property
    def thermostat_mode(self):
        return self._node["setPointTemperature"]["mode"]

    def set_thermostat_mode(self, v, wait=False):
        self._node_set["setPointTemperature"] = {}
        self._node_set["setPointTemperature"]["mode"] = v
        self.changed(wait)

    def set_target_temperature(self, v, wait=False):
        self._node_set["setPointTemperature"] = {}
        self._node_set["setPointTemperature"]["celsius"] = v
        self._node_set["setPointTemperature"]["mode"] = "temperature"
        self.changed(wait)

    @property
    def comfort_temperature(self):
        return self._node["comfortTemperature"]["celsius"]

    def set_comfort_temperature(self, v, wait=False):
        self._node_set["comfortTemperature"]= {}
        self._node_set["comfortTemperature"]["celsius"] = v
        self._node_set["comfortTemperature"]["mode"] = "temperature"
        self.changed(wait)

    @property
    def reduced_temperature(self):
        return self._node["reducedTemperature"]["celsius"]

    def set_reduced_temperature(self, v, wait=False):
        self._node_set["reducedTemperature"]= {}
        self._node_set["reducedTemperature"]["celsius"] = v
        self._node_set["reducedTemperature"]["mode"] = "temperature"
        self.changed(wait)

    @property
    def holiday_active(self):
        return self._node["isHolidayActive"]

    @property
    def adaptive_heating_active(self):
        return self._node["isAdaptiveActive"]

    @property
    def adaptive_heating_running(self):
        # not always exposed (only through /smarthome/configuration/… endpoints)
        return self._node.get("adaptiveHeatingModeEnabled")

    @property
    def summer_active(self):
        return self._node["isSummertimeActive"]

    @property
    def window_open(self):
        return self._node["windowOpenMode"]["enabled"]

    @property
    def window_open_endtime(self):
        return self._node["windowOpenMode"]["endTime"]

    @property
    def boost_active(self):
        return self._node["boost"]["enabled"]

    @property
    def boost_active_endtime(self):
        return self._node["boost"]["endTime"]

    def set_boost_mode(self, duration_secs, wait=False):
        import time
        self._node_set["boost"] = {}
        if duration_secs > 0:
            self._node_set["boost"]["enabled"] = True
            self._node_set["boost"]["endTime"] = int(time.time() + duration_secs)
        else:
            self._node_set["boost"]["enabled"] = False
            self._node_set["boost"]["endTime"] = 0
        self.changed(wait)

    def set_window_open(self, duration_secs, wait=False):
        import time
        self._node_set["windowOpenMode"] = {}
        if duration_secs > 0:
            self._node_set["windowOpenMode"]["enabled"] = True
            self._node_set["windowOpenMode"]["endTime"] = int(time.time() + duration_secs)
        else:
            self._node_set["windowOpenMode"]["enabled"] = False
            self._node_set["windowOpenMode"]["endTime"] = 0
        self.changed(wait)

class FritzhomeThermostatMixin():
    """The Fritzhome Thermostat mixin."""

    def find_thermostat_interface(self):
        return self.find_interface("thermostatInterface")

    @property
    def has_thermostat(self):
        """Check if the device has thermostat sensors."""
        return self.find_thermostat_interface() != None

    @property
    def target_temperature(self):
        """ Get the current thermostat """
        return self.find_thermostat_interface().target_temperature

    def set_target_temperature(self, v, wait=False):
        """ Get the current thermostat """
        self.find_thermostat_interface().set_target_temperature(v, wait)
        return self

    @property
    def reduced_temperature(self):
        """ Get the current thermostat offset """
        return self.find_thermostat_interface().reduced_temperature

    def set_reduced_temperature(self, v, wait=False):
        """ Get the current thermostat """
        self.find_thermostat_interface().set_reduced_temperature(v, wait)
        return self

    @property
    def comfort_temperature(self):
        return self.find_thermostat_interface().comfort_temperature

    def set_comfort_temperature(self, v, wait=False):
        """ Get the current thermostat """
        self.find_thermostat_interface().set_comfort_temperature(v, wait)
        return self

    @property
    def eco_temperature(self):
        return self.reduced_temperature

    @property
    def adaptive_heating_active(self):
        return self.find_thermostat_interface().adaptive_heating_active

    @property
    def adaptive_heating_running(self):
        return self.find_thermostat_interface().adaptive_heating_running

    @property
    def holiday_active(self):
        return self.find_thermostat_interface().holiday_active

    @property
    def summer_active(self):
        return self.find_thermostat_interface().summer_active

    @property
    def window_open(self):
        return self.find_thermostat_interface().window_open

    @property
    def window_open_endtime(self):
        return self.find_thermostat_interface().window_open_endtime

    @property
    def boost_active(self):
        return self.find_thermostat_interface().boost_active

    @property
    def boost_active_endtime(self):
        return self.find_thermostat_interface().boost_active_endtime

    def set_boost_mode(self, seconds, wait=False):
        """Set the thermostate into boost mode."""
        self.find_thermostat_interface().set_boost_mode(seconds)
        return self

    def set_window_open(self, seconds, wait=False):
        """Set the thermostate in open window mode."""
        self.find_thermostat_interface().set_window_open(seconds)
        return self

    def get_hkr_state(self):
        """Get the thermostate state."""
        mode = self.find_thermostat_interface().thermostat_mode
        if mode in ["on", "off"]:
            return mode
        elif self.target_temperature == self.eco_temperature:
            return "eco"
        elif self.target_temperature == self.comfort_temperature:
            return "comfort"
        return "manual"

    def set_hkr_state(self, state, wait=False):
        """Set the state of the thermostat.

        Possible values for state are: 'on', 'off', 'comfort', 'eco'.
        """
        if state in ["on", "off"]:
            self.find_thermostat_interface().set_thermostat_mode(state, wait)
        elif state == "eco":
            self.find_thermostat_interface().set_target_temperature(self.eco_temperature, wait)
        elif state == "comfort":
            self.find_thermostat_interface().set_target_temperature(self.comfort_temperature, wait)
        return self
