"""The base device class."""
# -*- coding: utf-8 -*-

from __future__ import print_function


import logging

from pyfritzhome.devicetypes.fritzhomeentitybase import FritzhomeEntityBase

_LOGGER = logging.getLogger(__name__)


class FritzhomeDeviceBase(FritzhomeEntityBase):
    """The Fritzhome Device class."""

    def __init__(self, fritz=None, node=None):
        super().__init__(fritz, node)
        self._units = {}

    def __repr__(self):
        """Return a string."""
        return "{ain} {manuf} {prod} {name}".format(
            ain=self.ain,
            manuf=self.manufacturer,
            prod=self.productname,
            name=self.name,
        )

    def update(self):
        """Update the device values."""
        self._fritz.update_device()

    def _update_from_node(self, node):
        _LOGGER.debug("update base device")
        super()._update_from_node(node)

    def get_config():
        self._fritz.update_device_config(self.ain)

    @property
    def uid(self):
        return self._node["UID"]

    @property
    def manufacturer(self):
        return self._node["manufacturer"]

    @property
    def product_name(self):
        return self._node["productName"]

    # legacy
    @property
    def productname(self):
        return self.product_name

    # legacy
    @property
    def is_connected(self):
        return self._node["isConnected"]

    # legacy
    @property
    def present(self):
        return self.is_connected

    def clear_units(self):
        self._units = {}

    def add_or_update_unit(self, unit):
        self._units[unit.ain] = unit

    def units(self):
        return self._units.values()
