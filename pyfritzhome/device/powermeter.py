# -*- coding: utf-8 -*-

from __future__ import print_function

import logging
from .fritzhomedevicefeatures import FritzhomeDeviceFeatures
from .base import FritzhomeBaseDevice

_LOGGER = logging.getLogger(__name__)


class FritzhomePowermeterDevice(FritzhomeBaseDevice):
    """The Fritzhome Device class."""

    power = None
    energy = None
    voltage = None
    offset = None

    def _update_from_node(self, node):
        super()._update_from_node(node)

        if self.present is False:
            return

        if self.has_powermeter:
            val = node.find("powermeter")
            self.power = int(val.findtext("power"))
            self.energy = int(val.findtext("energy"))
            try:
                self.voltage = float(int(val.findtext("voltage")) / 1000)
            except Exception:
                pass

    @property
    def has_powermeter(self):
        """Check if the device has powermeter function."""
        return self._has_feature(FritzhomeDeviceFeatures.POWER_METER)

    def get_switch_power(self):
        """ the switch state."""
        return self._fritz.get_switch_power(self.ain)

    def get_switch_energy(self):
        """Get the switch energy."""
        return self._fritz.get_switch_energy(self.ain)
