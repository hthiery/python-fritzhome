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

    update_intervals = [ 0.25, 0.5, 0.75, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 7, 8, 9, 10, 15 ]

    @staticmethod
    def node_property(node_name, value_name):
        return property(
            fget = lambda self: self._node[node_name].get(value_name),
            fset = lambda self, v: self._node[node_name].update(value_name, v)
        )

    def __init__(self, unit, type, node):
        """Create an entity base object."""
        self.type = type
        self._node = node
        self._node_set = {}
        self._unit_ref = weakref.ref(unit)
        if node is not None:
            self._update_from_node(node)

    def __repr__(self):
        """Return a string."""
        return f"{self.type} of {self._unit_ref().ain}"

    def _update_from_node(self, node):
        self._node = node

    def changed(self, wait=False):
        import sys
        assert self._node_set.keys() <= self._node.keys(), "_node_set must be a strict subset"
        self._unit_ref().update_interface(self, self._node_set)
        if not wait:
            self._node_set = {}
            return
        import time
        off = 0
        for i in self.update_intervals:
            self._unit_ref().update()
            if self._node | self._node_set == self._node:
                self._node_set = {}
                return
            time.sleep(i - off)
            off = i
        self._unit_ref().update()
        if self._node | self._node_set == self._node:
            self._node_set = {}
            return
        raise RuntimeError("Failed to fetch updated interface")

    @property
    def node(self):
        return self._node;

