"""The entity base class."""

# -*- coding: utf-8 -*-

from __future__ import print_function
from abc import ABC


import weakref
import logging
import json

_LOGGER = logging.getLogger(__name__)


class FritzhomeInterfaceBase():
    """The Fritzhome Interface class."""

    def __init__(self, unit, type, node):
        """Create an entity base object."""
        self.type = type
        self._node = node
        self._node_set = {}
        self._unit_ref = weakref.ref(unit)

    def __repr__(self):
        """Return a string."""
        return f"{self.type} of {self._unit_ref().ain}"

    def _update_from_node(self, node):
        self._node = node
        _LOGGER.debug(f"update {self.type}")
        if self._node["state"] != "valid":
            _LOGGER.warning(f"{self.type} state not valid")

    def changed(self, wait=False):
        assert self._node_set.keys() <= self._node.keys(), "_node_set must be a strict subset"
        self._unit_ref().interface_changed(self, self._node_set, wait)
        self._node_set = {}

    @property
    def node(self):
        return self._node;
