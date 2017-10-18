#!/usr/bin/env python

from nose.tools import raises
from mock import MagicMock

from requests import Response
from pyfritzhome import (Fritzhome, LoginError)

class TestFritzhome(object):

    @raises(LoginError)
    def test_login_fail(self):
        mock = MagicMock()
        mock.side_effect = [
            '<?xml version="1.0" encoding="utf-8"?><SessionInfo><SID>0000000000000000</SID><Challenge>44b750c0</Challenge><BlockTime>0</BlockTime><Rights></Rights></SessionInfo>',
            '<?xml version="1.0" encoding="utf-8"?><SessionInfo><SID>0000000000000000</SID><Challenge>44b750c0</Challenge><BlockTime>0</BlockTime><Rights></Rights></SessionInfo>',
        ]

        fritz = Fritzhome('10.0.0.1', 'user', 'pass')
        fritz._request = mock
        fritz.login()

    def test_login(self):

        mock = MagicMock()
        mock.side_effect = [
            '<?xml version="1.0" encoding="utf-8"?><SessionInfo><SID>0000000000000000</SID><Challenge>44b750c0</Challenge><BlockTime>0</BlockTime><Rights></Rights></SessionInfo>',
            '<?xml version="1.0" encoding="utf-8"?><SessionInfo><SID>0000000000000001</SID><Challenge>44b750c0</Challenge><BlockTime>0</BlockTime><Rights></Rights></SessionInfo>',
        ]

        fritz = Fritzhome('10.0.0.1', 'user', 'pass')
        fritz._request = mock
        fritz.login()

    def test_aha_command(self):
        pass
