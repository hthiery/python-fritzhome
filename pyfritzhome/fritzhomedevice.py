"""Toplevel device for pyfritzhome."""

# -*- coding: utf-8 -*-

from .devicetypes import FritzhomeTemplate  # noqa: F401
from .devicetypes import (
    FritzhomeDeviceAlarm,
    FritzhomeDeviceBlind,
    FritzhomeDeviceButton,
    FritzhomeDeviceLightBulb,
    FritzhomeDevicePowermeter,
    FritzhomeDeviceRepeater,
    FritzhomeDeviceSwitch,
    FritzhomeDeviceTemperature,
    FritzhomeDeviceThermostat,
)


class FritzhomeDevice(
    FritzhomeDeviceAlarm,
    FritzhomeDeviceButton,
    FritzhomeDevicePowermeter,
    FritzhomeDeviceRepeater,
    FritzhomeDeviceSwitch,
    FritzhomeDeviceTemperature,
    FritzhomeDeviceThermostat,
    FritzhomeDeviceLightBulb,
    FritzhomeDeviceBlind,
):
    """The Fritzhome Device class."""

    def __init__(self, fritz=None, node=None):
        """Create a device object."""
        super().__init__(fritz, node)

    def _update_from_node(self, node):
        super()._update_from_node(node)
