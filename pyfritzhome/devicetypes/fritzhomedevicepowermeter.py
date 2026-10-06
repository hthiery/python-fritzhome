"""The powermeter device class."""

from __future__ import annotations

import logging

from xml.etree import ElementTree

from .fritzhomedevicebase import FritzhomeDeviceBase
from .fritzhomedevicefeatures import FritzhomeDeviceFeatures

_LOGGER = logging.getLogger(__name__)


class FritzhomeDevicePowermeter(FritzhomeDeviceBase):
    """The Fritzhome Device class."""

    power: int | None = None
    energy: int | None = None
    voltage: int | None = None
    current: float | None = None

    def _update_from_node(self, node: ElementTree.Element) -> None:
        super()._update_from_node(node)
        if self.present is False:
            return

        if self.has_powermeter:
            self._update_powermeter_from_node(node)

    # Power Meter
    @property
    def has_powermeter(self) -> bool:
        """Check if the device has powermeter function."""
        return self._has_feature(FritzhomeDeviceFeatures.POWER_METER)

    def _update_powermeter_from_node(self, node: ElementTree.Element) -> None:
        _LOGGER.debug("update powermeter device")
        val = node.find("powermeter")
        if val is None:
            return

        try:
            power = val.findtext("power")
            if power is not None:
                self.power = int(power)
        except Exception:
            pass

        try:
            energy = val.findtext("energy")
            if energy is not None:
                self.energy = int(energy)
        except Exception:
            pass

        try:
            voltage = val.findtext("voltage")
            if voltage is not None:
                self.voltage = int(voltage)
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

    def get_switch_power(self) -> int:
        """Get the switch state."""
        return self._fritz.get_switch_power(self.ain)

    def get_switch_energy(self) -> int:
        """Get the switch energy."""
        return self._fritz.get_switch_energy(self.ain)
