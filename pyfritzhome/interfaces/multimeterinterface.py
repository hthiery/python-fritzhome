"""The powermeter device class."""
# -*- coding: utf-8 -*-

import logging

from .interfacebase import FritzhomeInterfaceBase

_LOGGER = logging.getLogger(__name__)


class FritzhomeMultimeterInterface(FritzhomeInterfaceBase):
    """The Fritzhome Multimeter interface class."""

    @property
    def power(self):
        return self._node["power"]

    @property
    def energy(self):
        return self._node["energy"]

    @property
    def voltage(self):
        return self._node["voltage"]

    @property
    def current(self):
        return self._node["current"]



class FritzhomeMultimeterMixin():
    """The Fritzhome Multimeter mixin."""

    def find_multimeter_interface(self):
        return self.find_interface("multimeterInterface")

    @property
    def has_powermeter(self):
        """Check if the device has powermeter sensors."""
        return self.find_multimeter_interface() is not None

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


