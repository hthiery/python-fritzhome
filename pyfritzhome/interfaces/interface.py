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

_LOGGER = logging.getLogger(__name__)

class FritzhomeInterface(FritzhomeOnOffInterface,
                         FritzhomeMultimeterInterface,
                         FritzhomeTemperatureInterface,
                         FritzhomeHumidityInterface):
    """The Fritzhome Interface class."""

    def __init__(self, unit, type, node = None):
        """Create an entity base object."""
        super().__init__(unit, type, node)

    # interfaces are not entities, only their parent units are, therefore this is
    # called with the unit REST node
    def _update_from_node(self, node):
        super()._update_from_node(node)
