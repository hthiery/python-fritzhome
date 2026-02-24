"""Init file for the device types."""

from .fritzhomeunit import FritzhomeUnit
from .fritzhometemplate import FritzhomeTemplate
from .fritzhometrigger import FritzhomeTrigger
from .fritzhomedevicebase import FritzhomeDeviceBase

__all__ = (
    "FritzhomeUnit",
    "FritzhomeTemplate",
    "FritzhomeTrigger",
)
