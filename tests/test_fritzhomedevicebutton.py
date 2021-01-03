#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import eq_, assert_true, assert_false
from unittest.mock import MagicMock
from .helper import Helper

from pyfritzhome import Fritzhome


class TestFritzhomeDeviceButton(object):
    def setup(self):
        self.mock = MagicMock()
        self.fritz = Fritzhome("10.0.0.1", "user", "pass")
        self.fritz._request = self.mock
        self.fritz._devices = {}

    def test_button_fritzdect440(self):
        self.mock.side_effect = [
            Helper.response("button/device_button_fritzdect440"),
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345 0000001")
        assert_true(device.present)
        eq_(device.alert_state, None)
        assert_true(device.has_temperature_sensor)
        assert_true(device.has_button)
        assert_false(device.battery_low)
        eq_(device.battery_level, 100)
        assert_false(device.tx_busy)

        button = device.get_button_by_ain("12345 0000001-1")
        eq_(button.name, "Taster Wohnzimmer: Oben rechts")
        eq_(button.last_pressed, 1608557681)

        button = device.get_button_by_ain("12345 0000001-2")
        eq_(button.name, "Taster Wohnzimmer: Unten rechts")
        eq_(button.last_pressed, 1608557682)

    def test_button_fritzdect440_humidity(self):
        self.mock.side_effect = [
            Helper.response("button/device_button_fritzdect440_fw_05_10"),
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345 0000002")
        assert_true(device.present)
        eq_(device.rel_humidity, 44)
