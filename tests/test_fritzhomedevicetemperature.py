#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import eq_
from unittest.mock import MagicMock
from .helper import Helper

from pyfritzhome import Fritzhome


class TestFritzhomeDeviceTemperature(object):
    def setup(self):
        self.mock = MagicMock()
        self.fritz = Fritzhome("10.0.0.1", "user", "pass")
        self.fritz._request = self.mock
        self.fritz._devices = {}

    def test_get_temperature(self):
        self.mock.side_effect = [
            Helper.response("thermostat/device_hkr_fritzos_7"),
            "245",
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345")

        eq_(device.get_temperature(), 24.5)
        device._fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {"ain": "12345", "switchcmd": "gettemperature", "sid": None},
        )
