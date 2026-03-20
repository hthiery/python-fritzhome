"""The powermeter device class."""
# -*- coding: utf-8 -*-

import logging

from .interfacebase import FritzhomeInterfaceBase

_LOGGER = logging.getLogger(__name__)


class FritzhomeMultimeterInterface(FritzhomeInterfaceBase):
    """The Fritzhome Device class."""

    power = None
    energy = None
    voltage = None
    current = None

    @property
    def is_powermeter(self):
        return self.type == "multimeterInterface"

    def _update_from_node(self, node):
        _LOGGER.debug("update switch device")
        super()._update_from_node(node)
        if self.is_powermeter:
            if self._node["state"] != "valid":
                _LOGGER.warning("interface state not valid")
            else:
                self.power = self._node["power"]
                self.energy = self._node["energy"]
                self.voltage = self._node["voltage"]
                self.current = self._node["current"]



class FritzhomeMultimeterMixin():
    """The Fritzhome Multimeter mixin."""

    def find_multimeter_interface(self):
        return self.find_interface("multimeterInterface")

    @property
    def has_powermeter(self):
        """Check if the device has powermeter sensors."""
        return self.find_multimeter_interface() != None

    @property
    def power(self):
        """ Get the current powermeter power """
        return self.find_multimeter_interface().power

    @property
    def energy(self):
        """ Get the current currentmeter energy """
        return self.find_multimeter_interface().energy

    @property
    def voltage(self):
        """ Get the current voltagemeter voltage """
        return self.find_multimeter_interface().voltage

    @property
    def current(self):
        """ Get the current currentmeter current """
        return self.find_multimeter_interface().current


