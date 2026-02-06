"""Init file for the device types."""

from .fritzhomeunit import FritzhomeUnit
from .fritzhometemplate import FritzhomeTemplate
from .fritzhometrigger import FritzhomeTrigger
from .fritzhomedevicebase import FritzhomeDeviceBase
from .fritzhomeinterface import FritzhomeInterface
from .fritzhomeonoffinterface import *

__all__ = (
    "FritzhomeUnit",
    "FritzhomeTemplate",
    "FritzhomeTrigger",
    "FritzhomeInterface",
    "FritzhomeOnOffInterface", "FritzhomeOnOffMixin",
)
