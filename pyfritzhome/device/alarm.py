# -*- coding: utf-8 -*-

from __future__ import print_function

import logging
from .fritzhomedevicefeatures import FritzhomeDeviceFeatures
from .base import FritzhomeBaseDevice

_LOGGER = logging.getLogger(__name__)


class FritzhomeAlarmDevice(FritzhomeBaseDevice):
    """The Fritzhome Device class."""

    alert_state = None

    def _update_from_node(self, node):
        super()._update_from_node(node)

        if self.present is False:
            return

        if self.has_alarm:
            val = node.find("alert")
            try:
                self.alert_state = self.get_node_value_as_int_as_bool(val, "state")
            except (Exception, ValueError):
                pass

    @property
    def has_alarm(self):
        """Check if the device has alarm function."""
        return self._has_feature(FritzhomeDeviceFeatures.ALARM)
