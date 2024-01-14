"""The alarm device class."""
# -*- coding: utf-8 -*-

import logging

from .fritzhomedevicebase import FritzhomeDeviceBase
from .fritzhomedevicefeatures import FritzhomeDeviceFeatures

_LOGGER = logging.getLogger(__name__)


class FritzhomeDeviceAlarm(FritzhomeDeviceBase):
    """The Fritzhome Device class."""

    alert_state = None

    def _update_from_node(self, node):
        super()._update_from_node(node)
        if self.present is False:
            return

        if self.has_alarm:
            self._update_alarm_from_node(node)

    # Alarm
    @property
    def has_alarm(self):
        """Check if the device has alarm function."""
        return self._has_feature(FritzhomeDeviceFeatures.ALARM)

    def _update_alarm_from_node(self, node):
        _LOGGER.debug("update alert device")
        val = node.find("alert")
        try:
            self.alert_state = self.get_node_value_as_int_as_bool(val, "state")
        except (Exception, ValueError):
            self.alert_state = None
