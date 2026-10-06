"""The entity base class."""

from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, cast

import logging
from xml.etree import ElementTree
from .fritzhomedevicefeatures import FritzhomeDeviceFeatures

_LOGGER = logging.getLogger(__name__)

if TYPE_CHECKING:
    from pyfritzhome.fritzhome import Fritzhome


class FritzhomeEntityBase(ABC):
    """The Fritzhome Entity class."""

    _fritz: Fritzhome = cast("Fritzhome", None)
    ain: str
    _functionsbitmask: int = 0
    supported_features: list[FritzhomeDeviceFeatures] | None = None

    def __init__(
        self,
        fritz: "Fritzhome" | None = None,
        node: ElementTree.Element | None = None,
    ) -> None:
        """Create an entity base object."""
        if fritz is not None:
            self._fritz = fritz
        if node is not None:
            self._update_from_node(node)

    def __repr__(self) -> str:
        """Return a string."""
        return "{ain} {name}".format(
            ain=self.ain,
            name=self.name,
        )

    def _has_feature(self, feature: FritzhomeDeviceFeatures) -> bool:
        return feature in FritzhomeDeviceFeatures(self._functionsbitmask)

    def _update_from_node(self, node: ElementTree.Element) -> None:
        _LOGGER.debug(ElementTree.tostring(node))
        self.ain = node.attrib["identifier"]
        self._functionsbitmask = int(node.attrib["functionbitmask"])

        self.name = node.findtext("name", "").strip()

        self.supported_features = []
        for feature in FritzhomeDeviceFeatures:
            if self._has_feature(feature):
                self.supported_features.append(feature)

    @property
    def device_and_unit_id(self) -> tuple[str | None, str | None]:
        """Get the device and possible unit id."""
        if (
            self.ain.startswith("tmp")
            or self.ain.startswith("grp")
            or self.ain.startswith("trg")
        ):
            return (self.ain, None)
        elif self.ain.startswith("Z") and len(self.ain) == 19:
            return (self.ain[0:17], self.ain[17:])
        elif "-" in self.ain:
            return (self.ain.split("-")[0], self.ain.split("-")[1])
        return (self.ain, None)

    # XML Helpers

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

    def get_node_value_as_int_as_bool(
        self, elem: ElementTree.Element | None, node: str
    ) -> bool:
        """Get the node value as boolean."""
        return bool(self.get_node_value_as_int(elem, node))

    def get_temp_from_node(self, elem: ElementTree.Element | None, node: str) -> float:
        """Get the node temp value as float."""
        value = self.get_node_value(elem, node)
        if value is None:
            raise TypeError("node value is missing")
        return float(value) / 2
