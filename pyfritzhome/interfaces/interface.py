"""The entity base class."""

# -*- coding: utf-8 -*-

from __future__ import print_function
from abc import ABC


import logging
import json

from .interfacebase import FritzhomeInterfaceBase
from .onoffinterface import FritzhomeOnOffInterface
from .multimeterinterface import FritzhomeMultimeterInterface
from .temperatureinterface import FritzhomeTemperatureInterface
from .humidityinterface import FritzhomeHumidityInterface
from .thermostatinterface import FritzhomeThermostatInterface

_LOGGER = logging.getLogger(__name__)

class FritzhomeInterface():
    """The Fritzhome Interface factory."""

    @staticmethod
    def create(unit, type, node = None):
        """Create a specific interface object."""
        cls = {
            "onOffInterface":       FritzhomeOnOffInterface,
            "multimeterInterface":  FritzhomeMultimeterInterface,
            "temperatureInterface": FritzhomeTemperatureInterface,
            "humidityInterface":    FritzhomeHumidityInterface,
            "thermostatInterface" : FritzhomeThermostatInterface,
        }
        try:
            return cls[type](unit, type, node)
        except KeyError:
            return FritzhomeInterfaceBase(unit, type, node)

