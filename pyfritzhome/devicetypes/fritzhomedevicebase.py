"""The base device class."""
# -*- coding: utf-8 -*-

from __future__ import print_function

import logging

from pyfritzhome.devicetypes.fritzhomeentitybase import FritzhomeEntityBase

_LOGGER = logging.getLogger(__name__)


class FritzhomeDeviceBase(FritzhomeEntityBase):
    """The Fritzhome Device class."""

    manufacturer = None
    product_name = None
    is_connected = None

    def __repr__(self):
        """Return a string."""
        return "{ain} {manuf} {prod} {name}".format(
            ain=self.ain,
            manuf=self.manufacturer,
            prod=self.productname,
            name=self.name,
        )

    def _update_from_node(self, node):
        _LOGGER.debug("update base device")
        super()._update_from_node(node)
        self._units = {}
        if self._fritz._use_aha:
            self.manufacturer = node.attrib["manufacturer"]
            self.product_name = node.attrib["productname"]
            self.is_connected = self.get_node_value_as_int_as_bool(node, "present")
        else:
            self.manufacturer = self._node["manufacturer"]
            self.product_name = self._node["productName"]
            self.is_connected = self._node["isConnected"]

    def find_interface(self, interface):
        for unit in self._units.values():
            if interface := unit.find_interface(interface):
                return interface
        return None

    def get_config():
        self._fritz.update_device_config(self.ain)

    # legacy
    @property
    def productname(self):
        return self.product_name

    # legacy
    @property
    def present(self):
        return self.is_connected

    def clear_units(self):
        self._units = {}

    def add_or_update_unit(self, unit):
        self._units[unit.ain] = unit

    # with aha, there are no units and interfaces. Emulated interfaces become directly attached
    def add_or_update_unit(self, unit):
        self._units[unit.ain] = unit

    def units(self):
        return self._units.values()
