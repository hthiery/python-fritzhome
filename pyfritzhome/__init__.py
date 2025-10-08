"""Init file for pyfritzhome."""

from importlib.metadata import version

from .errors import InvalidError, LoginError, NotLoggedInError
from .fritzhome import Fritzhome
from .fritzhomedevice import FritzhomeDevice

__version__ = version(__name__)

__all__ = (
    "Fritzhome",
    "FritzhomeDevice",
    "InvalidError",
    "LoginError",
    "NotLoggedInError",
)
