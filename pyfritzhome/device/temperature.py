# -*- coding: utf-8 -*-

from __future__ import print_function

import logging
from .fritzhomedevicefeatures import FritzhomeDeviceFeatures
from .base import FritzhomeBaseDevice

_LOGGER = logging.getLogger(__name__)


class FritzhomeTemperatureDevice(FritzhomeBaseDevice):
    """The Fritzhome Device class."""

    temperature = None

    def _update_from_node(self, node):
        super()._update_from_node(node)

        if self.present is False:
            return
        if self.has_temperature_sensor:
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

    @property
    def has_temperature_sensor(self):
        """Check if the device has temperature function."""
        return self._has_feature(FritzhomeDeviceFeatures.TEMPERATURE)
