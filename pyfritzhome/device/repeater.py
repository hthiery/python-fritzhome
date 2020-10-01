# -*- coding: utf-8 -*-

from __future__ import print_function

import logging
from .fritzhomedevicefeatures import FritzhomeDeviceFeatures
from .base import FritzhomeBaseDevice

_LOGGER = logging.getLogger(__name__)


class FritzhomeRepeaterDevice(FritzhomeBaseDevice):
    """The Fritzhome Device class."""

    alert_state = None

    def _update_from_node(self, node):
        super()._update_from_node(node)

        if self.present is False:
            return

    @property
    def has_repeater(self):
        """Check if the device has repeater function."""
        return self._has_feature(FritzhomeDeviceFeatures.DECT_REPEATER)
