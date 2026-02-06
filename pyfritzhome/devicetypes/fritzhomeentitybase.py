"""The entity base class."""

# -*- coding: utf-8 -*-

from __future__ import print_function
from abc import ABC


import logging
import json
from .fritzhomedevicefeatures import FritzhomeDeviceFeatures

_LOGGER = logging.getLogger(__name__)


class FritzhomeEntityBase(ABC):
    """The Fritzhome Entity class."""

    def __init__(self, fritz=None, node=None):
        """Create an entity base object."""
        self._fritz = fritz
        self._node = node
        if node is not None:
            self._update_from_node(node)

    def __repr__(self):
        """Return a string."""
        return f"{self.ain} {self.name}"

    def _update_from_node(self, node):
        _LOGGER.debug(json.dumps(node))
        if self.ain != node["ain"]:
            raise ValueError("updating invalid ain")
        self._node = node

    @property
    def node(self):
        return self._node;

    @property
    def ain(self):
        return self._node["ain"];

    @property
    def name(self):
        return self._node["name"];
