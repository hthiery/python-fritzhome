"""The feature list class."""
from enum import IntFlag


class FritzhomeDeviceFeatures(IntFlag):
    """The feature list class."""

    HANFUN_DEVICE = 0x0001  # bit 0
    LIGHTBULB = 0x0004  # bit 2
    ALARM = 0x0010  # bit 4
    BUTTON = 0x0020  # bit 5
    THERMOSTAT = 0x0040  # bit 6
    POWER_METER = 0x0080  # bit 7
    TEMPERATURE = 0x0100  # bit 8
    SWITCH = 0x0200  # bit 9
    DECT_REPEATER = 0x0400  # bit 10
    MICROPHONE = 0x0800  # bit 11
    HANFUN_UNIT = 0x2000  # bit 13
    SWITCHABLE = 0x8000  # bit 15
    LEVEL = 0x10000  # bit 16
    COLOR = 0x20000  # bit 17
    BLIND = 0x40000  # bit 18
    HUMIDITY = 0x100000  # bit 20
