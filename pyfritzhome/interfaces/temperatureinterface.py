"""The powermeter device class."""
# -*- coding: utf-8 -*-

import logging

from .interfacebase import FritzhomeInterfaceBase

_LOGGER = logging.getLogger(__name__)


class FritzhomeTemperatureInterface(FritzhomeInterfaceBase):
    """The Fritzhome Device class."""

    celsius = None
    offset = None

    @property
    def is_temperature(self):
        return self.type == "temperatureInterface"

    def _update_from_node(self, node):
        _LOGGER.debug("update switch device")
        super()._update_from_node(node)
        if self.is_temperature:
            if self._node["state"] != "valid":
                _LOGGER.warning("interface state not valid")
            else:
                self.celsius = self._node["celsius"]
                # offset is not always exposed (for Thermo 302 the offset is in the thermostatInterface)
                self.offset = self._node.get("offset") or 0.0



class FritzhomeTemperatureMixin():
    """The Fritzhome Temperature mixin."""

    def find_temperature_interface(self):
        return self.find_interface("temperatureInterface")

    @property
    def has_temperature_sensor(self):
        """Check if the device has temperature sensors."""
        return self.find_temperature_interface() != None

    @property
    def temperature(self):
        """ Get the current temperature """
        self.find_temperature_interface().celsius

    @property
    def actual_temperature(self):
        """ Get the current temperature (legacy) """
        self.find_temperature_interface().celsius

    @property
    def offset(self):
        """ Get the current temperature offset """
        self.find_temperature_interface().offset
