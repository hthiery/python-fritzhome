"""The base device class."""
# -*- coding: utf-8 -*-

from __future__ import print_function


import logging

from pyfritzhome.devicetypes.fritzhomeentitybase import FritzhomeEntityBase

_LOGGER = logging.getLogger(__name__)


class FritzhomeDeviceBase(FritzhomeEntityBase):
    """The Fritzhome Device class."""

    identifier = None
    fw_version = None
    manufacturer = None
    productname = None
    present = None

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
        super()._update_from_node(node)
        self.ain = node.attrib["identifier"]
        self.identifier = node.attrib["id"]
        self.fw_version = node.attrib["fwversion"]
        self.manufacturer = node.attrib["manufacturer"]
        self.productname = node.attrib["productname"]

        self.present = bool(int(node.findtext("present")))

    # General
    def get_present(self):
        """Check if the device is present."""
        return self._fritz.get_device_present(self.ain)
