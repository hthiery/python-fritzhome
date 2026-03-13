"""The base device class."""
# -*- coding: utf-8 -*-

from __future__ import print_function

import logging
import json

from pyfritzhome.devicetypes.fritzhomeentitybase import FritzhomeEntityBase

_LOGGER = logging.getLogger(__name__)


class FritzhomeDeviceBase(FritzhomeEntityBase):
    """The Fritzhome Device class."""

    manufacturer = None
    product_name = None
    fw_version   = None
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
        self._units = {}
        super()._update_from_node(node)
        if self._fritz._use_aha:
            self.manufacturer = node.attrib["manufacturer"]
            self.product_name = node.attrib["productname"]
            self.fw_version   = node.attrib["fwversion"]
            self.is_connected = self.get_node_value_as_int_as_bool(node, "present")
        else:
            self.manufacturer = self._node["manufacturer"]
            self.product_name = self._node["productName"]
            self.fw_version   = self._node["firmwareVersion"]
            self.is_connected = self._node["isConnected"]

    def update_unit(self, unit, node):
        """DOC-TODO (REST)"""
        assert unit.ain in self._units.keys(), "unknown unit to update"
        self._updates |= {"ain": self.ain, "units": node or unit._node}
        self._updates["units"] |= { "ain": unit.ain }
        if self.commit_now:
            self.trigger_update()

    def find_interface(self, interface):
        """DOC-TODO (REST)"""
        found = None
        for unit in self.units():
            if interface := unit.find_interface(interface):
                if found is None:
                    found = interface
                else:
                    _LOGGER.warning("ambigious device, multiple interface candidates, using first")
        return found

    def begin(self, unit_ain=None):
        """DOC-TODO (REST)"""
        if unit_ain:
            return self.units[unit_ain].begin()
        else:
            if len(self.units()) > 1:
                _LOGGER.warning("ambigious device, multiple units, using first")
            for unit in self._units.values():
                return unit.begin()

    def get_device_config():
        self._fritz.update_device_config(self.ain)

    def get_json(self):
        r = self._node.copy()
        r["units"] = {}
        for unit in self._node["unitUids"]:
            r["units"][unit] = self._units[unit]._node
        return json.dumps(r)

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

    @property
    def has_color(self):
        return False

    @property
    def has_blind(self):
        return False

    @property
    def has_alarm(self):
        return False

    @property
    def has_lightbulb(self):
        return False
    @property
    def holiday_active(self):
        return False
    @property
    def summer_active(self):
        return False
    @property
    def lock(self):
        return False
    @property
    def device_lock(self):
        return False

    @property
    def battery_level(self):
        return False

    @property
    def battery_low(self):
        return False

    @property
    def window_open(self):
        return False

    @property
    def nextchange_temperature(self):
        return False
    @property
    def nextchange_endperiod(self):
        return False
