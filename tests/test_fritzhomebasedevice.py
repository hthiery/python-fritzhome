#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import eq_, assert_true, assert_false
from .abstractdevicetest import AbstractTestDevice


class TestBaseDevice(AbstractTestDevice):
    def test_device_init(self):
        self.mock.side_effect = [self.response("device_list")]

        device = self.fritz.get_device_by_ain("08761 0000434")

        eq_(device.ain, "08761 0000434")
        eq_(device.fw_version, "03.33")
        assert_true(device.present)
        assert_true(device.has_switch)
        assert_true(device.has_temperature_sensor)
        assert_true(device.has_powermeter)

    def test_device_init_present_false(self):
        self.mock.side_effect = [
            self.response("device_not_present"),
        ]

        device = self.fritz.get_device_by_ain("11960 0089208")

        eq_(device.ain, "11960 0089208")
        assert_false(device.present)

    def test_device_init_no_devicelock_element(self):
        self.mock.side_effect = [
            self.response("device_no_devicelock_element"),
        ]

        device = self.fritz.get_device_by_ain("08761 0373130")

        eq_(device.ain, "08761 0373130")
        assert_true(device.present)

    def test_device_umlaut(self):
        self.mock.side_effect = [
            self.response("device_with_umlaut_in_name"),
        ]

        device = self.fritz.get_device_by_ain("08761 0373130")

        eq_(device.ain, "08761 0373130")
        eq_(device.name, u"äöü")

    def test_device_update(self):
        self.mock.side_effect = [
            self.response("device_list_battery_ok"),
            self.response("device_list_battery_low"),
        ]

        device = self.fritz.get_device_by_ain("11959 0171328")
        assert_false(device.battery_low)
        device.update()
        assert_true(device.battery_low)

    def test_get_device_present(self):
        device = self.get_switch_test_device()
        device._fritz._request.side_effect = ["1", "0"]

        assert_true(device.get_present())
        assert_false(device.get_present())
        device._fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {"ain": u"08761 0000434", "switchcmd": "getswitchpresent", "sid": None},
        )
