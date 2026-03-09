"""The switch device class."""
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
        if self._has_feature(FritzhomeDeviceFeatures.SWITCH):
            # for AVM plugs like FRITZ!DECT 200 and FRITZ!DECT 210
            return True
        if self._has_feature(
            FritzhomeDeviceFeatures.SWITCHABLE
        ) and not self._has_feature(FritzhomeDeviceFeatures.LIGHTBULB):
            # for HAN-FUN plugs
            return True
        return False

    def _update_switch_from_node(self, node):
        _LOGGER.debug("update switch device")
        if self._has_feature(FritzhomeDeviceFeatures.SWITCH):
            val = node.find("switch")
            try:
                self.switch_state = self.get_node_value_as_int_as_bool(val, "state")
            except Exception:
                self.switch_state = None
            self.switch_mode = self.get_node_value(val, "mode")
            try:
                self.lock = self.get_node_value_as_int_as_bool(val, "lock")
            except Exception:
                self.lock = None

            # optional value
            try:
                self.device_lock = self.get_node_value_as_int_as_bool(val, "devicelock")
            except Exception:
                pass
        else:
            val = node.find("simpleonoff")
            try:
                self.switch_state = self.get_node_value_as_int_as_bool(val, "state")
            except Exception:
                self.switch_state = None

    def get_switch_state(self):
        """Get the switch state."""
        return self._fritz.get_switch_state(self.ain)

    def set_switch_state_on(self, wait=False):
        """Set the switch state to on."""
        return self._fritz.set_switch_state_on(self.ain, wait)

    def set_switch_state_off(self, wait=False):
        """Set the switch state to off."""
        return self._fritz.set_switch_state_off(self.ain, wait)

    def set_switch_state_toggle(self, wait=False):
        """Toggle the switch state."""
        return self._fritz.set_switch_state_toggle(self.ain, wait)
