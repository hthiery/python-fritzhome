"""Toplevel device for pyfritzhome."""

from typing import Optional, TYPE_CHECKING
from xml.etree import ElementTree

from .devicetypes import FritzhomeTemplate  # noqa: F401
from .devicetypes import FritzhomeTrigger  # noqa: F401
from .devicetypes import (
    FritzhomeDeviceAlarm,
    FritzhomeDeviceBlind,
    FritzhomeDeviceButton,
    FritzhomeDeviceHumidity,
    FritzhomeDeviceLevel,
    FritzhomeDeviceLightBulb,
    FritzhomeDevicePowermeter,
    FritzhomeDeviceRepeater,
    FritzhomeDeviceSwitch,
    FritzhomeDeviceTemperature,
    FritzhomeDeviceThermostat,
)

if TYPE_CHECKING:
    from .fritzhome import Fritzhome


class FritzhomeDevice(
    FritzhomeDeviceAlarm,
    FritzhomeDeviceBlind,
    FritzhomeDeviceButton,
    FritzhomeDeviceHumidity,
    FritzhomeDeviceLevel,
    FritzhomeDeviceLightBulb,
    FritzhomeDevicePowermeter,
    FritzhomeDeviceRepeater,
    FritzhomeDeviceSwitch,
    FritzhomeDeviceTemperature,
    FritzhomeDeviceThermostat,
):
    """The Fritzhome Device class."""

    def __init__(
        self,
        fritz: Optional["Fritzhome"] = None,
        node: Optional[ElementTree.Element] = None,
    ) -> None:
        """Create a device object."""
        super().__init__(fritz, node)

    def _update_from_node(self, node: ElementTree.Element) -> None:
        super()._update_from_node(node)
