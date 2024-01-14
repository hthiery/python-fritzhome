"""The powermeter device class."""
# -*- coding: utf-8 -*-

import logging

from .fritzhomedevicebase import FritzhomeDeviceBase
from .fritzhomedevicefeatures import FritzhomeDeviceFeatures

_LOGGER = logging.getLogger(__name__)


class FritzhomeDevicePowermeter(FritzhomeDeviceBase):
    """The Fritzhome Device class."""

    power = None
    energy = None
    voltage = None
    current = None

    def _update_from_node(self, node):
        super()._update_from_node(node)
        if self.present is False:
            return

        if self.has_powermeter:
            self._update_powermeter_from_node(node)

    # Power Meter
    @property
    def has_powermeter(self):
        """Check if the device has powermeter function."""
        return self._has_feature(FritzhomeDeviceFeatures.POWER_METER)

    def _update_powermeter_from_node(self, node):
        _LOGGER.debug("update powermeter device")
        val = node.find("powermeter")
        self.power = int(val.findtext("power"))
        self.energy = int(val.findtext("energy"))
        try:
            self.voltage = int(val.findtext("voltage"))
        except Exception:
            pass

        if (
            isinstance(self.power, int)
            and isinstance(self.voltage, int)
            and self.voltage > 0
        ):
            self.current = self.power / self.voltage * 1000
        else:
            self.current = None

    def get_switch_power(self):
        """Get the switch state."""
        return self._fritz.get_switch_power(self.ain)

    def get_switch_energy(self):
        """Get the switch energy."""
        return self._fritz.get_switch_energy(self.ain)
