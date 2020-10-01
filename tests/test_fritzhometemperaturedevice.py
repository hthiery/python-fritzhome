#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import eq_

from .abstractdevicetest import AbstractTestDevice


class TestTemperatureDevice(AbstractTestDevice):
    def test_get_temperature(self):
        device = self.get_switch_test_device()
        device._fritz._request.side_effect = [
            "245",
        ]

        eq_(device.get_temperature(), 24.5)
        device._fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {"ain": u"08761 0000434", "switchcmd": "gettemperature", "sid": None},
        )
