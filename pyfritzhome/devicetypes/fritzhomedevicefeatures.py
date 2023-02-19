"""The feature list class."""
from enum import IntFlag


class FritzhomeDeviceFeatures(IntFlag):
    """The feature list class."""

    LIGHTBULB = 0x0004
    ALARM = 0x0010
    UNKNOWN = 0x0020
    BUTTON = 0x0020
    THERMOSTAT = 0x0040
    POWER_METER = 0x0080
    TEMPERATURE = 0x0100
    SWITCH = 0x0200
    DECT_REPEATER = 0x0400
    MICROPHONE = 0x0800
    HANFUN = 0x2000
    SWITCHABLE = 0x8000
    LEVEL = 0x10000
    COLOR = 0x20000
    BLIND = 0x40000
