"""The base device class."""
# -*- coding: utf-8 -*-

from __future__ import print_function


import logging

from pyfritzhome.devicetypes.fritzhomeentitybase import FritzhomeEntityBase

_LOGGER = logging.getLogger(__name__)


class FritzhomeDeviceBase(FritzhomeEntityBase):
    """The Fritzhome Device class."""

    battery_level = None
    battery_low = None
    identifier = None
    is_group = None
    fw_version = None
    group_members = None
    manufacturer = None
    productname = None
    present = None
    tx_busy = None

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

    def _update_from_node(self, node):
        _LOGGER.debug("update base device")
        super()._update_from_node(node)
        self.ain = node.attrib["identifier"]
        self.identifier = node.attrib["id"]
        self.fw_version = node.attrib["fwversion"]
        self.manufacturer = node.attrib["manufacturer"]
        self.productname = node.attrib["productname"]

        self.present = bool(int(node.findtext("present")))

        groupinfo = node.find("groupinfo")
        self.is_group = groupinfo is not None
        if self.is_group:
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
    def get_present(self):
        """Check if the device is present."""
        return self._fritz.get_device_present(self.ain)
