"""The base device class."""
# -*- coding: utf-8 -*-

from __future__ import print_function

import logging

from .fritzhomeentitybase import FritzhomeEntityBase
from .. import interfaces

_LOGGER = logging.getLogger(__name__)


class FritzhomeUnitBase(FritzhomeEntityBase):
    """The Fritzhome Device class."""

    def __init__(self, fritz=None, node=None):
        super().__init__(fritz, node)
        interfaces = {}

    def __repr__(self):
        """Return a string."""
        return f"{self.ain} of device {self.parent}"

    def fetch(self):
        """Update the device values."""
        # TODO: update specific unit (targeted REST endpoint)
        self._fritz.update_units()

    def _update_from_node(self, node):
        super()._update_from_node(node)
        _LOGGER.debug("update unit base")
        if self.ain != node["ain"]:
            raise ValueError

        # unshare class attribute on write
        self.interfaces = {}
        for iface, node in node["interfaces"].items():
            self.interfaces[iface] = interfaces.FritzhomeInterface(self, iface, node)

    def units(self):
        return [self]

    def update(self):
        pass

    @property
    def parent(self):
        return self._node["parentUid"]

    @property
    def device(self):
        return self._node["deviceUid"]

    @property
    def is_connected(self):
        return self._node["isConnected"]

    @property
    def is_group(self):
        return self._node["isGroupUnit"]

    @property
    def statistics(self):
        return self._node["statistics"]

    @property
    def unit_type(self):
        return self._node["unitType"]

    # General
    def get_present(self):
        """Check if the unit is present."""
        return self.is_connected
