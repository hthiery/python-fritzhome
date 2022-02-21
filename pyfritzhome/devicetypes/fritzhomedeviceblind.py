# -*- coding: utf-8 -*-

import logging

from xml.etree import ElementTree
from .fritzhomedevicebase import FritzhomeDeviceBase
from .fritzhomedevicefeatures import FritzhomeDeviceFeatures

_LOGGER = logging.getLogger(__name__)


class FritzhomeDeviceBlind(FritzhomeDeviceBase):
    """The Fritzhome Device class."""
    
    tx_busy = None
    endpositionsset = None
    level = None
    levelpercentage = None

    def _update_from_node(self, node):
        super()._update_from_node(node)
        if self.present is False:
            return

        if self.has_blind:
            self._update_blind_from_node(node)

    # Button
    @property
    def has_blind(self):
        """Check if the device has blind function."""
        return self._has_feature(FritzhomeDeviceFeatures.BLIND)

    def _update_blind_from_node(self, node):
        #print("update from blind")
        try:
            self.tx_busy = self.get_node_value_as_int_as_bool(node, "txbusy")
        except Exception:
            pass
        blind_element = node.find("blind")
        try:
            self.endpositionsset = self.get_node_value_as_int_as_bool(blind_element, "endpositionsset")
        except Exception:
            pass
        levelcontrol_element = node.find("levelcontrol")
        try:
            self.level = self.get_node_value_as_int(levelcontrol_element, "level")
            self.levelpercentage = self.get_node_value_as_int(levelcontrol_element, "levelpercentage")
        except Exception:
            pass
    
    def get_level(self):
        return self.level
    
    def get_level_percentage(self):
        return self.levelpercentage
        
    def set_level(self, level):
        self._fritz.set_level(self.ain, level)
    def set_level_percentage(self, levelpercentage):
        self._fritz.set_level_percentage(self.ain, levelpercentage)
    def set_blind_open(self):
        self._fritz.set_blind_open(self.ain)
    def set_blind_close(self):
        self._fritz.set_blind_close(self.ain)
    def set_blind_stop(self):
        self._fritz.set_blind_stop(self.ain)
