# -*- coding: utf-8 -*-

import logging

from .fritzhomedevicebase import FritzhomeDeviceBase
from .fritzhomedevicefeatures import FritzhomeDeviceFeatures

_LOGGER = logging.getLogger(__name__)


class FritzhomeDeviceSwitch(FritzhomeDeviceBase):
    """The Fritzhome Device class."""

    switch_state = None
    switch_mode = None
    lock = None

    def _update_from_node(self, node):
        super()._update_from_node(node)
        if self.present is False:
            return

        if self.has_switch:
            self._update_switch_from_node(node)

    # Switch
    @property
    def has_switch(self):
        """Check if the device has switch function."""
        return self._has_feature(FritzhomeDeviceFeatures.SWITCH)

    def _update_switch_from_node(self, node):
        val = node.find("switch")
        self.switch_state = self.get_node_value_as_int_as_bool(val, "state")
        self.switch_mode = self.get_node_value(val, "mode")
        self.lock = bool(self.get_node_value(val, "lock"))
        # optional value
        try:
            self.device_lock = self.get_node_value_as_int_as_bool(val, "devicelock")
        except Exception:
            pass

    def get_switch_state(self):
        """Get the switch state."""
        return self._fritz.get_switch_state(self.ain)

    def set_switch_state_on(self):
        """Set the switch state to on."""
        return self._fritz.set_switch_state_on(self.ain)

    def set_switch_state_off(self):
        """Set the switch state to off."""
        return self._fritz.set_switch_state_off(self.ain)

    def set_switch_state_toggle(self):
        """Toggle the switch state."""
        return self._fritz.set_switch_state_toggle(self.ain)
