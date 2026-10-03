"""The temperature device class."""

import logging
from typing import Optional
from xml.etree import ElementTree

from .fritzhomedevicebase import FritzhomeDeviceBase
from .fritzhomedevicefeatures import FritzhomeDeviceFeatures

_LOGGER = logging.getLogger(__name__)


class FritzhomeDeviceTemperature(FritzhomeDeviceBase):
    """The Fritzhome Device class."""

    offset: Optional[float] = None
    temperature: Optional[float] = None

    def _update_from_node(self, node: ElementTree.Element) -> None:
        super()._update_from_node(node)
        if self.present is False:
            return

        if self.has_temperature_sensor:
            self._update_temperature_from_node(node)

    # Temperature
    @property
    def has_temperature_sensor(self) -> bool:
        """Check if the device has temperature function."""
        return self._has_feature(FritzhomeDeviceFeatures.TEMPERATURE)

    def _update_temperature_from_node(self, node: ElementTree.Element) -> None:
        _LOGGER.debug("update temperature device")
        temperature_element = node.find("temperature")
        try:
            self.offset = (
                self.get_node_value_as_int(temperature_element, "offset") / 10.0
            )
        except ValueError:
            pass

        try:
            self.temperature = (
                self.get_node_value_as_int(temperature_element, "celsius") / 10.0
            )
        except ValueError:
            pass
