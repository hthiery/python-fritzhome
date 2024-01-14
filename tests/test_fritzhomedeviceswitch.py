#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest.mock import MagicMock

from pyfritzhome import Fritzhome
from pyfritzhome.devicetypes.fritzhomedevicefeatures import FritzhomeDeviceFeatures

from .helper import Helper


class TestFritzhomeDeviceSwitch(object):
    def setup_method(self):
        self.mock = MagicMock()
        self.fritz = Fritzhome("10.0.0.1", "user", "pass")
        self.fritz._request = self.mock
        self.fritz._devices = {}

    def test_get_switch_state(self):
        self.mock.side_effect = [
            Helper.response("switch/device_list"),
            "1",
            "0",
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("08761 0000434")

        assert device.get_switch_state()
        assert not device.get_switch_state()
        assert device.supported_features == [
            FritzhomeDeviceFeatures.POWER_METER,
            FritzhomeDeviceFeatures.TEMPERATURE,
            FritzhomeDeviceFeatures.SWITCH,
        ]
        device._fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {"ain": "08761 0000434", "switchcmd": "getswitchstate", "sid": None},
        )

    def test_set_switch_state_toggle(self):
        self.mock.side_effect = [
            Helper.response("switch/device_list"),
            "1",
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("08761 0000434")

        device.set_switch_state_toggle()
        device._fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {"ain": "08761 0000434", "switchcmd": "setswitchtoggle", "sid": None},
        )

    def test_set_switch_state_on(self):
        self.mock.side_effect = [
            Helper.response("switch/device_list"),
            "1",
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("08761 0000434")

        device.set_switch_state_on()
        device._fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {"ain": "08761 0000434", "switchcmd": "setswitchon", "sid": None},
        )

    def test_set_switch_state_off(self):
        self.mock.side_effect = [
            Helper.response("switch/device_list"),
            "1",
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("08761 0000434")

        device.set_switch_state_off()
        device._fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {"ain": "08761 0000434", "switchcmd": "setswitchoff", "sid": None},
        )
