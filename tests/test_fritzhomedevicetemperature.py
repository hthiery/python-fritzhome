#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest.mock import MagicMock

from pyfritzhome import Fritzhome
from pyfritzhome.devicetypes.fritzhomedevicefeatures import FritzhomeDeviceFeatures

from .helper import Helper


class TestFritzhomeDeviceTemperature(object):
    def setup_method(self):
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

        assert device.get_temperature() == 24.5
        assert device.supported_features == [
            FritzhomeDeviceFeatures.THERMOSTAT,
            FritzhomeDeviceFeatures.TEMPERATURE,
        ]
        device._fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {"ain": "12345", "switchcmd": "gettemperature", "sid": None},
        )
