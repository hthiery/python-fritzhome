#!/usr/bin/env python

from nose.tools import raises
from mock import MagicMock

from requests import Response
from pyfritzhome import (Fritzhome, LoginError)

class TestDevice(object):
    data = '''
<devicelist version="1">
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
</devicelist>
    '''
    data2 = """
<devicelist version="1">
    <device identifier="11959 0171328" id="16" functionbitmask="320" fwversion="03.54" manufacturer="AVM" productname="Comet DECT">
        <present>1</present>
        <name>Badezimmer</name>
        <temperature>
            <celsius>205</celsius>
            <offset>-15</offset>
        </temperature>
        <hkr>
            <tist>41</tist>
            <tsoll>36</tsoll>
            <absenk>36</absenk>
            <komfort>42</komfort>
            <lock>0</lock>
            <devicelock>0</devicelock>
            <errorcode>0</errorcode>
            <batterylow>0</batterylow>
            <nextchange>
                <endperiod>1508342400</endperiod>
                <tchange>42</tchange>
            </nextchange>
        </hkr>
    </device>
</devicelist>
"""

    def test_init(self):
        pass
