"""The thermostat device class."""
# -*- coding: utf-8 -*-

import logging
import time

from .fritzhomedevicebase import FritzhomeDeviceBase
from .fritzhomedevicefeatures import FritzhomeDeviceFeatures

_LOGGER = logging.getLogger(__name__)


class FritzhomeDeviceThermostat(FritzhomeDeviceBase):
    """The Fritzhome Device class."""

    actual_temperature = None
    target_temperature = None
    eco_temperature = None
    comfort_temperature = None
    device_lock = None
    lock = None
    error_code = None
    window_open = None
    window_open_endtime = None
    boost_active = None
    boost_active_endtime = None
    adaptive_heating_active = None
    adaptive_heating_running = None
    summer_active = None
    holiday_active = None
    nextchange_endperiod = None
    nextchange_temperature = None

    def _update_from_node(self, node):
        super()._update_from_node(node)
        if self.present is False:
            return

        if self.has_thermostat:
            self._update_hkr_from_node(node)

    # Thermostat
    @property
    def has_thermostat(self):
        """Check if the device has thermostat function."""
        return self._has_feature(FritzhomeDeviceFeatures.THERMOSTAT)

    def _update_hkr_from_node(self, node):
        _LOGGER.debug("update thermostat device")
        hkr_element = node.find("hkr")

        try:
            self.actual_temperature = self.get_temp_from_node(hkr_element, "tist")
        except ValueError:
            pass

        try:
            self.target_temperature = self.get_temp_from_node(hkr_element, "tsoll")
        except ValueError:
            self.target_temperature = None

        self.eco_temperature = self.get_temp_from_node(hkr_element, "absenk")
        self.comfort_temperature = self.get_temp_from_node(hkr_element, "komfort")

        # optional value
        try:
            self.device_lock = self.get_node_value_as_int_as_bool(
                hkr_element, "devicelock"
            )
            self.lock = self.get_node_value_as_int_as_bool(hkr_element, "lock")
            self.error_code = self.get_node_value_as_int(hkr_element, "errorcode")
            # keep battery values as fallback for Fritz!OS < 7.08

            if hkr_element.find("batterylow") is not None:
                self.battery_low = self.get_node_value_as_int_as_bool(
                    hkr_element, "batterylow"
                )
                self.battery_level = int(
                    self.get_node_value_as_int(hkr_element, "battery")
                )

            self.window_open = self.get_node_value_as_int_as_bool(
                hkr_element, "windowopenactiv"
            )
            self.window_open_endtime = (
                self.get_node_value_as_int(hkr_element, "windowopenactiveendtime")
                - time.time()
            )
            if self.window_open_endtime < 0:
                self.window_open_endtime = 0
            self.summer_active = self.get_node_value_as_int_as_bool(
                hkr_element, "summeractive"
            )
            self.holiday_active = self.get_node_value_as_int_as_bool(
                hkr_element, "holidayactive"
            )
            nextchange_element = hkr_element.find("nextchange")
            self.nextchange_endperiod = int(
                self.get_node_value_as_int(nextchange_element, "endperiod")
            )
            self.nextchange_temperature = self.get_temp_from_node(
                nextchange_element, "tchange"
            )

            if hkr_element.find("boostactive") is not None:
                self.boost_active = self.get_node_value_as_int_as_bool(
                    hkr_element, "boostactive"
                )
                self.boost_active_endtime = (
                    self.get_node_value_as_int(hkr_element, "boostactiveendtime")
                    - time.time()
                )
                if self.boost_active_endtime < 0:
                    self.boost_active_endtime = 0

            if hkr_element.find("adaptiveHeatingActive") is not None:
                self.adaptive_heating_active = self.get_node_value_as_int_as_bool(
                    hkr_element, "adaptiveHeatingActive"
                )
                self.adaptive_heating_running = self.get_node_value_as_int_as_bool(
                    hkr_element, "adaptiveHeatingRunning"
                )

        except Exception:
            pass

    def get_temperature(self):
        """Get the device temperature value."""
        return self._fritz.get_temperature(self.ain)

    def get_target_temperature(self):
        """Get the thermostate target temperature."""
        return self._fritz.get_target_temperature(self.ain)

    def set_target_temperature(self, temperature, wait=False):
        """Set the thermostate target temperature."""
        return self._fritz.set_target_temperature(self.ain, temperature, wait)

    def set_window_open(self, seconds, wait=False):
        """Set the thermostate to window open."""
        return self._fritz.set_window_open(self.ain, seconds, wait)

    def set_boost_mode(self, seconds, wait=False):
        """Set the thermostate into boost mode."""
        return self._fritz.set_boost_mode(self.ain, seconds, wait)

    def get_comfort_temperature(self):
        """Get the thermostate comfort temperature."""
        return self._fritz.get_comfort_temperature(self.ain)

    def get_eco_temperature(self):
        """Get the thermostate eco temperature."""
        return self._fritz.get_eco_temperature(self.ain)

    def get_hkr_state(self):
        """Get the thermostate state."""
        try:
            return {
                126.5: "off",
                127.0: "on",
                self.eco_temperature: "eco",
                self.comfort_temperature: "comfort",
            }[self.target_temperature]
        except KeyError:
            return "manual"

    def set_hkr_state(self, state, wait=False):
        """Set the state of the thermostat.

        Possible values for state are: 'on', 'off', 'comfort', 'eco'.
        """
        try:
            value = {
                "off": 0,
                "on": 100,
                "eco": self.eco_temperature,
                "comfort": self.comfort_temperature,
            }[state]
        except KeyError:
            return

        self.set_target_temperature(value, wait)
