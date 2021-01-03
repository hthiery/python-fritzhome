# -*- coding: utf-8 -*-

from .devicetypes import (
    FritzhomeDeviceAlarm,
    FritzhomeDeviceButton,
    FritzhomeDevicePowermeter,
    FritzhomeDeviceRepeater,
    FritzhomeDeviceSwitch,
    FritzhomeDeviceTemperature,
    FritzhomeDeviceThermostat,
    FritzhomeDeviceLightBulb,
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
):
    """The Fritzhome Device class."""

    def __init__(self, fritz=None, node=None):
        super().__init__(fritz, node)

    def _update_from_node(self, node):
        super()._update_from_node(node)
