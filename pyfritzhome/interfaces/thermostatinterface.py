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
        _LOGGER.debug("update switch device")
        super()._update_from_node(node)

    @property
    def target_temperature(self):
        return self._node["setPointTemperature"]["celsius"]

    def set_target_temperature(self, v):
        self._node_set["setPointTemperature"] = {}
        self._node_set["setPointTemperature"]["celsius"] = v
        self._node_set["setPointTemperature"]["mode"] = "temperature"
        self.changed()

    @property
    def comfort_temperature(self):
        return self._node["comfortTemperature"]["celsius"]

    def set_comfort_temperature(self, v):
        self._node_set["comfortTemperature"]= {}
        self._node_set["comfortTemperature"]["celsius"] = v
        self._node_set["comfortTemperature"]["mode"] = "temperature"
        self.changed()

    @property
    def reduced_temperature(self):
        return self._node["reducedTemperature"]["celsius"]

    def set_reduced_temperature(self, v):
        self._node_set["reducedTemperature"]= {}
        self._node_set["reducedTemperature"]["celsius"] = v
        self._node_set["reducedTemperature"]["mode"] = "temperature"
        self.changed()

    def set_boost_mode(self, duration_secs):
        import time
        self._node_set["boost"] = {}
        self._node_set["boost"]["enabled"] = True
        self._node_set["boost"]["endTime"] = int(time.time() + duration_secs)
        self.changed()

    def set_window_open(self, duration_secs):
        import time
        self._node_set["windowOpenMode"] = {}
        self._node_set["windowOpenMode"]["enabled"] = True
        self._node_set["windowOpenMode"]["endTime"] = int(time.time() + duration_secs)
        self.changed()

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
        self.find_thermostat_interface().target_temperature

    def set_target_temperature(self, v):
        """ Get the current thermostat """
        self.find_thermostat_interface().set_target_temperature(v)
        return self

    @property
    def reduced_temperature(self):
        """ Get the current thermostat offset """
        self.find_thermostat_interface().reduced_temperature

    def set_reduced_temperature(self, v):
        """ Get the current thermostat """
        self.find_thermostat_interface().set_reduced_temperature(v)
        return self

    @property
    def comfort_temperature(self):
        self.find_thermostat_interface().comfort_temperature

    def set_comfort_temperature(self, v):
        """ Get the current thermostat """
        self.find_thermostat_interface().set_comfort_temperature(v)
        return self

    @property
    def eco_temperature(self):
        return self.reduced_temperature

    def set_boost_mode(self, seconds, wait=False):
        """Set the thermostate into boost mode."""
        self.find_thermostat_interface().set_boost_mode(seconds)
        return self

    def set_window_open(self, seconds, wait=False):
        """Set the thermostate in open window mode."""
        self.find_thermostat_interface().set_window_open(seconds)
        return self
