# -*- coding: utf-8 -*-
# flake8: noqa

login_rsp_without_valid_sid = '<?xml version="1.0" encoding="utf-8"?><SessionInfo><SID>0000000000000000</SID><Challenge>44b750c0</Challenge><BlockTime>0</BlockTime><Rights></Rights></SessionInfo>'

login_rsp_with_valid_sid = '<?xml version="1.0" encoding="utf-8"?><SessionInfo><SID>0000000000000001</SID><Challenge>44b750c0</Challenge><BlockTime>0</BlockTime><Rights></Rights></SessionInfo>'

device_list_xml = """<devicelist version="1">
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
    <device identifier="08761 1048079" id="16" functionbitmask="1280"
    fwversion="03.44" manufacturer="AVM" productname="FRITZ!DECT Repeater 100">
        <present>1</present>
        <name>FRITZ!DECT Rep 100 #1</name>
        <temperature>
            <celsius>288</celsius>
            <offset>0</offset>
        </temperature>
    </device>
    <device identifier="11959 0171328" id="16" functionbitmask="320"
    fwversion="03.54" manufacturer="AVM" productname="Comet DECT">
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
    <device functionbitmask="8208" fwversion="0.0" id="2000"
     identifier="05333 0077045-1" manufacturer="0x0512" productname="HAN-FUN">
        <present>1</present>
        <name>Fenster</name>
        <etsiunitinfo>
            <etsideviceid>406</etsideviceid>
            <unittype>514</unittype>
            <interfaces>256</interfaces>
        </etsiunitinfo>
        <alert>
            <state>1</state>
        </alert>
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

device_list_battery_ok_xml = """<devicelist version="1">
    <device identifier="11959 0171328" id="16" functionbitmask="320"
    fwversion="03.54" manufacturer="AVM" productname="Comet DECT">
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
</devicelist>"""

device_list_battery_low_xml = """<devicelist version="1">
    <device identifier="11959 0171328" id="16" functionbitmask="320"
    fwversion="03.54" manufacturer="AVM" productname="Comet DECT">
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
            <batterylow>1</batterylow>
            <nextchange>
                <endperiod>1508342400</endperiod>
                <tchange>42</tchange>
            </nextchange>
        </hkr>
    </device>
</devicelist>"""


device_not_present_xml = """<?xml version="1.0" ?>
<devicelist version="1">
    <device functionbitmask="320" fwversion="03.54" id="18" identifier="11960 0089208" manufacturer="AVM" productname="Comet DECT">
        <present>0</present>
        <name>Kitchen</name>
        <temperature>
            <celsius/>
            <offset/>
        </temperature>
        <hkr>
            <tist/>
            <tsoll/>
            <absenk/>
            <komfort/>
            <lock/>
            <devicelock/>
            <errorcode>0</errorcode>
            <batterylow>0</batterylow>
            <nextchange>
                <endperiod>0</endperiod>
                <tchange>255</tchange>
            </nextchange>
        </hkr>
    </device>
</devicelist>"""

device_no_devicelock_element_xml = """<?xml version="1.0" ?>
<devicelist version="1">
    <device functionbitmask="896" fwversion="03.59" id="16" identifier="08761 0373130" manufacturer="AVM" productname="FRITZ!DECT 200">
            <present>1</present>
            <name>FRITZ!DECT 200 #1</name>
            <switch>
                    <state>1</state>
                    <mode>manuell</mode>
                    <lock>1</lock>
            </switch>
            <powermeter>
                    <power>114580</power>
                    <energy>87830</energy>
            </powermeter>
            <temperature>
                    <celsius>220</celsius>
                    <offset>0</offset>
            </temperature>
    </device>

</devicelist>"""

device_hkr_fw_03_50_xml = """<?xml version="1.0" ?>
<devicelist version="1">
    <device functionbitmask="320" fwversion="03.50" id="17" identifier="12345" manufacturer="AVM" productname="Comet DECT">
        <present>1</present>
        <name>Comet DECT #2</name>
        <temperature>
            <celsius>230</celsius>
            <offset>-10</offset>
        </temperature>
        <hkr>
            <tist>46</tist>
            <tsoll>45</tsoll>
            <absenk>32</absenk>
            <komfort>45</komfort>
        </hkr>
    </device>
