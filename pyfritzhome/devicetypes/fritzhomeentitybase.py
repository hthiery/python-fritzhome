"""The entity base class."""
# -*- coding: utf-8 -*-

from __future__ import print_function
from abc import ABC


import logging
from xml.etree import ElementTree
from .fritzhomedevicefeatures import FritzhomeDeviceFeatures

_LOGGER = logging.getLogger(__name__)


class FritzhomeEntityBase(ABC):
    """The Fritzhome Entity class."""

    _fritz = None
    ain: str = None
    _functionsbitmask = None
    supported_features = None

    def __init__(self, fritz=None, node=None):
        """Create an entity base object."""
        if fritz is not None:
            self._fritz = fritz
        if node is not None:
            self._update_from_node(node)

    def __repr__(self):
        """Return a string."""
        return "{ain} {name}".format(
            ain=self.ain,
            name=self.name,
        )

    def _has_feature(self, feature: FritzhomeDeviceFeatures) -> bool:
        return feature in FritzhomeDeviceFeatures(self._functionsbitmask)

    def _update_from_node(self, node):
        _LOGGER.debug(ElementTree.tostring(node))
        self.ain = node.attrib["identifier"]
        self._functionsbitmask = int(node.attrib["functionbitmask"])

        self.name = node.findtext("name").strip()

        self.supported_features = []
        for feature in FritzhomeDeviceFeatures:
            if self._has_feature(feature):
                self.supported_features.append(feature)

    @property
    def device_and_unit_id(self):
        """Get the device and possible unit id."""
        if self.ain.startswith("tmp") or self.ain.startswith("grp"):
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
        return int(self.get_node_value(elem, node))

    def get_node_value_as_int_as_bool(self, elem, node) -> bool:
        """Get the node value as boolean."""
        return bool(self.get_node_value_as_int(elem, node))

    def get_temp_from_node(self, elem, node):
        """Get the node temp value as float."""
        return float(self.get_node_value(elem, node)) / 2
