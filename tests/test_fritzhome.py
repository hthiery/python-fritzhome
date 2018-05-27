# -*- coding: utf-8 -*-

from nose.tools import eq_, raises
from mock import MagicMock

from pyfritzhome import (Fritzhome, InvalidError, LoginError)

from .elements import (device_list_xml, login_rsp_without_valid_sid,
                       login_rsp_with_valid_sid)


class TestFritzhome(object):

    def setup(self):
        self.mock = MagicMock()
        self.fritz = Fritzhome('10.0.0.1', 'user', 'pass')
        self.fritz._request = self.mock

    @raises(LoginError)
    def test_login_fail(self):
        self.mock.side_effect = [
            login_rsp_without_valid_sid,
            login_rsp_without_valid_sid,
        ]

        self.fritz.login()

    def test_login(self):
        self.mock.side_effect = [
            login_rsp_without_valid_sid,
            login_rsp_with_valid_sid,
        ]

        self.fritz.login()

    def test_logout(self):
        self.fritz.logout()
        self.fritz._request.assert_called_with(
            'http://10.0.0.1/login_sid.lua',
            {'sid': None, 'security:command/logout': '1'})

    def test_aha_request(self):
        self.fritz._aha_request(cmd='testcmd')
        self.fritz._request.assert_called_with(
            'http://10.0.0.1/webservices/homeautoswitch.lua',
            {'sid': None, 'switchcmd': 'testcmd'})

        self.fritz._aha_request(cmd='testcmd', ain='1')
        self.fritz._request.assert_called_with(
            'http://10.0.0.1/webservices/homeautoswitch.lua',
            {'sid': None, 'switchcmd': 'testcmd', 'ain': '1'})

        self.fritz._aha_request(cmd='testcmd', ain='1',
                                param={'a': '1', 'b': '2'})
        self.fritz._request.assert_called_with(
            'http://10.0.0.1/webservices/homeautoswitch.lua',
            {'sid': None, 'switchcmd': 'testcmd', 'ain': '1',
             'param': {'a': '1', 'b': '2'}})

    @raises(InvalidError)
    def test_aha_request_invalid(self):
        self.mock.side_effect = [
            'inval',
        ]

        self.fritz._aha_request(cmd='estcmd')

    def test_get_device_element(self):
        self.mock.side_effect = [
            device_list_xml,
            device_list_xml,
            device_list_xml,
        ]

        element = self.fritz.get_device_element('08761 0000434')
        eq_(element.getAttribute('identifier'), '08761 0000434')
        eq_(element.getAttribute('fwversion'), '03.33')

        element = self.fritz.get_device_element('08761 1048079')
        eq_(element.getAttribute('identifier'), '08761 1048079')
        eq_(element.getAttribute('fwversion'), '03.44')

        element = self.fritz.get_device_element('unknown')
        eq_(element, None)

    def test_get_device_by_ain(self):
        self.mock.side_effect = [
            device_list_xml,
            device_list_xml,
        ]

        device = self.fritz.get_device_by_ain('08761 0000434')
        eq_(device.ain, '08761 0000434')

    def test_aha_get_devices(self):
        self.mock.side_effect = [
            device_list_xml,
        ]

        devices = self.fritz.get_devices()
        eq_(devices[0].name, 'Steckdose')
        eq_(devices[1].name, 'FRITZ!DECT Rep 100 #1')

    def test_get_device_name(self):
        self.mock.side_effect = [
            'testname'
        ]

        eq_(self.fritz.get_device_name(ain='1234'), 'testname')

        self.fritz._request.assert_called_with(
            'http://10.0.0.1/webservices/homeautoswitch.lua',
            {'sid': None, 'ain': '1234', 'switchcmd': 'getswitchname'})

    def test_set_target_temperature(self):
        self.fritz.set_target_temperature('1', 25.5)
        self.fritz._request.assert_called_with(
            'http://10.0.0.1/webservices/homeautoswitch.lua',
            {'sid': None, 'ain': '1', 'switchcmd': 'sethkrtsoll', 'param': 51}
        )

        self.fritz.set_target_temperature('1', 0.0)
        self.fritz._request.assert_called_with(
            'http://10.0.0.1/webservices/homeautoswitch.lua',
            {'sid': None, 'ain': '1', 'switchcmd': 'sethkrtsoll', 'param': 253}
        )

        self.fritz.set_target_temperature('1', 32.0)
        self.fritz._request.assert_called_with(
            'http://10.0.0.1/webservices/homeautoswitch.lua',
            {'sid': None, 'ain': '1', 'switchcmd': 'sethkrtsoll', 'param': 254}
        )

    def test_get_alert_state(self):
        self.mock.side_effect = [
            device_list_xml,
        ]

        eq_(self.fritz.get_alert_state('05333 0077045-1'), True)
