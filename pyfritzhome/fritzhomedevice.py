"""Toplevel device for pyfritzhome."""

# -*- coding: utf-8 -*-

from .devicetypes import FritzhomeUnit  # noqa: F401
from .devicetypes import FritzhomeTemplate  # noqa: F401
from .devicetypes import FritzhomeTrigger  # noqa: F401
from .devicetypes import FritzhomeDeviceBase
from .devicetypes import FritzhomeOnOffMixin
from .devicetypes import FritzhomeMultimeterMixin
from .devicetypes import FritzhomeTemperatureMixin

class FritzhomeDevice(
    FritzhomeDeviceBase,
    FritzhomeOnOffMixin,
    FritzhomeMultimeterMixin,
    FritzhomeTemperatureMixin,
):
    """The Fritzhome Device class."""

    def __init__(self, fritz=None, node=None):
        """Create a device object."""
        super().__init__(fritz, node)

    def _update_from_node(self, node):
        super()._update_from_node(node)
