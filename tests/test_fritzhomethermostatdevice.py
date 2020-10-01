#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import eq_, assert_true
from pyfritzhome import FritzhomeDevice

from .abstractdevicetest import AbstractTestDevice


class TestThermostatDevice(AbstractTestDevice):
    def test_device_hkr_fw_03_50(self):
        self.mock.side_effect = [
            self.response("device_hkr_fw_03_50"),
        ]

        device = self.fritz.get_device_by_ain("12345")
        assert_true(device.present)
        eq_(device.device_lock, None)
        eq_(device.lock, None)
        eq_(device.error_code, None)
        eq_(device.battery_low, None)

    def test_device_hkr_fw_03_54(self):
        self.mock.side_effect = [
            self.response("device_hkr_fw_03_54"),
        ]

        device = self.fritz.get_device_by_ain("23456")
        assert_true(device.present)

    def test_get_target_temperature(self):
        device = self.get_switch_test_device()
        device._fritz._request.side_effect = [
            "38",
        ]

        eq_(device.get_target_temperature(), 19.0)
        device._fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {"ain": u"08761 0000434", "switchcmd": "gethkrtsoll", "sid": None},
        )

    def test_get_eco_temperature(self):
        device = self.get_switch_test_device()
        device._fritz._request.side_effect = [
            "40",
        ]

        eq_(device.get_eco_temperature(), 20.0)
        device._fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {"ain": u"08761 0000434", "switchcmd": "gethkrabsenk", "sid": None},
        )

    def test_get_comfort_temperature(self):
        device = self.get_switch_test_device()
        device._fritz._request.side_effect = [
            "41",
        ]

        eq_(device.get_comfort_temperature(), 20.5)
        device._fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {"ain": u"08761 0000434", "switchcmd": "gethkrkomfort", "sid": None},
        )

    def test_hkr_without_temperature_values(self):
        self.mock.side_effect = [
            self.response("device_hkr_no_temp_values"),
        ]

        element = self.fritz.get_device_element("11960 0071472")
        device = FritzhomeDevice(node=element)

        eq_(device.ain, "11960 0071472")
        eq_(device.offset, None)
        eq_(device.temperature, None)

    def test_hkr_get_state_on(self):
        self.mock.side_effect = [
            self.response("device_hkr_state_on"),
            self.response("device_hkr_state_on"),
        ]

        device = self.fritz.get_device_by_ain("12345")
        eq_(device.get_hkr_state(), "on")

    def test_hkr_get_state_off(self):
        self.mock.side_effect = [
            self.response("device_hkr_state_off"),
            self.response("device_hkr_state_off"),
        ]

        device = self.fritz.get_device_by_ain("12345")
        eq_(device.get_hkr_state(), "off")

    def test_hkr_get_state_eco(self):
        self.mock.side_effect = [
            self.response("device_hkr_state_eco"),
            self.response("device_hkr_state_eco"),
        ]

        device = self.fritz.get_device_by_ain("12345")
        eq_(device.get_hkr_state(), "eco")

    def test_hkr_get_state_comfort(self):
        self.mock.side_effect = [
            self.response("device_hkr_state_comfort"),
            self.response("device_hkr_state_comfort"),
        ]

        device = self.fritz.get_device_by_ain("12345")
        eq_(device.get_hkr_state(), "comfort")

    def test_hkr_get_state_manual(self):
        self.mock.side_effect = [
            self.response("device_hkr_state_manual"),
            self.response("device_hkr_state_manual"),
        ]

        device = self.fritz.get_device_by_ain("12345")
        eq_(device.get_hkr_state(), "manual")

    def test_hkr_set_state_on(self):
        self.mock.side_effect = [
            self.response("device_hkr_state_manual"),
            self.response("device_hkr_state_manual"),
        ]

        device = self.fritz.get_device_by_ain("12345")

        device.set_hkr_state("on")
        device._fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {"ain": u"12345", "switchcmd": "sethkrtsoll", "param": 254, "sid": None},
        )

    def test_hkr_set_state_off(self):
        self.mock.side_effect = [
            self.response("device_hkr_state_manual"),
            self.response("device_hkr_state_manual"),
        ]

        device = self.fritz.get_device_by_ain("12345")

        device.set_hkr_state("off")
        device._fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {"ain": u"12345", "switchcmd": "sethkrtsoll", "param": 253, "sid": None},
        )

    def test_hkr_battery_level(self):
        self.mock.side_effect = [self.response("device_hkr_fritzos_7")]

        device = self.fritz.get_device_by_ain("12345")
        eq_(device.battery_level, 70)

    def test_hkr_window_open(self):
        self.mock.side_effect = [self.response("device_hkr_fritzos_7")]

        device = self.fritz.get_device_by_ain("12345")
        eq_(device.window_open, False)

    def test_hkr_summer_active(self):
        self.mock.side_effect = [self.response("device_hkr_fritzos_7")]

        device = self.fritz.get_device_by_ain("12345")
        eq_(device.summer_active, True)

    def test_hkr_holiday_active(self):
        self.mock.side_effect = [self.response("device_hkr_fritzos_7")]

        device = self.fritz.get_device_by_ain("12345")
        eq_(device.holiday_active, False)
