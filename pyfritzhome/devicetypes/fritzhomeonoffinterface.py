"""The switch device class."""
# -*- coding: utf-8 -*-

import logging

from .fritzhomeinterfacebase import FritzhomeInterfaceBase

_LOGGER = logging.getLogger(__name__)


class FritzhomeOnOffInterface(FritzhomeInterfaceBase):
    """The Fritzhome OnOff interface class."""

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
        self._node["active"] = True

    def set_switch_state_off(self, wait=False):
        self._node["active"] = False

    def set_switch_state_toggle(self, wait=False):
        self._node["active"] = not self._node["active"]


class FritzhomeOnOffMixin():

    def find_switch_interface(self):
        #~ return next((unit for unit in self._units if unit.is_switch), None)
        for unit in self.units():
            if interface := unit.interfaces.get("onOffInterface"):
                return (unit, interface)
        return None

    @property
    def has_switch(self):
        return self.find_switch_interface() != None

    @property
    def switch_state(self):
        """ Get the current switch state """
        if pair := self.find_switch_interface():
            return pair[1].switch_state

    def set_switch_state_on(self):
        """Set the switch state to on."""
        if pair := self.find_switch_interface():
            pair[1].set_switch_state_on()
            pair[0].update()

    def set_switch_state_off(self):
        """Set the switch state to off."""
        if pair := self.find_switch_interface():
            pair[1].set_switch_state_off()
            pair[0].update()

    def set_switch_state_toggle(self):
        """Toggle the switch state."""
        if pair := self.find_switch_interface():
            pair[1].set_switch_state_toggle()
            pair[0].update()

