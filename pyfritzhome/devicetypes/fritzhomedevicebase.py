"""The base device class."""

from __future__ import print_function


import logging
from typing import Optional
from xml.etree import ElementTree

from pyfritzhome.devicetypes.fritzhomeentitybase import FritzhomeEntityBase

_LOGGER = logging.getLogger(__name__)


class FritzhomeDeviceBase(FritzhomeEntityBase):
    """The Fritzhome Device class."""

    battery_level: Optional[int] = None
    battery_low: Optional[bool] = None
    identifier: Optional[str] = None
    is_group: Optional[bool] = None
    fw_version: Optional[str] = None
    group_members: Optional[list[str]] = None
    manufacturer: Optional[str] = None
    productname: Optional[str] = None
    present: Optional[bool] = None
    tx_busy: Optional[bool] = None

    def __repr__(self) -> str:
        """Return a string."""
        return "{ain} {identifier} {manuf} {prod} {name}".format(
            ain=self.ain,
            identifier=self.identifier,
            manuf=self.manufacturer,
            prod=self.productname,
            name=self.name,
        )

    def update(self) -> None:
        """Update the device values."""
        self._fritz.update_devices()

    def _update_from_node(self, node: ElementTree.Element) -> None:
        _LOGGER.debug("update base device")
        super()._update_from_node(node)
        self.ain = node.attrib["identifier"]
        self.identifier = node.attrib["id"]
        self.fw_version = node.attrib["fwversion"]
        self.manufacturer = node.attrib["manufacturer"]
        self.productname = node.attrib["productname"]

        present_value = node.findtext("present")
        if present_value is None:
            raise ValueError("device node is missing present state")
        self.present = bool(int(present_value))

        groupinfo = node.find("groupinfo")
        self.is_group = groupinfo is not None
        if groupinfo is not None:
            self.group_members = str(groupinfo.findtext("members")).split(",")

        try:
            self.tx_busy = self.get_node_value_as_int_as_bool(node, "txbusy")
        except Exception:
            pass

        try:
            self.battery_low = self.get_node_value_as_int_as_bool(node, "batterylow")
            self.battery_level = int(self.get_node_value_as_int(node, "battery"))
        except Exception:
            pass

    # General
    def get_present(self) -> bool:
        """Check if the device is present."""
        return self._fritz.get_device_present(self.ain)
