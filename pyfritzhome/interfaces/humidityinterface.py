"""The powermeter device class."""
# -*- coding: utf-8 -*-

import logging

from .interfacebase import FritzhomeInterfaceBase

_LOGGER = logging.getLogger(__name__)


class FritzhomeHumidityInterface(FritzhomeInterfaceBase):
    """The Fritzhome Device class."""

    rel_humidity = None

    @property
    def is_humidity(self):
        return self.type == "humidityInterface"

    def _update_from_node(self, node):
        _LOGGER.debug("update switch device")
        super()._update_from_node(node)
        if self.is_humidity:
            if self._node["state"] != "valid":
                _LOGGER.warning("interface state not valid")
            else:
                self.rel_humidity = self._node["relativeHumidity"]



class FritzhomeHumidityMixin():
    """The Fritzhome Humidity mixin."""

    def find_humidity_interface(self):
        return self.find_interface("humidityInterface")

    @property
    def has_humidity_sensor(self):
        """Check if the device has humidity sensors."""
        return self.find_humidity_interface() != None

    @property
    def rel_humidity(self):
        """ Get the current humidity """
        return self.find_humidity_interface().rel_humidity
