#!/usr/bin/env python

from nose.tools import eq_, assert_true, assert_false
from mock import MagicMock

from pyfritzhome import (FritzhomeDevice, Fritzhome)

from .elements import (device_list_xml, device_list_battery_ok_xml,
                       device_list_battery_low_xml)


class TestDevice(object):

    def test_device_init(self):
        mock = MagicMock()
        mock.side_effect = [
            device_list_xml,
        ]

        fritz = Fritzhome('10.0.0.1', 'user', 'pass')
        fritz._request = mock
        element = fritz.get_device_element('08761 0000434')
        device = FritzhomeDevice(node=element)

        eq_(device.ain, '08761 0000434')
        eq_(device.fw_version, '03.33')
        assert_true(device.has_switch)
        assert_true(device.has_temperature_sensor)
        assert_true(device.has_powermeter)

    def test_device_update(self):
        mock = MagicMock()
        mock.side_effect = [
            device_list_battery_ok_xml,
            device_list_battery_low_xml,
        ]

        fritz = Fritzhome('10.0.0.1', 'user', 'pass')
        fritz._request = mock
        element = fritz.get_device_element('11959 0171328')
        device = FritzhomeDevice(fritz=fritz, node=element)

        assert_false(device.battery_low)
        device.update()
        assert_true(device.battery_low)
