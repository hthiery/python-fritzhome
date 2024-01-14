"""The template class."""
# -*- coding: utf-8 -*-

import logging

from .fritzhomeentitybase import FritzhomeEntityBase
from .fritzhomedevicefeatures import FritzhomeDeviceFeatures

_LOGGER = logging.getLogger(__name__)


class FritzhomeTemplate(FritzhomeEntityBase):
    """The Fritzhome Template class."""

    devices = None
    features = None
    apply_hkr_summer = None
    apply_hkr_temperature = None
    apply_hkr_holidays = None
    apply_hkr_time_table = None
    apply_relay_manual = None
    apply_relay_automatic = None
    apply_level = None
    apply_color = None
    apply_dialhelper = None

    def _update_from_node(self, node):
        _LOGGER.debug("update template")
        super()._update_from_node(node)

        self.features = FritzhomeDeviceFeatures(self._functionsbitmask)

        applymask = node.find("applymask")
        self.apply_hkr_summer = applymask.find("hkr_summer") is not None
        self.apply_hkr_temperature = applymask.find("hkr_temperature") is not None
        self.apply_hkr_holidays = applymask.find("hkr_holidays") is not None
        self.apply_hkr_time_table = applymask.find("hkr_time_table") is not None
        self.apply_relay_manual = applymask.find("relay_manual") is not None
        self.apply_relay_automatic = applymask.find("relay_automatic") is not None
        self.apply_level = applymask.find("level") is not None
        self.apply_color = applymask.find("color") is not None
        self.apply_dialhelper = applymask.find("dialhelper") is not None

        self.devices = []
        for device in node.find("devices").findall("device"):
            self.devices.append(device.attrib["identifier"])
