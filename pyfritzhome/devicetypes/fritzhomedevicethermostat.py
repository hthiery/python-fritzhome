"""The thermostat device class."""

from __future__ import annotations

import logging
import time

from xml.etree import ElementTree

from .fritzhomedevicebase import FritzhomeDeviceBase
from .fritzhomedevicefeatures import FritzhomeDeviceFeatures

_LOGGER = logging.getLogger(__name__)


class FritzhomeDeviceThermostat(FritzhomeDeviceBase):
    """The Fritzhome Device class."""

    actual_temperature: float | None = None
    target_temperature: float | None = None
    eco_temperature: float | None = None
    comfort_temperature: float | None = None
    device_lock: bool | None = None
    lock: bool | None = None
    error_code: int | None = None
    window_open: bool | None = None
    window_open_endtime: float | None = None
    boost_active: bool | None = None
    boost_active_endtime: float | None = None
    adaptive_heating_active: bool | None = None
    adaptive_heating_running: bool | None = None
    summer_active: bool | None = None
    holiday_active: bool | None = None
    nextchange_endperiod: int | None = None
    nextchange_temperature: float | None = None

    def _update_from_node(self, node: ElementTree.Element) -> None:
        super()._update_from_node(node)
        if self.present is False:
            return

        if self.has_thermostat:
            self._update_hkr_from_node(node)

    # Thermostat
    @property
    def has_thermostat(self) -> bool:
        """Check if the device has thermostat function."""
        return self._has_feature(FritzhomeDeviceFeatures.THERMOSTAT)

    def _update_hkr_from_node(self, node: ElementTree.Element) -> None:
        _LOGGER.debug("update thermostat device")
        hkr_element = node.find("hkr")
        if hkr_element is None:
            return

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

    def get_temperature(self) -> float:
        """Get the device temperature value."""
        return self._fritz.get_temperature(self.ain)

    def get_target_temperature(self) -> float:
        """Get the thermostate target temperature."""
        return self._fritz.get_target_temperature(self.ain)

    def set_target_temperature(self, temperature: float, wait: bool = False) -> None:
        """Set the thermostate target temperature."""
        return self._fritz.set_target_temperature(self.ain, temperature, wait)

    def set_window_open(self, seconds: float, wait: bool = False) -> None:
        """Set the thermostate to window open."""
        return self._fritz.set_window_open(self.ain, seconds, wait)

    def set_boost_mode(self, seconds: float, wait: bool = False) -> None:
        """Set the thermostate into boost mode."""
        return self._fritz.set_boost_mode(self.ain, seconds, wait)

    def get_comfort_temperature(self) -> float:
        """Get the thermostate comfort temperature."""
        return self._fritz.get_comfort_temperature(self.ain)

    def get_eco_temperature(self) -> float:
        """Get the thermostate eco temperature."""
        return self._fritz.get_eco_temperature(self.ain)

    def get_hkr_state(self) -> str:
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

    def set_hkr_state(self, state: str, wait: bool = False) -> None:
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

        if value is not None:
            self.set_target_temperature(value, wait)
