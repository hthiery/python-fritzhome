"""The base device class."""
# -*- coding: utf-8 -*-

from __future__ import print_function

import logging
import weakref

from .fritzhomeentitybase import FritzhomeEntityBase
from .. import interfaces

_LOGGER = logging.getLogger(__name__)


class FritzhomeUnitBase(FritzhomeEntityBase):
    """The Fritzhome Device class."""

    interfaces = None

    def __init__(self, fritz=None, node=None):
        """Create a unit object (REST-only)."""
        super().__init__(fritz, node)
        self._updates = {}

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

    def update_interface(self, interface, node=None):
        import traceback
        if self.commit_now:
            traceback.print_stack()
            self._fritz.put_unit(self.ain, {"interfaces": {interface.type: node or interface._node}})
        else:
            self._updates |= {"interfaces": {interface.type: node or interface._node}}

    def begin(self):
        """DOC-TODO (REST)"""
        assert self.commit_now, "nested begin() not permitted"
        print(f"A {self}")
        self.commit_now = False
        return self

    def end(self):
        """DOC-TODO (REST)"""
        print(f"Z {self}")
        self.commit_now = True
        self.trigger_update()

    def trigger_update(self):
        self._fritz.put_unit(self.ain, self._updates)

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
