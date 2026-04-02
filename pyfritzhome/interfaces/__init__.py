"""Init file for the device types."""

__all__ = (
    "FritzhomeInterface",
    "FritzhomeOnOffInterface", "FritzhomeOnOffMixin",
    "FritzhomeMultimeterInterface", "FritzhomeMultimeterMixin",
    "FritzhomeTemperatureInterface", "FritzhomeTemperatureMixin",
    "FritzhomeHumidityInterface", "FritzhomeHumidityMixin",
    "FritzhomeThermostatInterface", "FritzhomeThermostatMixin",
)

from .interface import FritzhomeInterface
from .onoffinterface import FritzhomeOnOffInterface, FritzhomeOnOffMixin
from .multimeterinterface import FritzhomeMultimeterInterface, FritzhomeMultimeterMixin
from .temperatureinterface import FritzhomeTemperatureInterface, FritzhomeTemperatureMixin
from .humidityinterface import FritzhomeHumidityInterface, FritzhomeHumidityMixin
from .thermostatinterface import FritzhomeThermostatInterface, FritzhomeThermostatMixin
