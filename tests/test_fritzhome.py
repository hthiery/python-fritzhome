#!/usr/bin/env python

from nose.tools import eq_, raises
from mock import MagicMock

from requests import Response
from pyfritzhome import (Fritzhome, LoginError)

from .elements import (device_list_xml, login_rsp_without_valid_sid,
                       login_rsp_with_valid_sid)


class TestFritzhome(object):

    @raises(LoginError)
    def test_login_fail(self):
        mock = MagicMock()
        mock.side_effect = [
            login_rsp_without_valid_sid,
            login_rsp_without_valid_sid,
        ]

        fritz = Fritzhome('10.0.0.1', 'user', 'pass')
        fritz._request = mock
        fritz.login()

    def test_login(self):

        mock = MagicMock()
        mock.side_effect = [
            login_rsp_without_valid_sid,
            login_rsp_with_valid_sid,
        ]

        fritz = Fritzhome('10.0.0.1', 'user', 'pass')
        fritz._request = mock
        fritz.login()

    def test_get_device_element(self):
        mock = MagicMock()
        mock.side_effect = [
            device_list_xml,
            device_list_xml,
        ]

        fritz = Fritzhome('10.0.0.1', 'user', 'pass')
        fritz._request = mock
        elements = fritz.get_device_element('08761 0000434')
        eq_(elements.getAttribute('identifier'), '08761 0000434')
        eq_(elements.getAttribute('fwversion'), '03.33')

        elements = fritz.get_device_element('08761 1048079')
        eq_(elements.getAttribute('identifier'), '08761 1048079')
        eq_(elements.getAttribute('fwversion'), '03.44')

    def test_aha_get_devices(self):

        mock = MagicMock()
        mock.side_effect = [
            device_list_xml,
        ]

        fritz = Fritzhome('10.0.0.1', 'user', 'pass')
        fritz._request = mock
        devices = fritz.get_devices()
        eq_(devices[0].name, 'Steckdose')
        eq_(devices[1].name, 'FRITZ!DECT Rep 100 #1')

    def test_get_device_name(self):

        mock = MagicMock()
        mock.side_effect = [
            'testname'
        ]

        fritz = Fritzhome('10.0.0.1', 'user', 'pass')
        fritz._request = mock

        eq_(fritz.get_device_name(ain='1234'), 'testname')

        fritz._request.assert_called_with(
            'http://10.0.0.1/webservices/homeautoswitch.lua',
            {'sid': None, 'ain': '1234', 'switchcmd': 'getswitchname'})

    def test_set_target_temperature(self):
        mock = MagicMock()

        fritz = Fritzhome('10.0.0.1', 'user', 'pass')
        fritz._request = mock

        fritz.set_target_temperature('1', 25.5)
        fritz._request.assert_called_with(
            'http://10.0.0.1/webservices/homeautoswitch.lua',
            {'sid': None, 'ain': '1', 'switchcmd': 'sethkrsoll', 'param': 51})

        fritz.set_target_temperature('1', 0.0)
        fritz._request.assert_called_with(
            'http://10.0.0.1/webservices/homeautoswitch.lua',
            {'sid': None, 'ain': '1', 'switchcmd': 'sethkrsoll', 'param': 253})

        fritz.set_target_temperature('1', 32.0)
        fritz._request.assert_called_with(
            'http://10.0.0.1/webservices/homeautoswitch.lua',
            {'sid': None, 'ain': '1', 'switchcmd': 'sethkrsoll', 'param': 254})
