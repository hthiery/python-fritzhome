"""The button device class."""

from __future__ import annotations

import logging


from xml.etree import ElementTree
from .fritzhomedevicebase import FritzhomeDeviceBase
from .fritzhomedevicefeatures import FritzhomeDeviceFeatures

_LOGGER = logging.getLogger(__name__)


class FritzhomeDeviceButton(FritzhomeDeviceBase):
    """The Fritzhome Device class."""

    def _update_from_node(self, node: ElementTree.Element) -> None:
        super()._update_from_node(node)
        if self.present is False:
            return

        if self.has_button:
            self._update_button_from_node(node)

    # Button
    @property
    def has_button(self) -> bool:
        """Check if the device has button function."""
        return self._has_feature(FritzhomeDeviceFeatures.BUTTON)

    def _update_button_from_node(self, node: ElementTree.Element) -> None:
        _LOGGER.debug("update button device")
        self.buttons = {}

        for element in node.findall("button"):
            button = FritzhomeButton(element)
            self.buttons[button.ain] = button

    def get_button_by_ain(self, ain: str) -> "FritzhomeButton":
        """Return the button by AIN."""
        return self.buttons[ain]


class FritzhomeButton(object):
    """The Fritzhome Button Device class."""

    ain: str | None = None
    identifier: str | None = None
    name: str | None = None
    last_pressed: int | None = None

    def __init__(self, node: ElementTree.Element | None = None) -> None:
        """Create a button object."""
        if node is not None:
            self._update_from_node(node)

    def _update_from_node(self, node: ElementTree.Element) -> None:
        _LOGGER.debug(ElementTree.tostring(node))
        self.ain = node.attrib["identifier"]
        self.identifier = node.attrib["id"]
        self.name = node.findtext("name")
        try:
            self.last_pressed = self.get_node_value_as_int(node, "lastpressedtimestamp")
        except ValueError:
            pass

    def get_node_value(self, elem: ElementTree.Element | None, node: str) -> str | None:
        """Get the node value."""
        if elem is None:
            return None
        return elem.findtext(node)

    def get_node_value_as_int(self, elem: ElementTree.Element | None, node: str) -> int:
        """Get the node value as integer."""
        value = self.get_node_value(elem, node)
        if value is None:
            raise TypeError("node value is missing")
        return int(value)