</devicelist>"""

device_hkr_fw_03_54_xml = """<?xml version="1.0" ?>
<devicelist version="1">
    <device functionbitmask="320" fwversion="03.54" id="18" identifier="23456" manufacturer="AVM" productname="Comet DECT">
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
</devicelist>"""

device_hkr_no_temp_values_xml = """<device functionbitmask="320" fwversion="03.54" id="22" identifier="11960 0071472" manufacturer="AVM" productname="Comet DECT">
    <present>1</present>
    <name>Thermostat Wohnzimmer Seite</name>
    <temperature>
        <celsius/>
        <offset/>
    </temperature>
    <hkr>
        <tist>44</tist>
        <tsoll>42</tsoll>
        <absenk>36</absenk>
        <komfort>42</komfort>
        <lock>0</lock>
        <devicelock>0</devicelock>
        <errorcode>5</errorcode>
        <batterylow>0</batterylow>
        <nextchange>
            <endperiod>1519160400</endperiod>
            <tchange>36</tchange>
        </nextchange>
    </hkr>
</device>"""

device_alert_on_xml = """<device functionbitmask="8208" fwversion="0.0" id="2000" identifier="05333 0077045-1" manufacturer="0x0512" productname="HAN-FUN">
    <present>1</present>
    <name>Fenster</name>
    <etsiunitinfo>
        <etsideviceid>406</etsideviceid>
        <unittype>514</unittype>
        <interfaces>256</interfaces>
    </etsiunitinfo>
    <alert>
        <state>1</state>
    </alert>
</device>"""

device_alert_off_xml = """<device functionbitmask="8208" fwversion="0.0" id="2000" identifier="05333 0077045-2" manufacturer="0x0512" productname="HAN-FUN">
    <present>1</present>
    <name>Fenster</name>
    <etsiunitinfo>
        <etsideviceid>406</etsideviceid>
        <unittype>514</unittype>
        <interfaces>256</interfaces>
    </etsiunitinfo>
    <alert>
        <state>0</state>
    </alert>
</device>"""

device_alert_no_alertstate_xml = """<device functionbitmask="8208" fwversion="0.0" id="2000" identifier="05333 0077045-3" manufacturer="0x0512" productname="HAN-FUN">
    <present>1</present>
    <name>Fenster</name>
    <etsiunitinfo>
        <etsideviceid>406</etsideviceid>
        <unittype>514</unittype>
        <interfaces>256</interfaces>
    </etsiunitinfo>
    <alert></alert>
</device>"""

device_with_umlaut_in_name_xml = """<?xml version="1.0" ?>
<devicelist version="1">
    <device functionbitmask="896" fwversion="03.59" id="16" identifier="08761 0373130" manufacturer="AVM" productname="FRITZ!DECT 200">
            <present>1</present>
            <name>äöü</name>
            <switch>
                    <state>1</state>
                    <mode>manuell</mode>
                    <lock>1</lock>
            </switch>
            <powermeter>
                    <power>114580</power>
                    <energy>87830</energy>
            </powermeter>
            <temperature>
                    <celsius>220</celsius>
                    <offset>0</offset>
            </temperature>
    </device>

</devicelist>"""

device_hkr_state_on_xml = """<?xml version="1.0" ?>
<devicelist version="1">
    <device functionbitmask="320" fwversion="03.50" id="17" identifier="12345" manufacturer="AVM" productname="Comet DECT">
        <present>1</present>
        <name>Comet DECT #2</name>
        <temperature>
            <celsius>230</celsius>
            <offset>-10</offset>
        </temperature>
        <hkr>
            <tist>46</tist>
            <tsoll>254</tsoll>
            <absenk>32</absenk>
            <komfort>45</komfort>
        </hkr>
    </device>
