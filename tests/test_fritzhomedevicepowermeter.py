#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest.mock import MagicMock

from pyfritzhome import Fritzhome
from pyfritzhome.devicetypes.fritzhomedevicefeatures import FritzhomeDeviceFeatures

from .helper import Helper


class TestFritzhomeDevicePowermeter(object):
    def setup_method(self):
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

        assert device.get_switch_power() == 18000
        assert device.supported_features == [
            FritzhomeDeviceFeatures.POWER_METER,
            FritzhomeDeviceFeatures.TEMPERATURE,
            FritzhomeDeviceFeatures.SWITCH,
        ]
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

        assert device.get_switch_energy() == 2000
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

        assert device.energy == 707
        assert device.power == 1000
        assert device.voltage == 230000
        assert device.current == 4.3478260869565215

    def test_faulty_powermeter_properties(self):
        self.mock.side_effect = [
            Helper.response("powermeter/device_list_faulty"),
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("08761 0000434")

        assert device.energy == 0
        assert device.power == 0
        assert device.voltage == 0
        assert device.current is None
