#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import eq_, assert_true

from .abstractdevicetest import AbstractTestDevice


class TestAlarmDevice(AbstractTestDevice):
    def test_magenta_smoke_alarm(self):
        self.mock.side_effect = [
            self.response("device_magenta_smoke_alarm"),
        ]
        device = self.fritz.get_device_by_ain("11324 0244498-1")
        assert_true(device.present)
        eq_(device.alert_state, None)

    def test_device_alert_on(self):
        self.mock.side_effect = [
            self.response("device_alert_on"),
        ]

        device = self.fritz.get_device_by_ain("05333 0077045-1")
        assert_true(device.present)
        eq_(device.alert_state, True)

    def test_device_alert_off(self):
        self.mock.side_effect = [
            self.response("device_alert_off"),
        ]

        device = self.fritz.get_device_by_ain("05333 0077045-2")
        assert_true(device.present)
        eq_(device.alert_state, False)

    def test_device_alert_no_alertstate(self):
        self.mock.side_effect = [
            self.response("device_alert_no_alertstate"),
        ]

        device = self.fritz.get_device_by_ain("05333 0077045-3")
        assert_true(device.present)
        eq_(device.alert_state, None)
