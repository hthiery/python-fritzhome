#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest.mock import MagicMock

from pyfritzhome import Fritzhome
from pyfritzhome.devicetypes.fritzhomedevicefeatures import FritzhomeDeviceFeatures

from .helper import Helper


class TestFritzhomeDeviceAlarm(object):
    def setup_method(self):
        self.mock = MagicMock()
        self.fritz = Fritzhome("10.0.0.1", "user", "pass")
        self.fritz._request = self.mock
        self.fritz._devices = {}
        self.fritz._sid = "0000001"

    def test_device_alert_on(self):
        self.mock.side_effect = [
            Helper.response("alarm/device_alert_on"),
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("05333 0077045-1")
        assert device.present
        assert device.alert_state
        assert device.supported_features == [
            FritzhomeDeviceFeatures.ALARM,
            FritzhomeDeviceFeatures.HANFUN_UNIT,
        ]

    def test_device_alert_off(self):
        self.mock.side_effect = [
            Helper.response("alarm/device_alert_off"),
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("05333 0077045-2")
        assert device.present
        assert not device.alert_state

    def test_device_alert_no_alertstate(self):
        self.mock.side_effect = [
            Helper.response("alarm/device_alert_no_alertstate"),
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("05333 0077045-3")
        assert device.present
        assert device.alert_state is None

    def test_magenta_smoke_alarm(self):
        self.mock.side_effect = [
            Helper.response("alarm/device_magenta_smoke_alarm"),
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("11324 0244498-1")
        assert device.present
        assert device.alert_state is None
