"""Init file for the device types."""

from .fritzhomeunit import FritzhomeUnit
from .fritzhometemplate import FritzhomeTemplate
from .fritzhometrigger import FritzhomeTrigger
from .fritzhomedevicebase import FritzhomeDeviceBase
from .fritzhomeinterface import FritzhomeInterface
from .fritzhomeonoffinterface import *
from .fritzhomemultimeterinterface import *
from .fritzhometemperatureinterface import *

__all__ = (
    "FritzhomeUnit",
    "FritzhomeTemplate",
    "FritzhomeTrigger",
    "FritzhomeInterface",
    "FritzhomeOnOffInterface", "FritzhomeOnOffMixin",
    "FritzhomeMultimeterInterface", "FritzhomeMultimeterMixin",
    "FritzhomeTemperatureInterface", "FritzhomeTemperatureMixin",
)
