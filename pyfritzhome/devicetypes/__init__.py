"""Init file for the device types."""

from .fritzhomedevicealarm import FritzhomeDeviceAlarm
from .fritzhomedevicebutton import FritzhomeDeviceButton
from .fritzhomedevicehumidity import FritzhomeDeviceHumidity
from .fritzhomedevicelevel import FritzhomeDeviceLevel
from .fritzhomedevicepowermeter import FritzhomeDevicePowermeter
from .fritzhomedevicerepeater import FritzhomeDeviceRepeater
from .fritzhomedeviceswitch import FritzhomeDeviceSwitch
from .fritzhomedevicetemperature import FritzhomeDeviceTemperature
from .fritzhomedevicethermostat import FritzhomeDeviceThermostat
from .fritzhomedevicelightbulb import FritzhomeDeviceLightBulb
from .fritzhomedeviceblind import FritzhomeDeviceBlind
from .fritzhometemplate import FritzhomeTemplate


__all__ = (
    "FritzhomeDeviceAlarm",
    "FritzhomeDeviceButton",
    "FritzhomeDeviceHumidity",
    "FritzhomeDeviceLevel",
    "FritzhomeDevicePowermeter",
    "FritzhomeDeviceRepeater",
    "FritzhomeDeviceSwitch",
    "FritzhomeDeviceTemperature",
    "FritzhomeDeviceThermostat",
    "FritzhomeDeviceLightBulb",
    "FritzhomeDeviceBlind",
    "FritzhomeTemplate",
)
