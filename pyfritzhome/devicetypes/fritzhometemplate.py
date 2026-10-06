"""The template class."""

from __future__ import annotations

import logging

from xml.etree import ElementTree

from .fritzhomeentitybase import FritzhomeEntityBase
from .fritzhomedevicefeatures import FritzhomeDeviceFeatures

_LOGGER = logging.getLogger(__name__)


class FritzhomeTemplate(FritzhomeEntityBase):
    """The Fritzhome Template class."""

    devices: list[str] | None = None
    features: FritzhomeDeviceFeatures | None = None
    apply_hkr_summer: bool | None = None
    apply_hkr_temperature: bool | None = None
    apply_hkr_holidays: bool | None = None
    apply_hkr_time_table: bool | None = None
    apply_relay_manual: bool | None = None
    apply_relay_automatic: bool | None = None
    apply_level: bool | None = None
    apply_color: bool | None = None
    apply_dialhelper: bool | None = None

    def _update_from_node(self, node: ElementTree.Element) -> None:
        _LOGGER.debug("update template")
        super()._update_from_node(node)

        self.features = FritzhomeDeviceFeatures(self._functionsbitmask)

        applymask = node.find("applymask")
        if applymask is None:
            raise ValueError("template node is missing applymask")
        self.apply_hkr_summer = applymask.find("hkr_summer") is not None
        self.apply_hkr_temperature = applymask.find("hkr_temperature") is not None
        self.apply_hkr_holidays = applymask.find("hkr_holidays") is not None
        self.apply_hkr_time_table = applymask.find("hkr_time_table") is not None
        self.apply_relay_manual = applymask.find("relay_manual") is not None
        self.apply_relay_automatic = applymask.find("relay_automatic") is not None
        self.apply_level = applymask.find("level") is not None
        self.apply_color = applymask.find("color") is not None
        self.apply_dialhelper = applymask.find("dialhelper") is not None

        devices = node.find("devices")
        if devices is None:
            raise ValueError("template node is missing devices")
        self.devices = []
        for device in devices.findall("device"):
            self.devices.append(device.attrib["identifier"])
