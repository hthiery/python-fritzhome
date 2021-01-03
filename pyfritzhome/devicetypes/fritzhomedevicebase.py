# -*- coding: utf-8 -*-

from __future__ import print_function
from abc import ABC


import logging
from xml.etree import ElementTree
from .fritzhomedevicefeatures import FritzhomeDeviceFeatures

_LOGGER = logging.getLogger(__name__)


class FritzhomeDeviceBase(ABC):
    """The Fritzhome Device class."""

    _fritz = None
    ain: str = None
    identifier = None
    fw_version = None
    manufacturer = None
    productname = None
    _functionsbitmask = None
    present = None

    def __init__(self, fritz=None, node=None):
        if fritz is not None:
            self._fritz = fritz
        if node is not None:
            self._update_from_node(node)

    def __repr__(self):
        """Return a string."""
        return "{ain} {identifier} {manuf} {prod} {name}".format(
            ain=self.ain,
            identifier=self.identifier,
            manuf=self.manufacturer,
            prod=self.productname,
            name=self.name,
        )

    def update(self):
        """Update the device values."""
        self._fritz.update_devices()

    def _has_feature(self, feature: FritzhomeDeviceFeatures) -> bool:
        return feature in FritzhomeDeviceFeatures(self._functionsbitmask)

    def _update_from_node(self, node):
        _LOGGER.debug(ElementTree.tostring(node))
        self.ain = node.attrib["identifier"]
        self.identifier = node.attrib["id"]
        self._functionsbitmask = int(node.attrib["functionbitmask"])
        self.fw_version = node.attrib["fwversion"]
        self.manufacturer = node.attrib["manufacturer"]
        self.productname = node.attrib["productname"]

        self.name = node.findtext("name").strip()
        self.present = bool(int(node.findtext("present")))

    # General
    def get_present(self):
        """Check if the device is present."""
        return self._fritz.get_device_present(self.ain)

    # XML Helpers

    def get_node_value(self, elem, node):
        return elem.findtext(node)

    def get_node_value_as_int(self, elem, node) -> int:
        return int(self.get_node_value(elem, node))

    def get_node_value_as_int_as_bool(self, elem, node) -> bool:
        return bool(self.get_node_value_as_int(elem, node))

    def get_temp_from_node(self, elem, node):
        return float(self.get_node_value(elem, node)) / 2
