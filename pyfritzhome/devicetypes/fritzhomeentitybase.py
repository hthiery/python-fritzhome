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
        self.ain = None
        self.name = None
        self._functionsbitmask = 0
        self.commit_now = True
        if node is not None:
            self._update_from_node(node)

    def __repr__(self):
        """Return a string."""
        return f"{self.ain} {self.name}"

    def _has_feature(self, feature: FritzhomeDeviceFeatures) -> bool:
        return feature in FritzhomeDeviceFeatures(self._functionsbitmask)

    def _update_from_node(self, node):
        self._node = node
        if node.get("identifier") is not None: # AHA
            if self.ain is not None and self.ain != node.attrib["identifier"]:
                raise ValueError("updating invalid ain")
            self.ain = node.attrib["identifier"]
            self.name = self.get_node_value(node, "name")
            self._functionsbitmask = int(node.attrib["functionbitmask"])
        else: # REST
            if self.ain is not None and self.ain != node["ain"]:
                raise ValueError("updating invalid ain")
            self.ain = node["ain"]
            self.name = node["name"]

    @property
    def node(self):
        return self._node;

    @property
    def device_and_unit_id(self):
        """Get the device and possible unit id."""
        # These three are not exposed in the overview/devices endpoint in the REST api
        if (
            self.ain.startswith("tmp")
            or self.ain.startswith("grp")
            or self.ain.startswith("trg")
        ):
            return (self.ain, None)
        elif self.ain.startswith("Z") and len(self.ain) == 19:
            return (self.ain[0:17], self.ain[17:])
        elif "-" in self.ain:
            return tuple(self.ain.split("-"))
        return (self.ain, None)

    # XML Helpers

    def get_node_value(self, elem, node):
        """Get the node value."""
        return elem.findtext(node)

    def get_node_value_as_int(self, elem, node) -> int:
        """Get the node value as integer."""
        if value := self.get_node_value(elem, node):
            return int(value)
        return None

    def get_node_value_as_int_as_bool(self, elem, node) -> bool:
        """Get the node value as boolean."""
        return bool(self.get_node_value_as_int(elem, node))

    def get_temp_from_node(self, elem, node):
        """Get the node temp value as float."""
        return float(self.get_node_value(elem, node)) / 2
        return x
