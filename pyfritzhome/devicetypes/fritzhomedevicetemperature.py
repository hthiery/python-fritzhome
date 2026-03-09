"""The temperature device class."""
# -*- coding: utf-8 -*-

import logging

from .fritzhomedevicebase import FritzhomeDeviceBase
from .fritzhomedevicefeatures import FritzhomeDeviceFeatures

_LOGGER = logging.getLogger(__name__)


class FritzhomeDeviceTemperature(FritzhomeDeviceBase):
    """The Fritzhome Device class."""

    offset = None
    temperature = None

    def _update_from_node(self, node):
        super()._update_from_node(node)
        if self.present is False:
            return

        if self.has_temperature_sensor:
            self._update_temperature_from_node(node)

    # Temperature
    @property
    def has_temperature_sensor(self):
        """Check if the device has temperature function."""
        return self._has_feature(FritzhomeDeviceFeatures.TEMPERATURE)

    def _update_temperature_from_node(self, node):
        _LOGGER.debug("update temperature device")
        temperature_element = node.find("temperature")
        try:
            self.offset = (
                self.get_node_value_as_int(temperature_element, "offset") / 10.0
            )
        except ValueError:
            pass

        try:
            self.temperature = (
                self.get_node_value_as_int(temperature_element, "celsius") / 10.0
            )
        except ValueError:
            pass
