#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest.mock import MagicMock

from pyfritzhome import Fritzhome

from .helper import Helper


class TestFritzhomeDeviceBase(object):
    def setup_method(self):
        self.mock = MagicMock()
        self.fritz = Fritzhome("10.0.0.1", "user", "pass")
        self.fritz._request = self.mock
        self.fritz._devices = {}

    def test_device_init(self):
        self.mock.side_effect = [Helper.response("base/device_list")]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("08761 0000434")

        assert device.ain == "08761 0000434"
        assert device.fw_version == "03.33"
        assert device.present
        assert device.has_switch
        assert device.has_temperature_sensor
        assert device.has_powermeter

    def test_device_init_present_false(self):
        self.mock.side_effect = [
            Helper.response("base/device_not_present"),
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("11960 0089208")

        assert device.ain == "11960 0089208"
        assert not device.present

    def test_device_init_no_devicelock_element(self):
        self.mock.side_effect = [
            Helper.response("base/device_no_devicelock_element"),
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("08761 0373130")

        assert device.ain == "08761 0373130"
        assert device.present

    def test_device_umlaut(self):
        self.mock.side_effect = [
            Helper.response("base/device_with_umlaut_in_name"),
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("08761 0373130")

        assert device.ain == "08761 0373130"
        assert device.name == "äöü"

    def test_device_update(self):
        self.mock.side_effect = [
            Helper.response("thermostat/device_list_battery_ok"),
            Helper.response("thermostat/device_list_battery_low"),
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("11959 0171328")
        assert not device.battery_low
        device.update()
        assert device.battery_low

    def test_get_device_present(self):
        self.mock.side_effect = [
            Helper.response("base/device_list"),
            "1",
            "0",
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("08761 0000434")

        assert device.get_present()
        assert not device.get_present()
        device._fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {"ain": "08761 0000434", "switchcmd": "getswitchpresent", "sid": None},
        )
