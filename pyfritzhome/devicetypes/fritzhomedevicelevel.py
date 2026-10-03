"""The level device class."""

import logging
from typing import Optional, Union
from xml.etree import ElementTree

from .fritzhomedevicebase import FritzhomeDeviceBase
from .fritzhomedevicefeatures import FritzhomeDeviceFeatures

_LOGGER = logging.getLogger(__name__)


class FritzhomeDeviceLevel(FritzhomeDeviceBase):
    """The Fritzhome Device class."""

    level: Optional[int] = None
    levelpercentage: Optional[int] = None

    def _update_from_node(self, node: ElementTree.Element) -> None:
        super()._update_from_node(node)
        if self.present is False:
            return

        if self.has_level:
            self._update_level_from_node(node)

    # Level
    @property
    def has_level(self) -> bool:
        """Check if the device has level function."""
        return self._has_feature(FritzhomeDeviceFeatures.LEVEL)

    def _update_level_from_node(self, node: ElementTree.Element) -> None:
        _LOGGER.debug("update level device")
        levelcontrol_element = node.find("levelcontrol")
        try:
            self.level = self.get_node_value_as_int(levelcontrol_element, "level")
            self.levelpercentage = self.get_node_value_as_int(
                levelcontrol_element, "levelpercentage"
            )
        except Exception:
            pass

    def get_level(self) -> Optional[int]:
        """Get the level."""
        return self.level

    def get_level_percentage(self) -> Optional[int]:
        """Get the level in percentage."""
        return self.levelpercentage

    def set_level(self, level: Union[int, float], wait: bool = False) -> None:
        """Set the level."""
        self._fritz.set_level(self.ain, level, wait)

    def set_level_percentage(
        self, levelpercentage: Union[int, float], wait: bool = False
    ) -> None:
        """Set the level in percentage."""
        self._fritz.set_level_percentage(self.ain, levelpercentage, wait)
