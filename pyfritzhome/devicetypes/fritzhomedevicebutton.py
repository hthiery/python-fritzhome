"""The button device class."""
# -*- coding: utf-8 -*-

import logging

from xml.etree import ElementTree
from .fritzhomedevicebase import FritzhomeDeviceBase
from .fritzhomedevicefeatures import FritzhomeDeviceFeatures

_LOGGER = logging.getLogger(__name__)


class FritzhomeDeviceButton(FritzhomeDeviceBase):
    """The Fritzhome Device class."""

    def _update_from_node(self, node):
        super()._update_from_node(node)
        if self.present is False:
            return

        if self.has_button:
            self._update_button_from_node(node)

    # Button
    @property
    def has_button(self):
        """Check if the device has button function."""
        return self._has_feature(FritzhomeDeviceFeatures.BUTTON)

    def _update_button_from_node(self, node):
        _LOGGER.debug("update button device")
        self.buttons = {}

        for element in node.findall("button"):
            button = FritzhomeButton(element)
            self.buttons[button.ain] = button

    def get_button_by_ain(self, ain):
        """Return the button by AIN."""
        return self.buttons[ain]


class FritzhomeButton(object):
    """The Fritzhome Button Device class."""

    ain = None
    identifier = None
    name = None
    last_pressed = None

    def __init__(self, node=None):
        """Create a button object."""
        if node is not None:
            self._update_from_node(node)

    def _update_from_node(self, node):
        _LOGGER.debug(ElementTree.tostring(node))
        self.ain = node.attrib["identifier"]
        self.identifier = node.attrib["id"]
        self.name = node.findtext("name")
        try:
            self.last_pressed = self.get_node_value_as_int(node, "lastpressedtimestamp")
        except ValueError:
            pass

    def get_node_value(self, elem, node):
        """Get the node value."""
        return elem.findtext(node)

    def get_node_value_as_int(self, elem, node) -> int:
        """Get the node value as integer."""
        return int(self.get_node_value(elem, node))
