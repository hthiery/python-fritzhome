#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import eq_
from unittest.mock import MagicMock
from .helper import Helper

from pyfritzhome import Fritzhome


class TestFritzhomeDevicePowermeter(object):
    def setup(self):
        self.mock = MagicMock()
        self.fritz = Fritzhome("10.0.0.1", "user", "pass")
        self.fritz._request = self.mock
        self.fritz._devices = {}

    def test_get_switch_power(self):
        self.mock.side_effect = [
            Helper.response("powermeter/device_list"),
            "18000",
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("08761 0000434")

        eq_(device.get_switch_power(), 18000)
        device._fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {"ain": "08761 0000434", "switchcmd": "getswitchpower", "sid": None},
        )

    def test_get_switch_energy(self):
        self.mock.side_effect = [
            Helper.response("powermeter/device_list"),
            "2000",
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("08761 0000434")

        eq_(device.get_switch_energy(), 2000)
        device._fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {"ain": "08761 0000434", "switchcmd": "getswitchenergy", "sid": None},
        )

    def test_get_switch_powermeter_properties(self):
        self.mock.side_effect = [
            Helper.response("powermeter/device_list"),
            "2000",
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("08761 0000434")

        eq_(device.energy, 707)
        eq_(device.power, 1000)
        eq_(device.voltage, 230000)
        eq_(device.current, 4.3478260869565215)
