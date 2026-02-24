"""Init file for the device types."""

__all__ = (
    "FritzhomeInterface",
    "FritzhomeOnOffInterface", "FritzhomeOnOffMixin",
    "FritzhomeMultimeterInterface", "FritzhomeMultimeterMixin",
    "FritzhomeTemperatureInterface", "FritzhomeTemperatureMixin",
)

from .interface import FritzhomeInterface
from .onoffinterface import FritzhomeOnOffInterface, FritzhomeOnOffMixin
from .multimeterinterface import FritzhomeMultimeterInterface, FritzhomeMultimeterMixin
from .temperatureinterface import FritzhomeTemperatureInterface, FritzhomeTemperatureMixin
