"""Init file for pyfritzhome."""

try:
    from importlib.metadata import version
    __version__ = version(__name__)
except ImportError:
    __version__ = "dev"

from .errors import InvalidError, LoginError, NotLoggedInError
from .fritzhome import Fritzhome
from .fritzhomedevice import FritzhomeDevice

__all__ = (
    "Fritzhome",
    "FritzhomeDevice",
    "InvalidError",
    "LoginError",
    "NotLoggedInError",
)
