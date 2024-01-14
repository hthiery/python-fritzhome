"""The light bulb device class."""
# -*- coding: utf-8 -*-

import logging

from .fritzhomedevicebase import FritzhomeDeviceBase
from .fritzhomedevicefeatures import FritzhomeDeviceFeatures

_LOGGER = logging.getLogger(__name__)


class FritzhomeDeviceLightBulb(FritzhomeDeviceBase):
    """The Fritzhome Device class."""

    state = None
    hue = None
    saturation = None
    unmapped_hue = None
    unmapped_saturation = None
    color_temp = None
    color_mode = None
    supported_color_mode = None

    def _update_from_node(self, node):
        super()._update_from_node(node)
        if self.present is False:
            return

        if self.has_lightbulb:
            self._update_lightbulb_from_node(node)

    # Light Bulb
    @property
    def has_lightbulb(self):
        """Check if the device has LightBulb function."""
        return self._has_feature(FritzhomeDeviceFeatures.LIGHTBULB)

    @property
    def has_color(self):
        """Check if the device has LightBulb function."""
        return self._has_feature(FritzhomeDeviceFeatures.COLOR)

    def _update_lightbulb_from_node(self, node):
        _LOGGER.debug("update light bulb device")
        state_element = node.find("simpleonoff")
        try:
            self.state = self.get_node_value_as_int_as_bool(state_element, "state")

        except ValueError:
            pass

        if self.has_color:
            colorcontrol_element = node.find("colorcontrol")
            try:
                self.color_mode = colorcontrol_element.attrib.get("current_mode")

                self.supported_color_mode = colorcontrol_element.attrib.get(
                    "supported_modes"
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

    def set_state_off(self):
        """Switch light bulb off."""
        self.state = True
        self._fritz.set_state_off(self.ain)

    def set_state_on(self):
        """Switch light bulb on."""
        self.state = True
        self._fritz.set_state_on(self.ain)

    def set_state_toggle(self):
        """Toogle light bulb state."""
        self.state = True
        self._fritz.set_state_toggle(self.ain)

    def get_colors(self):
        """Get the supported colors."""
        if self.has_color:
            return self._fritz.get_colors(self.ain)
        else:
            return {}

    def set_color(self, hsv, duration=0):
        """Set HSV color."""
        if self.has_color:
            self._fritz.set_color(self.ain, hsv, duration, True)

    def set_unmapped_color(self, hsv, duration=0):
        """Set unmapped HSV color (Free color selection)."""
        if self.has_color:
            self._fritz.set_color(self.ain, hsv, duration, False)

    def get_color_temps(self):
        """Get the supported color temperatures energy."""
        if self.has_color:
            return self._fritz.get_color_temps(self.ain)
        else:
            return []

    def set_color_temp(self, temperature, duration=0):
        """Set white color temperature."""
        if self.has_color:
            self._fritz.set_color_temp(self.ain, temperature, duration)
