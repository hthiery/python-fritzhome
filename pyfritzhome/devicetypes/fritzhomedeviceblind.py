"""The blind device class."""
# -*- coding: utf-8 -*-

import logging

from .fritzhomedevicebase import FritzhomeDeviceBase
from .fritzhomedevicefeatures import FritzhomeDeviceFeatures

_LOGGER = logging.getLogger(__name__)


class FritzhomeDeviceBlind(FritzhomeDeviceBase):
    """The Fritzhome Device class."""

    endpositionsset = None

    def _update_from_node(self, node):
        super()._update_from_node(node)
        if self.present is False:
            return

        if self.has_blind:
            self._update_blind_from_node(node)

    # Blind
    @property
    def has_blind(self):
        """Check if the device has blind function."""
        return self._has_feature(FritzhomeDeviceFeatures.BLIND)

    def _update_blind_from_node(self, node):
        _LOGGER.debug("update blind device")
        blind_element = node.find("blind")
        try:
            self.endpositionsset = self.get_node_value_as_int_as_bool(
                blind_element, "endpositionsset"
            )
        except Exception:
            pass

    def set_blind_open(self, wait=False):
        """Open the blind."""
        self._fritz.set_blind_open(self.ain, wait)

    def set_blind_close(self, wait=False):
        """Close the blind."""
        self._fritz.set_blind_close(self.ain, wait)

    def set_blind_stop(self, wait=False):
        """Stop the blind."""
        self._fritz.set_blind_stop(self.ain, wait)
