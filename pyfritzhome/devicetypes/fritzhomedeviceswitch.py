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
    simple_switch = None

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
        self.simple_switch = not self._has_feature(FritzhomeDeviceFeatures.SWITCH)
        self.simple_switch = self.simple_switch and self._has_feature(FritzhomeDeviceFeatures.SWITCHABLE)
        return (self._has_feature(FritzhomeDeviceFeatures.SWITCH) or self.simple_switch)

    def _update_switch_from_node(self, node):
        if not self.simple_switch :

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

        else :
            val = node.find("simpleonoff")
            try:
                self.switch_state = self.get_node_value_as_int_as_bool(val, "state")
            except ValueError:
                pass

    def get_switch_state(self):
        if not self.simple_switch :
            """Get the switch state."""
            return self._fritz.get_switch_state(self.ain)
        else :
            return self.switch_state

    def set_switch_state_on(self):
        if not self.simple_switch :
            """Set the switch state to on."""
            return self._fritz.set_switch_state_on(self.ain)
        else :
           self.switch_state = True
           self._fritz.set_state_on(self.ain)


    def set_switch_state_off(self):
        if not self.simple_switch :
            """Set the switch state to off."""
            return self._fritz.set_switch_state_off(self.ain)
        else :
            self.switch_state = True
            self._fritz.set_state_off(self.ain)

    def set_switch_state_toggle(self):
        if not self.simple_switch :
            """Toggle the switch state."""
            return self._fritz.set_switch_state_toggle(self.ain)
        else :
           self.switch_state = True
           self._fritz.set_state_toggle(self.ain)

