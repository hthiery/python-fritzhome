"""The entity base class."""

# -*- coding: utf-8 -*-

from __future__ import print_function
from abc import ABC


import logging
import json

_LOGGER = logging.getLogger(__name__)


class FritzhomeInterfaceBase():
    """The Fritzhome Interface class."""

    def __init__(self, type, node):
        """Create an entity base object."""
        self.type = type
        self._node = node
        if node is not None:
            self._update_from_node(node)

    def __repr__(self):
        """Return a string."""
        return f"{self.type} of {self._unit.ain}"

    def _update_from_node(self, node):
        pass

    @property
    def node(self):
        return self._node;
