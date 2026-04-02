"""The base device class."""
# -*- coding: utf-8 -*-

from __future__ import print_function

import logging
import weakref

from .fritzhomeentitybase import FritzhomeEntityBase
from .. import interfaces

_LOGGER = logging.getLogger(__name__)

def dict_deepmerge(base, override):
    """ Returns a new dict which is a recursive merge of two input dicts. """
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = dict_deepmerge(result[key], value)
        elif isinstance(value, dict):
            result[key] = value.copy()
        else:
            result[key] = value
    return result

class FritzhomeUnitBase(FritzhomeEntityBase):
    """The Fritzhome Device class."""

    _update_intervals = [ 0.25, 0.5, 0.75, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 7, 8, 9, 10, 15 ]

    def __init__(self, fritz=None, node=None):
        """Create a unit object (REST-only)."""
        self._updates = {}
        self.interfaces = {}
        super().__init__(fritz, node)

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

        for iface, node in node["interfaces"].items():
            if n := self.interfaces.get(iface):
                self.interfaces[iface]._update_from_node(node)
            else:
                self.interfaces[iface] = interfaces.FritzhomeInterface.create(self, iface, node)


    def _update_unit(self, node, wait=False):
        self._fritz.put_unit(self.ain, node)
        if not wait:
            return
        import time
        off = 0
        for i in self._update_intervals:
            # this calls our _update_from_node eventually
            self._fritz._update_unit(self.ain)
            if dict_deepmerge(self._node, node) == self._node:
                return
            time.sleep(i - off)
            off = i
        self._unit_ref().update()
        if self._node | node == self._node:
            return
        raise RuntimeError("Failed to fetch updated unit")

    def interface_changed(self, interface, node=None, wait=False):
        import sys

        if not self.commit_now:
            if wait:
                LOGGER.err("wait=True not supported in bulk update")
            self._updates |= {"interfaces": {interface.type: node or interface._node}}
            return
        self._update_unit({"interfaces": {interface.type: node or interface._node}}, wait)

    def begin(self):
        """DOC-TODO (REST)"""
        assert self.commit_now, "nested begin() not permitted"
        print(f"A {self}")
        self.commit_now = False
        return self

    def end(self, wait=False):
        """DOC-TODO (REST)"""
        print(f"Z {self}")
        self.commit_now = True
        self._update_unit(self._updates, wait)
        self._updates = {}

    def find_interface(self, interface):
        return self.interfaces.get(interface);

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
