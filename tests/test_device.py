#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import eq_, assert_true, assert_false
from mock import MagicMock

from pyfritzhome import (FritzhomeDevice, Fritzhome)

from .elements import (device_list_xml, device_list_battery_ok_xml,
                       device_list_battery_low_xml, device_not_present_xml,
                       device_no_devicelock_element_xml,
                       device_with_umlaut_in_name_xml,
                       device_hkr_fw_03_50_xml, device_hkr_fw_03_54_xml,
                       device_hkr_no_temp_values_xml, device_alert_on_xml,
                       device_alert_off_xml, device_alert_no_alertstate_xml,
                       device_hkr_state_on_xml, device_hkr_state_off_xml,
                       device_hkr_state_eco_xml, device_hkr_state_comfort_xml,
                       device_hkr_state_manual_xml, device_hkr_fritzos_7_xml)


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

    def setup(self):
        self.mock = MagicMock()
        self.fritz = Fritzhome('10.0.0.1', 'user', 'pass')
        self.fritz._request = self.mock

    def test_device_init(self):
        self.mock.side_effect = [
            device_list_xml,
        ]

        device = self.fritz.get_device_by_ain('08761 0000434')

        eq_(device.ain, '08761 0000434')
        eq_(device.fw_version, '03.33')
        assert_true(device.present)
        assert_true(device.has_switch)
        assert_true(device.has_temperature_sensor)
        assert_true(device.has_powermeter)

    def test_device_init_present_false(self):
        self.mock.side_effect = [
            device_not_present_xml,
        ]

        device = self.fritz.get_device_by_ain('11960 0089208')

        eq_(device.ain, '11960 0089208')
        assert_false(device.present)

    def test_device_init_no_devicelock_element(self):
        self.mock.side_effect = [
            device_no_devicelock_element_xml,
        ]

        device = self.fritz.get_device_by_ain('08761 0373130')

        eq_(device.ain, '08761 0373130')
        assert_true(device.present)

    def test_device_umlaut(self):
        self.mock.side_effect = [
            device_with_umlaut_in_name_xml,
        ]

        device = self.fritz.get_device_by_ain('08761 0373130')

        eq_(device.ain, '08761 0373130')
        eq_(device.name, u'äöü')

    def test_device_hkr_fw_03_50(self):
        self.mock.side_effect = [
            device_hkr_fw_03_50_xml,
        ]

        device = self.fritz.get_device_by_ain('12345')
        assert_true(device.present)
        eq_(device.device_lock, None)
        eq_(device.lock, None)
        eq_(device.error_code, None)
        eq_(device.battery_low, None)

    def test_device_hkr_fw_03_54(self):
        self.mock.side_effect = [
            device_hkr_fw_03_54_xml,
        ]

        device = self.fritz.get_device_by_ain('23456')
        assert_true(device.present)

    def test_device_alert_on(self):
        self.mock.side_effect = [
            device_alert_on_xml,
        ]

        device = self.fritz.get_device_by_ain('05333 0077045-1')
        assert_true(device.present)
        eq_(device.alert_state, True)

    def test_device_alert_off(self):
        self.mock.side_effect = [
            device_alert_off_xml,
        ]

        device = self.fritz.get_device_by_ain('05333 0077045-2')
        assert_true(device.present)
        eq_(device.alert_state, False)

    def test_device_alert_no_alertstate(self):
        self.mock.side_effect = [
            device_alert_no_alertstate_xml,
        ]

        device = self.fritz.get_device_by_ain('05333 0077045-3')
        assert_true(device.present)
        eq_(device.alert_state, None)

    def test_device_update(self):
        self.mock.side_effect = [
            device_list_battery_ok_xml,
            device_list_battery_low_xml,
        ]

        device = self.fritz.get_device_by_ain('11959 0171328')
        assert_false(device.battery_low)
        device.update()
        assert_true(device.battery_low)

    def test_get_device_present(self):
        self.mock.side_effect = [
            '1',
            '0'
        ]

        device = get_switch_test_device()
        device._fritz._request = self.mock

        assert_true(device.get_present())
        assert_false(device.get_present())
        device._fritz._request.assert_called_with(
            'http://10.0.0.1/webservices/homeautoswitch.lua',
            {'ain': u'08761 0000434', 'switchcmd':
             'getswitchpresent', 'sid': None})

    def test_get_switch_state(self):
        self.mock.side_effect = [
            '1',
            '0'
        ]

        device = get_switch_test_device()
        device._fritz._request = self.mock

        assert_true(device.get_switch_state())
        assert_false(device.get_switch_state())
        device._fritz._request.assert_called_with(
            'http://10.0.0.1/webservices/homeautoswitch.lua',
            {'ain': u'08761 0000434', 'switchcmd':
             'getswitchstate', 'sid': None})

    def test_set_switch_state(self):
        device = get_switch_test_device()
        device._fritz._request = self.mock

        device.set_switch_state_on()
        device._fritz._request.assert_called_with(
            'http://10.0.0.1/webservices/homeautoswitch.lua',
            {'ain': u'08761 0000434', 'switchcmd':
             'setswitchon', 'sid': None})

        device.set_switch_state_off()
        device._fritz._request.assert_called_with(
            'http://10.0.0.1/webservices/homeautoswitch.lua',
            {'ain': u'08761 0000434', 'switchcmd':
             'setswitchoff', 'sid': None})

        device.set_switch_state_toggle()
        device._fritz._request.assert_called_with(
            'http://10.0.0.1/webservices/homeautoswitch.lua',
            {'ain': u'08761 0000434', 'switchcmd':
             'setswitchtoggle', 'sid': None})

    def test_get_switch_power(self):
        self.mock.side_effect = [
            '18000',
        ]

        device = get_switch_test_device()
        device._fritz._request = self.mock

        eq_(device.get_switch_power(), 18000)
        device._fritz._request.assert_called_with(
            'http://10.0.0.1/webservices/homeautoswitch.lua',
            {'ain': u'08761 0000434', 'switchcmd':
             'getswitchpower', 'sid': None})

    def test_get_switch_energy(self):
        self.mock.side_effect = [
            '2000',
        ]

        device = get_switch_test_device()
        device._fritz._request = self.mock

        eq_(device.get_switch_energy(), 2000)
        device._fritz._request.assert_called_with(
            'http://10.0.0.1/webservices/homeautoswitch.lua',
            {'ain': u'08761 0000434', 'switchcmd':
             'getswitchenergy', 'sid': None})

    def test_get_temperature(self):
        self.mock.side_effect = [
            '245',
        ]

        device = get_switch_test_device()
        device._fritz._request = self.mock

        eq_(device.get_temperature(), 24.5)
        device._fritz._request.assert_called_with(
            'http://10.0.0.1/webservices/homeautoswitch.lua',
            {'ain': u'08761 0000434', 'switchcmd':
             'gettemperature', 'sid': None})

    def test_get_target_temperature(self):
        self.mock.side_effect = [
            '38',
        ]

        device = get_switch_test_device()
        device._fritz._request = self.mock

        eq_(device.get_target_temperature(), 19.0)
        device._fritz._request.assert_called_with(
            'http://10.0.0.1/webservices/homeautoswitch.lua',
            {'ain': u'08761 0000434', 'switchcmd':
             'gethkrtsoll', 'sid': None})

    def test_get_eco_temperature(self):
        self.mock.side_effect = [
            '40',
        ]

        device = get_switch_test_device()
        device._fritz._request = self.mock

        eq_(device.get_eco_temperature(), 20.0)
        device._fritz._request.assert_called_with(
            'http://10.0.0.1/webservices/homeautoswitch.lua',
            {'ain': u'08761 0000434', 'switchcmd':
             'gethkrabsenk', 'sid': None})

    def test_get_comfort_temperature(self):
        self.mock.side_effect = [
            '41',
        ]

        device = get_switch_test_device()
        device._fritz._request = self.mock

        eq_(device.get_comfort_temperature(), 20.5)
        device._fritz._request.assert_called_with(
            'http://10.0.0.1/webservices/homeautoswitch.lua',
            {'ain': u'08761 0000434', 'switchcmd':
             'gethkrkomfort', 'sid': None})

    def test_hkr_without_temperature_values(self):
        self.mock.side_effect = [
            device_hkr_no_temp_values_xml,
        ]

        element = self.fritz.get_device_element('11960 0071472')
        device = FritzhomeDevice(node=element)

        eq_(device.ain, '11960 0071472')
        eq_(device.offset, None)
        eq_(device.temperature, None)

    def test_hkr_get_state_on(self):
        self.mock.side_effect = [
            device_hkr_state_on_xml,
            device_hkr_state_on_xml,
        ]

        device = self.fritz.get_device_by_ain('12345')
        eq_(device.get_hkr_state(), 'on')

    def test_hkr_get_state_off(self):
        self.mock.side_effect = [
            device_hkr_state_off_xml,
            device_hkr_state_off_xml,
        ]

        device = self.fritz.get_device_by_ain('12345')
        eq_(device.get_hkr_state(), 'off')

    def test_hkr_get_state_eco(self):
        self.mock.side_effect = [
            device_hkr_state_eco_xml,
            device_hkr_state_eco_xml,
        ]

        device = self.fritz.get_device_by_ain('12345')
        eq_(device.get_hkr_state(), 'eco')

    def test_hkr_get_state_comfort(self):
        self.mock.side_effect = [
            device_hkr_state_comfort_xml,
            device_hkr_state_comfort_xml,
        ]

        device = self.fritz.get_device_by_ain('12345')
        eq_(device.get_hkr_state(), 'comfort')

    def test_hkr_get_state_manual(self):
        self.mock.side_effect = [
            device_hkr_state_manual_xml,
            device_hkr_state_manual_xml,
        ]

        device = self.fritz.get_device_by_ain('12345')
        eq_(device.get_hkr_state(), 'manual')

    def test_hkr_set_state_on(self):
        self.mock.side_effect = [
            device_hkr_state_manual_xml,
            device_hkr_state_manual_xml,
        ]

        device = self.fritz.get_device_by_ain('12345')

        device.set_hkr_state('on')
        device._fritz._request.assert_called_with(
            'http://10.0.0.1/webservices/homeautoswitch.lua',
            {'ain': u'12345', 'switchcmd':
             'sethkrtsoll', 'param': 254, 'sid': None})

    def test_hkr_set_state_off(self):
        self.mock.side_effect = [
            device_hkr_state_manual_xml,
            device_hkr_state_manual_xml,
        ]

        device = self.fritz.get_device_by_ain('12345')

        device.set_hkr_state('off')
        device._fritz._request.assert_called_with(
            'http://10.0.0.1/webservices/homeautoswitch.lua',
            {'ain': u'12345', 'switchcmd':
             'sethkrtsoll', 'param': 253, 'sid': None})

    def test_hkr_battery_level(self):
        self.mock.side_effect = [
            device_hkr_fritzos_7_xml
        ]

        device = self.fritz.get_device_by_ain('12345')
        eq_(device.battery_level, 70)

    def test_hkr_window_open(self):
        self.mock.side_effect = [
            device_hkr_fritzos_7_xml
        ]

        device = self.fritz.get_device_by_ain('12345')
        eq_(device.window_open, False)

    def test_hkr_summer_active(self):
        self.mock.side_effect = [
            device_hkr_fritzos_7_xml
        ]

        device = self.fritz.get_device_by_ain('12345')
        eq_(device.summer_active, True)

    def test_hkr_holiday_active(self):
        self.mock.side_effect = [
            device_hkr_fritzos_7_xml
        ]

        device = self.fritz.get_device_by_ain('12345')
        eq_(device.holiday_active, False)
