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
        self._unit_ref = weakref.ref(unit)
        if node is not None:
            self._update_from_node(node)

    def __repr__(self):
        """Return a string."""
        return f"{self.type} of {self._unit_ref().ain}"

    def _update_from_node(self, node):
        pass

    def update(self):
        self._unit_ref().update_interface(self)

    @property
    def node(self):
        return self._node;
