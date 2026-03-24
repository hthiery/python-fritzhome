"""The powermeter device class."""
# -*- coding: utf-8 -*-

import logging

from .interfacebase import FritzhomeInterfaceBase

_LOGGER = logging.getLogger(__name__)


class FritzhomeTemperatureInterface(FritzhomeInterfaceBase):
    """The Fritzhome Temperature interface class."""

    @property
    def celsius(self):
        return self._node["celsius"]

    @property
    def offset(self):
        # offset is not always exposed (only through /smarthome/configuration/… endpoints)
        return self._node.get("offset")

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
        return self.find_temperature_interface().celsius

    @property
    def actual_temperature(self):
        """ Get the current temperature (legacy) """
        return self.temperature

    @property
    def offset(self):
        """ Get the current temperature offset (maybe None!) """
        return self.find_temperature_interface().offset
