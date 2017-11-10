#!/usr/bin/env python

from nose.tools import eq_, assert_true, assert_false
from mock import MagicMock

from pyfritzhome import (FritzhomeDevice, Fritzhome)

from .elements import (device_list_xml, device_list_battery_ok_xml,
                       device_list_battery_low_xml, device_not_present_xml,
                       device_no_devicelock_element_xml)


def get_switch_test_device():
    mock = MagicMock()
    mock.side_effect = [
        device_list_xml,
        '1'
    ]

    fritz = Fritzhome('10.0.0.1', 'user', 'pass')
    fritz._request = mock
    element = fritz.get_device_element('08761 0000434')
    device = FritzhomeDevice(fritz=fritz, node=element)
    return device

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
        assert_true(device.present)
        assert_true(device.has_switch)
        assert_true(device.has_temperature_sensor)
        assert_true(device.has_powermeter)

    def test_device_init_present_false(self):
        mock = MagicMock()
        mock.side_effect = [
            device_not_present_xml,
        ]

        fritz = Fritzhome('10.0.0.1', 'user', 'pass')
        fritz._request = mock
        element = fritz.get_device_element('11960 0089208')
        device = FritzhomeDevice(node=element)

        eq_(device.ain, '11960 0089208')
        assert_false(device.present)

    def test_device_init_no_devicelock_element(self):
        mock = MagicMock()
        mock.side_effect = [
            device_no_devicelock_element_xml,
        ]

        fritz = Fritzhome('10.0.0.1', 'user', 'pass')
        fritz._request = mock
        element = fritz.get_device_element('08761 0373130')
        device = FritzhomeDevice(node=element)

        eq_(device.ain, '08761 0373130')
        assert_true(device.present)

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

    def test_get_device_present(self):
        mock = MagicMock()
        mock.side_effect = [
            '1',
            '0'
        ]

        device = get_switch_test_device()
        device._fritz._request = mock

        assert_true(device.get_present())
        assert_false(device.get_present())
        device._fritz._request.assert_called_with(
            'http://10.0.0.1/webservices/homeautoswitch.lua',
             { 'ain': u'08761 0000434', 'switchcmd':
             'getswitchpresent', 'sid': None})

    def test_get_switch_state(self):
        mock = MagicMock()
        mock.side_effect = [
            '1',
            '0'
        ]

        device = get_switch_test_device()
        device._fritz._request = mock

        assert_true(device.get_switch_state())
        assert_false(device.get_switch_state())
        device._fritz._request.assert_called_with(
            'http://10.0.0.1/webservices/homeautoswitch.lua',
             { 'ain': u'08761 0000434', 'switchcmd':
             'getswitchstate', 'sid': None})

    def test_set_switch_state(self):
        mock = MagicMock()
        #mock.side_effect = [
        #    True,
        #    True,
        #]

        device = get_switch_test_device()
        device._fritz._request = mock

        device.set_switch_state_on()
        device._fritz._request.assert_called_with(
            'http://10.0.0.1/webservices/homeautoswitch.lua',
             { 'ain': u'08761 0000434', 'switchcmd':
             'setswitchon', 'sid': None})

        device.set_switch_state_off()
        device._fritz._request.assert_called_with(
            'http://10.0.0.1/webservices/homeautoswitch.lua',
             { 'ain': u'08761 0000434', 'switchcmd':
             'setswitchoff', 'sid': None})

        device.set_switch_state_toggle()
        device._fritz._request.assert_called_with(
            'http://10.0.0.1/webservices/homeautoswitch.lua',
             { 'ain': u'08761 0000434', 'switchcmd':
             'setswitchtoggle', 'sid': None})

    def test_get_switch_power(self):
        mock = MagicMock()
        mock.side_effect = [
            '18000',
        ]

        device = get_switch_test_device()
        device._fritz._request = mock

        eq_(device.get_switch_power(), 18000)
        device._fritz._request.assert_called_with(
            'http://10.0.0.1/webservices/homeautoswitch.lua',
             { 'ain': u'08761 0000434', 'switchcmd':
             'getswitchpower', 'sid': None})

    def test_get_switch_energy(self):
        mock = MagicMock()
        mock.side_effect = [
            '2000',
        ]

        device = get_switch_test_device()
        device._fritz._request = mock

        eq_(device.get_switch_energy(), 2000)
        device._fritz._request.assert_called_with(
            'http://10.0.0.1/webservices/homeautoswitch.lua',
             { 'ain': u'08761 0000434', 'switchcmd':
             'getswitchenergy', 'sid': None})

    def test_get_temperature(self):
        mock = MagicMock()
        mock.side_effect = [
            '245',
        ]

        device = get_switch_test_device()
        device._fritz._request = mock

        eq_(device.get_temperature(), 24.5)
        device._fritz._request.assert_called_with(
            'http://10.0.0.1/webservices/homeautoswitch.lua',
             { 'ain': u'08761 0000434', 'switchcmd':
             'gettemperature', 'sid': None})

    def test_get_target_temperature(self):
        mock = MagicMock()
        mock.side_effect = [
            '38',
        ]

        device = get_switch_test_device()
        device._fritz._request = mock

        eq_(device.get_target_temperature(), 19.0)
        device._fritz._request.assert_called_with(
            'http://10.0.0.1/webservices/homeautoswitch.lua',
             { 'ain': u'08761 0000434', 'switchcmd':
             'gethkrtsoll', 'sid': None})

    def test_get_eco_temperature(self):
        mock = MagicMock()
        mock.side_effect = [
            '40',
        ]

        device = get_switch_test_device()
        device._fritz._request = mock

        eq_(device.get_eco_temperature(), 20.0)
        device._fritz._request.assert_called_with(
            'http://10.0.0.1/webservices/homeautoswitch.lua',
             { 'ain': u'08761 0000434', 'switchcmd':
             'gethkrabsenk', 'sid': None})

    def test_get_comfort_temperature(self):
        mock = MagicMock()
        mock.side_effect = [
            '41',
        ]

        device = get_switch_test_device()
        device._fritz._request = mock

        eq_(device.get_comfort_temperature(), 20.5)
        device._fritz._request.assert_called_with(
            'http://10.0.0.1/webservices/homeautoswitch.lua',
             { 'ain': u'08761 0000434', 'switchcmd':
             'gethkrkomfort', 'sid': None})
