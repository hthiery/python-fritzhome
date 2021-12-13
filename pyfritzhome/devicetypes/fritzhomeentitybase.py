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

    def __init__(self, fritz=None, node=None):
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

    # XML Helpers

    def get_node_value(self, elem, node):
        return elem.findtext(node)

    def get_node_value_as_int(self, elem, node) -> int:
        return int(self.get_node_value(elem, node))

    def get_node_value_as_int_as_bool(self, elem, node) -> bool:
        return bool(self.get_node_value_as_int(elem, node))

    def get_temp_from_node(self, elem, node):
        return float(self.get_node_value(elem, node)) / 2
