#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest.mock import MagicMock

from pyfritzhome import Fritzhome
from pyfritzhome.devicetypes.fritzhomedevicefeatures import FritzhomeDeviceFeatures

from .helper import Helper


class TestFritzhomeDeviceButton(object):
    def setup_method(self):
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
        assert device.present
        assert device.alert_state is None
        assert device.has_temperature_sensor
        assert device.has_button
        assert not device.battery_low
        assert device.battery_level == 100
        assert not device.tx_busy
        assert device.supported_features == [
            FritzhomeDeviceFeatures.BUTTON,
            FritzhomeDeviceFeatures.TEMPERATURE,
        ]

        button = device.get_button_by_ain("12345 0000001-1")
        assert button.name == "Taster Wohnzimmer: Oben rechts"
        assert button.last_pressed == 1608557681

        button = device.get_button_by_ain("12345 0000001-2")
        assert button.name == "Taster Wohnzimmer: Unten rechts"
        assert button.last_pressed == 1608557682

    def test_button_fritzdect440_humidity(self):
        self.mock.side_effect = [
            Helper.response("button/device_button_fritzdect440_fw_05_10"),
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345 0000002")
        assert device.present
        assert device.rel_humidity == 44
