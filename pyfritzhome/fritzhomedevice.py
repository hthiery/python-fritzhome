"""Toplevel device for pyfritzhome."""

# -*- coding: utf-8 -*-

from .devicetypes import *
from .interfaces import *

class FritzhomeDeviceAHA(
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

    def __init__(self, fritz=None, node=None):
        """Create a device object."""
        super().__init__(fritz, node)

    def _update_from_node(self, node):
        super()._update_from_node(node)

class FritzhomeDeviceREST(
    FritzhomeDeviceBase,
    FritzhomeOnOffMixin,
    FritzhomeMultimeterMixin,
    FritzhomeTemperatureMixin,
    FritzhomeHumidityMixin,
):
    """The Fritzhome Device class."""

    def __init__(self, fritz=None, node=None):
        """Create a device object."""
        super().__init__(fritz, node)

    def _update_from_node(self, node):
        super()._update_from_node(node)

FritzhomeDevice = None

def __get_defice_class(base):
    class FritzhomeDevice(base):
        pass
    return FritzhomeDevice

def get_device_class(is_aha):
    global FritzhomeDevice
    if is_aha:
        FritzhomeDevice = __get_defice_class(FritzhomeDeviceAHA)
    else:
        FritzhomeDevice = __get_defice_class(FritzhomeDeviceREST)
    return FritzhomeDevice
