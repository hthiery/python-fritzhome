"""The repeater device class."""
# -*- coding: utf-8 -*-

import logging

from .fritzhomedevicebase import FritzhomeDeviceBase
from .fritzhomedevicefeatures import FritzhomeDeviceFeatures

_LOGGER = logging.getLogger(__name__)


class FritzhomeDeviceRepeater(FritzhomeDeviceBase):
    """The Fritzhome Device class."""

    def _update_from_node(self, node):
        super()._update_from_node(node)
        if self.present is False:
            return

    # Repeater
    @property
    def has_repeater(self):
        """Check if the device has repeater function."""
        return self._has_feature(FritzhomeDeviceFeatures.DECT_REPEATER)
