"""The light bulb device class."""

import logging
from typing import Optional, Sequence, SupportsInt, Union
from xml.etree import ElementTree

from .fritzhomedevicebase import FritzhomeDeviceBase
from .fritzhomedevicefeatures import FritzhomeDeviceFeatures

_LOGGER = logging.getLogger(__name__)


class FritzhomeDeviceLightBulb(FritzhomeDeviceBase):
    """The Fritzhome Device class."""

    state: Optional[bool] = None
    hue: Optional[int] = None
    saturation: Optional[int] = None
    unmapped_hue: Optional[int] = None
    unmapped_saturation: Optional[int] = None
    color_temp: Optional[int] = None
    color_mode: Optional[str] = None
    supported_color_mode: Optional[str] = None
    fullcolorsupport: bool = False

    def _update_from_node(self, node: ElementTree.Element) -> None:
        super()._update_from_node(node)
        if self.present is False:
            return

        if self.has_lightbulb:
            self._update_lightbulb_from_node(node)

    # Light Bulb
    @property
    def has_lightbulb(self) -> bool:
        """Check if the device has LightBulb function."""
        return self._has_feature(FritzhomeDeviceFeatures.LIGHTBULB)

    @property
    def has_color(self) -> bool:
        """Check if the device has LightBulb function."""
        return self._has_feature(FritzhomeDeviceFeatures.COLOR)

    def _update_lightbulb_from_node(self, node: ElementTree.Element) -> None:
        _LOGGER.debug("update light bulb device")
        state_element = node.find("simpleonoff")
        try:
            self.state = self.get_node_value_as_int_as_bool(state_element, "state")

        except ValueError:
            pass

        if self.has_color:
            colorcontrol_element = node.find("colorcontrol")
            if colorcontrol_element is None:
                return
            try:
                self.color_mode = colorcontrol_element.attrib.get("current_mode")

                self.supported_color_mode = colorcontrol_element.attrib.get(
                    "supported_modes"
                )

                self.fullcolorsupport = bool(
                    colorcontrol_element.attrib.get("fullcolorsupport")
                )

            except ValueError:
                pass

            try:
                self.hue = self.get_node_value_as_int(colorcontrol_element, "hue")

                self.saturation = self.get_node_value_as_int(
                    colorcontrol_element, "saturation"
                )

                self.unmapped_hue = self.get_node_value_as_int(
                    colorcontrol_element, "unmapped_hue"
                )

                self.unmapped_saturation = self.get_node_value_as_int(
                    colorcontrol_element, "unmapped_saturation"
                )
            except ValueError:
                # reset values after color mode changed
                self.hue = None
                self.saturation = None
                self.unmapped_hue = None
                self.unmapped_saturation = None

            try:
                self.color_temp = self.get_node_value_as_int(
                    colorcontrol_element, "temperature"
                )

            except ValueError:
                # reset values after color mode changed
                self.color_temp = None

    def set_state_off(self, wait: bool = False) -> None:
        """Switch light bulb off."""
        self.state = True
        self._fritz.set_state_off(self.ain, wait)

    def set_state_on(self, wait: bool = False) -> None:
        """Switch light bulb on."""
        self.state = True
        self._fritz.set_state_on(self.ain, wait)

    def set_state_toggle(self, wait: bool = False) -> None:
        """Toogle light bulb state."""
        self.state = True
        self._fritz.set_state_toggle(self.ain, wait)

    def get_colors(
        self,
    ) -> dict[str, list[tuple[Optional[str], Optional[str], Optional[str]]]]:
        """Get the supported colors."""
        if self.has_color:
            return self._fritz.get_colors(self.ain)
        else:
            return {}

    def set_color(
        self,
        hsv: Sequence[Union[str, SupportsInt]],
        duration: int = 0,
        wait: bool = False,
    ) -> None:
        """Set HSV color."""
        if self.has_color:
            self._fritz.set_color(self.ain, hsv, duration, True, wait)

    def set_unmapped_color(
        self,
        hsv: Sequence[Union[str, SupportsInt]],
        duration: int = 0,
        wait: bool = False,
    ) -> None:
        """Set unmapped HSV color (Free color selection)."""
        if self.has_color and self.fullcolorsupport:
            self._fritz.set_color(self.ain, hsv, duration, False, wait)

    def get_color_temps(self) -> list[Optional[str]]:
        """Get the supported color temperatures energy."""
        if self.has_color:
            return self._fritz.get_color_temps(self.ain)
        else:
            return []

    def set_color_temp(
        self,
        temperature: Union[str, int, float],
        duration: int = 0,
        wait: bool = False,
    ) -> None:
        """Set white color temperature."""
        if self.has_color:
            self._fritz.set_color_temp(self.ain, temperature, duration, wait)
