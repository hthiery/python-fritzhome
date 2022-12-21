#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import eq_, assert_true
from unittest.mock import MagicMock
from .helper import Helper

from pyfritzhome import Fritzhome, FritzhomeDevice


class TestFritzhomeDeviceThermostat(object):
    def setup(self):
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
        assert_true(device.present)
        eq_(device.device_lock, None)
        eq_(device.lock, None)
        eq_(device.error_code, None)
        eq_(device.battery_low, None)

    def test_device_hkr_fw_03_54(self):
        self.mock.side_effect = [
            Helper.response("thermostat/device_hkr_fw_03_54"),
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("23456")
        assert_true(device.present)

    def test_get_target_temperature(self):
        self.mock.side_effect = [
            Helper.response("thermostat/device_hkr_fritzos_7"),
            "38",
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345")

        eq_(device.get_target_temperature(), 19.0)
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

        eq_(device.get_eco_temperature(), 20.0)
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

        eq_(device.get_comfort_temperature(), 20.5)
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

        eq_(device.ain, "11960 0071472")
        eq_(device.offset, None)
        eq_(device.temperature, None)

    def test_hkr_get_state_on(self):
        self.mock.side_effect = [
            Helper.response("thermostat/device_hkr_state_on"),
            Helper.response("thermostat/device_hkr_state_on"),
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345")
        eq_(device.get_hkr_state(), "on")

    def test_hkr_get_state_off(self):
        self.mock.side_effect = [
            Helper.response("thermostat/device_hkr_state_off"),
            Helper.response("thermostat/device_hkr_state_off"),
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345")
        eq_(device.get_hkr_state(), "off")

    def test_hkr_get_state_eco(self):
        self.mock.side_effect = [
            Helper.response("thermostat/device_hkr_state_eco"),
            Helper.response("thermostat/device_hkr_state_eco"),
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345")
        eq_(device.get_hkr_state(), "eco")

    def test_hkr_get_state_comfort(self):
        self.mock.side_effect = [
            Helper.response("thermostat/device_hkr_state_comfort"),
            Helper.response("thermostat/device_hkr_state_comfort"),
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345")
        eq_(device.get_hkr_state(), "comfort")

    def test_hkr_get_state_manual(self):
        self.mock.side_effect = [
            Helper.response("thermostat/device_hkr_state_manual"),
            Helper.response("thermostat/device_hkr_state_manual"),
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345")
        eq_(device.get_hkr_state(), "manual")

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
        eq_(device.battery_level, 70)

    def test_hkr_window_open(self):
        self.mock.side_effect = [Helper.response("thermostat/device_hkr_fritzos_7")]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345")
        eq_(device.window_open, False)

    def test_hkr_summer_active(self):
        self.mock.side_effect = [Helper.response("thermostat/device_hkr_fritzos_7")]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345")
        eq_(device.summer_active, True)

    def test_hkr_holiday_active(self):
        self.mock.side_effect = [Helper.response("thermostat/device_hkr_fritzos_7")]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345")
        eq_(device.holiday_active, False)

    def test_hkr_nextchange_endperiod(self):
        self.mock.side_effect = [Helper.response("thermostat/device_hkr_fritzos_7")]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345")
        eq_(device.nextchange_endperiod, 1538341200)

    def test_hkr_nextchange_temperature(self):
        self.mock.side_effect = [Helper.response("thermostat/device_hkr_fritzos_7")]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345")
        eq_(device.nextchange_temperature, 21.0)
