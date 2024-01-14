#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest.mock import MagicMock

from pyfritzhome import Fritzhome, FritzhomeDevice
from pyfritzhome.devicetypes.fritzhomedevicefeatures import FritzhomeDeviceFeatures

from .helper import Helper


class TestFritzhomeDeviceThermostat(object):
    def setup_method(self):
        self.mock = MagicMock()
        self.fritz = Fritzhome("10.0.0.1", "user", "pass")
        self.fritz._request = self.mock
        self.fritz._devices = {}

    def test_device_hkr_fw_03_50(self):
        self.mock.side_effect = [
            Helper.response("thermostat/device_hkr_fw_03_50"),
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345")
        assert device.present
        assert device.device_lock is None
        assert device.lock is None
        assert device.error_code is None
        assert device.battery_low is None
        assert device.supported_features == [
            FritzhomeDeviceFeatures.THERMOSTAT,
            FritzhomeDeviceFeatures.TEMPERATURE,
        ]

    def test_device_hkr_fw_03_54(self):
        self.mock.side_effect = [
            Helper.response("thermostat/device_hkr_fw_03_54"),
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("23456")
        assert device.present
        assert device.supported_features == [
            FritzhomeDeviceFeatures.THERMOSTAT,
            FritzhomeDeviceFeatures.TEMPERATURE,
        ]

    def test_get_target_temperature(self):
        self.mock.side_effect = [
            Helper.response("thermostat/device_hkr_fritzos_7"),
            "38",
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345")

        assert device.get_target_temperature() == 19.0
        device._fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {"ain": "12345", "switchcmd": "gethkrtsoll", "sid": None},
        )

    def test_get_eco_temperature(self):
        self.mock.side_effect = [
            Helper.response("thermostat/device_hkr_fritzos_7"),
            "40",
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345")

        assert device.get_eco_temperature() == 20.0
        device._fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {"ain": "12345", "switchcmd": "gethkrabsenk", "sid": None},
        )

    def test_get_comfort_temperature(self):
        self.mock.side_effect = [
            Helper.response("thermostat/device_hkr_fritzos_7"),
            "41",
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345")

        assert device.get_comfort_temperature() == 20.5
        device._fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {"ain": "12345", "switchcmd": "gethkrkomfort", "sid": None},
        )

    def test_hkr_without_temperature_values(self):
        self.mock.side_effect = [
            Helper.response("thermostat/device_hkr_no_temp_values"),
        ]

        element = self.fritz.get_device_element("11960 0071472")
        device = FritzhomeDevice(node=element)

        assert device.ain == "11960 0071472"
        assert device.offset is None
        assert device.temperature is None

    def test_hkr_get_state_on(self):
        self.mock.side_effect = [
            Helper.response("thermostat/device_hkr_state_on"),
            Helper.response("thermostat/device_hkr_state_on"),
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345")
        assert device.get_hkr_state() == "on"

    def test_hkr_get_state_off(self):
        self.mock.side_effect = [
            Helper.response("thermostat/device_hkr_state_off"),
            Helper.response("thermostat/device_hkr_state_off"),
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345")
        assert device.get_hkr_state() == "off"

    def test_hkr_get_state_eco(self):
        self.mock.side_effect = [
            Helper.response("thermostat/device_hkr_state_eco"),
            Helper.response("thermostat/device_hkr_state_eco"),
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345")
        assert device.get_hkr_state() == "eco"

    def test_hkr_get_state_comfort(self):
        self.mock.side_effect = [
            Helper.response("thermostat/device_hkr_state_comfort"),
            Helper.response("thermostat/device_hkr_state_comfort"),
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345")
        assert device.get_hkr_state() == "comfort"

    def test_hkr_get_state_manual(self):
        self.mock.side_effect = [
            Helper.response("thermostat/device_hkr_state_manual"),
            Helper.response("thermostat/device_hkr_state_manual"),
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345")
        assert device.get_hkr_state() == "manual"

    def test_hkr_set_state_on(self):
        self.mock.side_effect = [
            Helper.response("thermostat/device_hkr_state_manual"),
            Helper.response("thermostat/device_hkr_state_manual"),
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345")

        device.set_hkr_state("on")
        device._fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {"ain": "12345", "switchcmd": "sethkrtsoll", "param": 254, "sid": None},
        )

    def test_hkr_set_state_off(self):
        self.mock.side_effect = [
            Helper.response("thermostat/device_hkr_state_manual"),
            Helper.response("thermostat/device_hkr_state_manual"),
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345")

        device.set_hkr_state("off")
        device._fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {"ain": "12345", "switchcmd": "sethkrtsoll", "param": 253, "sid": None},
        )

    def test_hkr_battery_level(self):
        self.mock.side_effect = [Helper.response("thermostat/device_hkr_fritzos_7")]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345")
        assert device.battery_level == 70

    def test_hkr_window_open(self):
        self.mock.side_effect = [Helper.response("thermostat/device_hkr_fritzos_7")]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345")
        assert not device.window_open

    def test_hkr_summer_active(self):
        self.mock.side_effect = [Helper.response("thermostat/device_hkr_fritzos_7")]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345")
        assert device.summer_active

    def test_hkr_holiday_active(self):
        self.mock.side_effect = [Helper.response("thermostat/device_hkr_fritzos_7")]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345")
        assert not device.holiday_active

    def test_hkr_nextchange_endperiod(self):
        self.mock.side_effect = [Helper.response("thermostat/device_hkr_fritzos_7")]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345")
        assert device.nextchange_endperiod == 1538341200

    def test_hkr_nextchange_temperature(self):
        self.mock.side_effect = [Helper.response("thermostat/device_hkr_fritzos_7")]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345")
        assert device.nextchange_temperature == 21.0
