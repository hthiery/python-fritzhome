"""The base device class."""
# -*- coding: utf-8 -*-

from __future__ import print_function

import logging

from .fritzhomeunitbase import FritzhomeUnitBase
from .. import interfaces

_LOGGER = logging.getLogger(__name__)

class FritzhomeUnit(FritzhomeUnitBase,
                    interfaces.FritzhomeOnOffMixin,
                    interfaces.FritzhomeMultimeterMixin,
                    interfaces.FritzhomeTemperatureMixin,
                    interfaces.FritzhomeHumidityMixin):
    """The Fritzhome Device class."""

    def __init__(self, fritz=None, node=None):
        """Create a device object."""
        super().__init__(fritz, node)

    def _update_from_node(self, node):
        super()._update_from_node(node)
