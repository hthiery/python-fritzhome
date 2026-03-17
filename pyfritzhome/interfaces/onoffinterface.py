"""The switch device class."""
# -*- coding: utf-8 -*-

import logging

from .interfacebase import FritzhomeInterfaceBase

_LOGGER = logging.getLogger(__name__)


class FritzhomeOnOffInterface(FritzhomeInterfaceBase):
    """The Fritzhome OnOff interface class."""

    switch_state = None

    # Switch
    @property
    def is_switch(self):
        return self.type == "onOffInterface"

    def _update_from_node(self, node):
        _LOGGER.debug("update switch device")
        super()._update_from_node(node)
        if self.is_switch:
            if self._node["state"] != "valid":
                _LOGGER.warning("interface state not valid")
            else:
                self.switch_state = self._node["active"]

    def set_switch_state_on(self, wait=False):
        self._node_set["active"] = True
        self.changed(wait)

    def set_switch_state_off(self, wait=False):
        self._node_set["active"] = False
        self.changed(wait)

    def set_switch_state_toggle(self, wait=False):
        self._node_set["active"] = not self._node["active"]
        self.changed(wait)


class FritzhomeOnOffMixin():

    def find_switch_interface(self):
        return self.find_interface("onOffInterface")

    @property
    def has_switch(self):
        return self.find_switch_interface() != None

    @property
    def switch_state(self):
        """ Get the current switch state """
        return self.find_switch_interface().switch_state

    def set_switch_state_on(self, wait=False):
        """Set the switch state to on."""
        self.find_switch_interface().set_switch_state_on()
        return self

    def set_switch_state_off(self, wait=False):
        """Set the switch state to off."""
        self.find_switch_interface().set_switch_state_off()
        return self

    def set_switch_state_toggle(self, wait=False):
        """Toggle the switch state."""
        self.find_switch_interface().set_switch_state_toggle()
        return self

