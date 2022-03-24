#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import eq_, assert_true, assert_false
from unittest.mock import MagicMock
from .helper import Helper

from pyfritzhome import Fritzhome, FritzhomeDevice


class TestFritzhomeDeviceBlind(object):
    def setup(self):
        self.mock = MagicMock()
        self.fritz = Fritzhome("10.0.0.1", "user", "pass")
        self.fritz._request = self.mock
        self.fritz._devices = {}

    def test_device_response(self):
        self.mock.side_effect = [
            Helper.response("blind/device_blind_rollotron1213"),
        ]

        self.fritz.update_devices()
        device1 = self.fritz.get_device_by_ain("14276 1234567")
        assert_true(device1.present)
        assert_false(device1.tx_busy)
        
        device2 = self.fritz.get_device_by_ain("14276 1234567-1")
        assert_true(device2.present)
        assert_false(device2.tx_busy)
        assert_true(device2.endpositionsset)
        
        eq_(device2.level, 252)
        eq_(device2.levelpercentage, 99)
        
        eq_(device2.get_level(), 252)
        eq_(device2.get_level_percentage(), 99)

    def test_set_level(self):
        self.mock.side_effect = [
            Helper.response("blind/device_blind_rollotron1213"),
            None
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("14276 1234567-1")

        device.set_level(100)
        device._fritz._request.assert_called_with(
           "http://10.0.0.1/webservices/homeautoswitch.lua",
           {"switchcmd": "setlevel", "sid": None, "ain": "14276 1234567-1", "level": 100},
        )

    def test_set_level_percentage(self):
        self.mock.side_effect = [
            Helper.response("blind/device_blind_rollotron1213"),
            None
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("14276 1234567-1")

        device.set_level_percentage(50)
        device._fritz._request.assert_called_with(
           "http://10.0.0.1/webservices/homeautoswitch.lua",
           {"switchcmd": "setlevelpercentage", "sid": None, "ain": "14276 1234567-1", "level": 50},
        )

    def test_set_blind_open(self):
        self.mock.side_effect = [
            Helper.response("blind/device_blind_rollotron1213"),
            None
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("14276 1234567-1")

        device.set_blind_open()
        device._fritz._request.assert_called_with(
           "http://10.0.0.1/webservices/homeautoswitch.lua",
           {"switchcmd": "setblind", "sid": None, "ain": "14276 1234567-1", "target": "open"},
        )

    def test_set_blind_close(self):
        self.mock.side_effect = [
            Helper.response("blind/device_blind_rollotron1213"),
            None
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("14276 1234567-1")

        device.set_blind_close()
        device._fritz._request.assert_called_with(
           "http://10.0.0.1/webservices/homeautoswitch.lua",
           {"switchcmd": "setblind", "sid": None, "ain": "14276 1234567-1", "target": "close"},
        )
        
    def test_set_blind_stop(self):
        self.mock.side_effect = [
            Helper.response("blind/device_blind_rollotron1213"),
            None
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("14276 1234567-1")

        device.set_blind_stop()
        device._fritz._request.assert_called_with(
           "http://10.0.0.1/webservices/homeautoswitch.lua",
           {"switchcmd": "setblind", "sid": None, "ain": "14276 1234567-1", "target": "stop"},
        )
