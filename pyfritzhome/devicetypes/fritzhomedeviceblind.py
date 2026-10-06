"""The blind device class."""

from __future__ import annotations

import logging

from xml.etree import ElementTree

from .fritzhomedevicebase import FritzhomeDeviceBase
from .fritzhomedevicefeatures import FritzhomeDeviceFeatures

_LOGGER = logging.getLogger(__name__)


class FritzhomeDeviceBlind(FritzhomeDeviceBase):
    """The Fritzhome Device class."""

    endpositionsset: bool | None = None

    def _update_from_node(self, node: ElementTree.Element) -> None:
        super()._update_from_node(node)
        if self.present is False:
            return

        if self.has_blind:
            self._update_blind_from_node(node)

    # Blind
    @property
    def has_blind(self) -> bool:
        """Check if the device has blind function."""
        return self._has_feature(FritzhomeDeviceFeatures.BLIND)

    def _update_blind_from_node(self, node: ElementTree.Element) -> None:
        _LOGGER.debug("update blind device")
        blind_element = node.find("blind")
        try:
            self.endpositionsset = self.get_node_value_as_int_as_bool(
                blind_element, "endpositionsset"
            )
        except Exception:
            pass

    def set_blind_open(self, wait: bool = False) -> None:
        """Open the blind."""
        self._fritz.set_blind_open(self.ain, wait)

    def set_blind_close(self, wait: bool = False) -> None:
        """Close the blind."""
        self._fritz.set_blind_close(self.ain, wait)

    def set_blind_stop(self, wait: bool = False) -> None:
        """Stop the blind."""
        self._fritz.set_blind_stop(self.ain, wait)
