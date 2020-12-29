#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import eq_, assert_true
from unittest.mock import MagicMock
from .helper import Helper

from pyfritzhome import Fritzhome


class TestFritzhomeDeviceAlarm(object):
    def setup(self):
        self.mock = MagicMock()
        self.fritz = Fritzhome("10.0.0.1", "user", "pass")
        self.fritz._request = self.mock
        self.fritz._devices = {}

    def test_device_alert_on(self):
        self.mock.side_effect = [
            Helper.response("alarm/device_alert_on"),
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("05333 0077045-1")
        assert_true(device.present)
        eq_(device.alert_state, True)

    def test_device_alert_off(self):
        self.mock.side_effect = [
            Helper.response("alarm/device_alert_off"),
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("05333 0077045-2")
        assert_true(device.present)
        eq_(device.alert_state, False)

    def test_device_alert_no_alertstate(self):
        self.mock.side_effect = [
            Helper.response("alarm/device_alert_no_alertstate"),
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("05333 0077045-3")
        assert_true(device.present)
        eq_(device.alert_state, None)

    def test_magenta_smoke_alarm(self):
        self.mock.side_effect = [
            Helper.response("alarm/device_magenta_smoke_alarm"),
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("11324 0244498-1")
        assert_true(device.present)
        eq_(device.alert_state, None)
