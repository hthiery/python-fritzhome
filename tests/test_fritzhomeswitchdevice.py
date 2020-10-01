#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import eq_, assert_true, assert_false


from .abstractdevicetest import AbstractTestDevice


class TestSwitchDevice(AbstractTestDevice):
    def test_get_switch_state(self):
        device = self.get_switch_test_device()
        device._fritz._request.side_effect = ["1", "0"]

        assert_true(device.get_switch_state())
        assert_false(device.get_switch_state())
        device._fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {"ain": u"08761 0000434", "switchcmd": "getswitchstate", "sid": None},
        )

    def test_set_switch_state(self):
        device = self.get_switch_test_device()
        device._fritz._request.side_effect = [0, 0, 0]

        device.set_switch_state_on()
        device._fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {"ain": u"08761 0000434", "switchcmd": "setswitchon", "sid": None},
        )

        device.set_switch_state_off()
        device._fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {"ain": u"08761 0000434", "switchcmd": "setswitchoff", "sid": None},
        )

        device.set_switch_state_toggle()
        device._fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {"ain": u"08761 0000434", "switchcmd": "setswitchtoggle", "sid": None},
        )

    def test_get_switch_power(self):
        device = self.get_switch_test_device()
        device._fritz._request.side_effect = [
            "18000",
        ]

        eq_(device.get_switch_power(), 18000)
        device._fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {"ain": u"08761 0000434", "switchcmd": "getswitchpower", "sid": None},
        )

    def test_get_switch_energy(self):
        device = self.get_switch_test_device()
        device._fritz._request.side_effect = [
            "2000",
        ]

        eq_(device.get_switch_energy(), 2000)
        device._fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {"ain": u"08761 0000434", "switchcmd": "getswitchenergy", "sid": None},
        )
