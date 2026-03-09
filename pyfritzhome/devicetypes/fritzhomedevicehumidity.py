"""The humidity device class."""
# -*- coding: utf-8 -*-

import logging

from .fritzhomedevicebase import FritzhomeDeviceBase
from .fritzhomedevicefeatures import FritzhomeDeviceFeatures

_LOGGER = logging.getLogger(__name__)


class FritzhomeDeviceHumidity(FritzhomeDeviceBase):
    """The Fritzhome Device class."""

    rel_humidity = None

    def _update_from_node(self, node):
        super()._update_from_node(node)
        if self.present is False:
            return

        if self.has_humidity_sensor:
            self._update_humidity_from_node(node)

    # Humidity
    @property
    def has_humidity_sensor(self):
        """Check if the device has humidity function."""
        return self._has_feature(FritzhomeDeviceFeatures.HUMIDITY)

    def _update_humidity_from_node(self, node):
        _LOGGER.debug("update humidity device")
        humidity_element = node.find("humidity")
        try:
            self.rel_humidity = self.get_node_value_as_int(
                humidity_element, "rel_humidity"
            )
        except ValueError:
            pass
