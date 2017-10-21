#!/usr/bin/env python

from nose.tools import eq_, raises
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

    def test_aha_get_devices(self):

        mock = MagicMock()
        mock.side_effect = [
            '<?xml version="1.0" encoding="utf-8"?><SessionInfo><SID>0000000000000000</SID><Challenge>44b750c0</Challenge><BlockTime>0</BlockTime><Rights></Rights></SessionInfo>',
            '<?xml version="1.0" encoding="utf-8"?><SessionInfo><SID>0000000000000001</SID><Challenge>44b750c0</Challenge><BlockTime>0</BlockTime><Rights></Rights></SessionInfo>',
"""<devicelist version="1">
    <device identifier="08761 0000434" id="17" functionbitmask="896" fwversion="03.33" manufacturer="AVM" productname="FRITZ!DECT 200">
        <present>1</present>
        <name>Steckdose</name>
        <switch>
            <state>1</state>
            <mode>auto</mode>
            <lock>0</lock>
            <devicelock>0</devicelock>
        </switch>
        <powermeter>
            <power>0</power>
            <energy>707</energy>
        </powermeter>
        <temperature>
            <celsius>285</celsius>
            <offset>0</offset>
        </temperature>
    </device>
    <device identifier="08761 1048079" id="16" functionbitmask="1280" fwversion="03.33" manufacturer="AVM" productname="FRITZ!DECT Repeater 100">
        <present>1</present>
        <name>FRITZ!DECT Rep 100 #1</name>
        <temperature>
            <celsius>288</celsius>
            <offset>0</offset>
        </temperature>
    </device>
    <group identifier="65:3A:18-900" id="900" functionbitmask="512" fwversion="1.0" manufacturer="AVM" productname="">
        <present>1</present>
        <name>Gruppe</name>
        <switch>
            <state>1</state>
            <mode>auto</mode>
            <lock/>
            <devicelock/>
        </switch>
        <groupinfo>
            <masterdeviceid>0</masterdeviceid>
            <members>17</members>
        </groupinfo>
    </group>
</devicelist>"""
        ]

        fritz = Fritzhome('10.0.0.1', 'user', 'pass')
        fritz._request = mock
        fritz.login()
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
#        fritz._request.assert_called_once_with(
#            'http://10.0.0.1/webservices/homeautoswitch.lua',
#            params = {
#                'switchcmd': 'getswitchname',
#                'sid': None,
#            }
#        )