</devicelist>"""

device_hkr_state_off_xml = """<?xml version="1.0" ?>
<devicelist version="1">
    <device functionbitmask="320" fwversion="03.50" id="17" identifier="12345" manufacturer="AVM" productname="Comet DECT">
        <present>1</present>
        <name>Comet DECT #2</name>
        <temperature>
            <celsius>230</celsius>
            <offset>-10</offset>
        </temperature>
        <hkr>
            <tist>46</tist>
            <tsoll>253</tsoll>
            <absenk>32</absenk>
            <komfort>45</komfort>
        </hkr>
    </device>
</devicelist>"""

device_hkr_state_eco_xml = """<?xml version="1.0" ?>
<devicelist version="1">
    <device functionbitmask="320" fwversion="03.50" id="17" identifier="12345" manufacturer="AVM" productname="Comet DECT">
        <present>1</present>
        <name>Comet DECT #2</name>
        <temperature>
            <celsius>230</celsius>
            <offset>-10</offset>
        </temperature>
        <hkr>
            <tist>46</tist>
            <tsoll>45</tsoll>
            <absenk>45</absenk>
            <komfort>48</komfort>
        </hkr>
    </device>
</devicelist>"""

device_hkr_state_comfort_xml = """<?xml version="1.0" ?>
<devicelist version="1">
    <device functionbitmask="320" fwversion="03.50" id="17" identifier="12345" manufacturer="AVM" productname="Comet DECT">
        <present>1</present>
        <name>Comet DECT #2</name>
        <temperature>
            <celsius>230</celsius>
            <offset>-10</offset>
        </temperature>
        <hkr>
            <tist>46</tist>
            <tsoll>48</tsoll>
            <absenk>45</absenk>
            <komfort>48</komfort>
        </hkr>
    </device>
</devicelist>"""

device_hkr_state_manual_xml = """<?xml version="1.0" ?>
<devicelist version="1">
    <device functionbitmask="320" fwversion="03.50" id="17" identifier="12345" manufacturer="AVM" productname="Comet DECT">
        <present>1</present>
        <name>Comet DECT #2</name>
        <temperature>
            <celsius>230</celsius>
            <offset>-10</offset>
        </temperature>
        <hkr>
            <tist>46</tist>
            <tsoll>40</tsoll>
            <absenk>45</absenk>
            <komfort>48</komfort>
        </hkr>
    </device>
</devicelist>"""


device_hkr_fritzos_7_xml = """<?xml version="1.0" ?>
<devicelist version="1">
    <device functionbitmask="320" fwversion="03.54" id="22" identifier="12345" manufacturer="AVM" productname="Comet DECT">
        <present>1</present>
        <name>Thermostat Wohnzimmer Seite</name>
        <temperature>
            <celsius>205</celsius>
            <offset>-10</offset>
        </temperature>
        <hkr>
            <tist>41</tist>
            <tsoll>253</tsoll>
            <absenk>36</absenk>
            <komfort>42</komfort>
            <lock>1</lock>
            <devicelock>1</devicelock>
            <errorcode>0</errorcode>
            <batterylow>0</batterylow>
            <windowopenactiv>0</windowopenactiv>
            <battery>70</battery>
            <nextchange>
                <endperiod>1538341200</endperiod>
                <tchange>42</tchange>
            </nextchange>
            <summeractive>1</summeractive>
            <holidayactive>0</holidayactive>
        </hkr>
    </device>
</devicelist>"""

device_magenta_smoke_alarm_xml = """<?xml version="1.0" ?>
<devicelist version="1">
    <device functionbitmask="8208" fwversion="0.0" id="2000" identifier="11324 0244498-1" manufacturer="0x2c3c" productname="HAN-FUN">
        <present>1</present>
        <name>Rauchmelder</name>
        <etsiunitinfo>
            <etsideviceid>406</etsideviceid>
            <unittype>516</unittype>
            <interfaces>256</interfaces>
        </etsiunitinfo>
        <alert>
            <state/>
        </alert>
    </device>
</devicelist>"""
