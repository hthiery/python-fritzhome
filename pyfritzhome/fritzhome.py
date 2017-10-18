"""
References:
 - https://avm.de/fileadmin/user_upload/Global/Service/Schnittstellen/AHA-HTTP-Interface.pdf
 - https://github.com/DerMitch/fritzbox-smarthome
"""

from requests import Session
import hashlib
import logging
import xml.dom.minidom

_LOGGER = logging.getLogger(__name__)

from .errors import (InvalidError, LoginError)

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def getNodeValue(node, name):
    return getText(node.getElementsByTagName(name)[0].childNodes)


class Fritzhome(object):
    """Fritzhome object to communicate with the device."""

    _sid = None
    _session = None

    def __init__(self, host, user, password):
        self._host = host
        self._user = user
        self._password = password
        self._session = Session()

    def _request(self, url, params=None, timeout=10):
        rsp = self._session.get(url, params=params, timeout=timeout)
        rsp.raise_for_status()
        return rsp.text.strip()

    def _login_request(self, username=None, secret=None, timeout=10):
        url = 'http://' + self._host + '/login_sid.lua'
        params = {}
        if username:
            params['username'] = username
        if secret:
            params['response'] = secret

        plain = self._request(url, params, timeout)
        dom = xml.dom.minidom.parseString(plain)
        sid = getText(dom.getElementsByTagName('SID')[0].childNodes)
        challenge = getText(dom.getElementsByTagName('Challenge')[0].childNodes)

        return (sid, challenge)

    def _create_login_secret(self, challenge, password):
        to_hash = (challenge + '-' + password).encode('UTF-16LE')
        hashed = hashlib.md5(to_hash).hexdigest()
        return '{0}-{1}'.format(challenge, hashed)

#    def _haq_request(self, cmd, ain=None, param=None):
#        url = 'http://' + self._host + '/net/home_auto_query.lua'

    def _aha_request(self, cmd, ain=None, param=None):
        url = 'http://' + self._host + '/webservices/homeautoswitch.lua'
        params = {
            'switchcmd': cmd,
            'sid': self._sid
        }
        if param:
            params['params'] = param
        if ain:
            params['ain'] = ain

        plain = self._request(url, params)
        _LOGGER.info("plain=%s", plain)
        if plain == 'inval':
            raise InvalidError
        return plain

    def login(self, retry=3):
        (sid, challenge) = self._login_request()
        _LOGGER.debug("sid=%s challenge", (sid, challenge))
        if sid == '0000000000000000':
            secret = self._create_login_secret(challenge, self._password)
            (sid2, challenge) = self._login_request(
                    username=self._user, secret=secret)
            if sid2 == '0000000000000000':
                _LOGGER.warning("login failed %s", sid2)
                raise LoginError(self._user)
        self._sid = sid2
        _LOGGER.info("login")

    def logout(self):
        pass

    def get_devices(self):
        """Get the list of all known devices."""
        plain = self._aha_request('getdevicelistinfos')
        dom = xml.dom.minidom.parseString(plain)

        devices = []
        for element in dom.getElementsByTagName("device"):
            device = Device(self, node=element)
            devices.append(device)

        return devices

    def get_switchlist(self, ain):
        plain = self._aha_request('getswitchlist')
        print(plain)


    def get_device_present(self, ain):
        plain = self._aha_request('getswitchpresent', ain=ain)
        return bool(int(plain))

    def get_device_name(self, ain):
        plain = self._aha_request('getswitchname', ain=ain)
        return plain


    def get_switch_state(self, ain):
        plain = self._aha_request('getswitchstate', ain=ain)
        return bool(int(plain))

    def set_switch_state_on(self, ain):
        plain = self._aha_request('setswitchon', ain=ain)
        return bool(int(plain))

    def set_switch_state_off(self, ain):
        plain = self._aha_request('setswitchoff', ain=ain)
        return bool(int(plain))

    def set_switch_state_toggle(self, ain):
        plain = self._aha_request('setswitchtoggle', ain=ain)
        return bool(int(plain))

    def get_switch_power(self, ain):
        plain = self._aha_request('getswitchpower', ain=ain)
        return plain

    def get_switch_energy(self, ain):
        plain = self._aha_request('getswitchenergy', ain=ain)
        return plain


    def get_temperature(self, ain):
        plain = self._aha_request('gettemperature', ain=ain)
        return float(int(plain) / 10.0)

    def get_soll_temperature(self, ain):
        plain = self._aha_request('gethkrtsoll', ain=ain)
        return ((float(plain) - 16) / 2 + 8)

    def get_komfort_temperature(self, ain):
        plain = self._aha_request('gethkrkomfort', ain=ain)
        return ((float(plain) - 16) / 2 + 8)

    def get_absenk_temperature(self, ain):
        plain = self._aha_request('gethkrabsenk', ain=ain)
        return ((float(plain) - 16) / 2 + 8)


class Device(object):

    ALARM_MASK = 0x010
    UNKNOWN_MASK = 0x020
    THERMOSTAT_MASK = 0x040
    POWER_METER_MASK = 0x080
    TEMPERATURE_MASK = 0x100
    SWITCH_MASK = 0x200
    DECT_REPEATER_MASK = 0x400
    UNKNOWN2_MASK = 0x800

    def __init__(self, fritz=None, node=None, *args, **kwargs):
        if node is not None:
            _LOGGER.debug(node.toprettyxml())
            self._set_from_dom_node(node)

        if fritz is not None:
            self._fritz = fritz

    def _set_from_dom_node(self, node):
        # data from attributes
        self.ain = node.getAttribute("identifier")
        self.id = node.getAttribute("id")
        self._functionsbitmask = int(node.getAttribute("functionbitmask"))
        self.fw_version= node.getAttribute("fwversion")
        self.manufacturer = node.getAttribute("manufacturer")
        self.productname = node.getAttribute("productname")

        self.name = getNodeValue(node, 'name')
        self._present = getNodeValue(node, 'present')

    def __repr__(self):
        return '{} {} {} {}'.format(self.ain, self._id,
                self._manufacturer, self._productname)

    @property
    def has_alarm(self):
        return bool(self._functionsbitmask & self.ALARM_MASK)

    @property
    def has_thermostat(self):
        return bool(self._functionsbitmask & self.THERMOSTAT_MASK)

    @property
    def has_powermeter(self):
        return bool(self._functionsbitmask & self.POWER_METER_MASK)

    @property
    def has_temperature_sensor(self):
        return bool(self._functionsbitmask & self.TEMPERATURE_MASK)

    @property
    def has_switch(self):
        return bool(self._functionsbitmask & self.SWITCH_MASK)

    @property
    def has_repeater(self):
        return bool(self._functionsbitmask & self.DECT_REPEATER_MASK)

    def get_present(self):
        return self._fritz.get_device_present(ain=self.ain)


    def get_switch_state(self):
        return self._fritz.get_switch_state(ain=self.ain)

    def set_switch_state_on(self):
        return self._fritz.set_switch_state_on(ain=self.ain)

    def set_switch_state_off(self):
        return self._fritz.set_switch_state_off(ain=self.ain)

    def set_switch_state_toggle(self):
        return self._fritz.set_switch_state_toggle(ain=self.ain)

    def get_switch_power(self):
        return self._fritz.get_switch_power(ain=self.ain)

    def get_switch_energy(self):
        return self._fritz.get_switch_energy(ain=self.ain)


    def get_temperature(self):
        return self._fritz.get_temperature(ain=self.ain)

    def get_soll_temperature(self):
        return self._fritz.get_soll_temperature(ain=self.ain)

    def get_komfort_temperature(self):
        return self._fritz.get_komfort_temperature(ain=self.ain)

    def get_absenk_temperature(self):
        return self._fritz.get_absenk_temperature(ain=self.ain)


class Alarm(Device):
    def __init__(self, node=None):
        raise NotImplemented

class Thermostat(Device):
    def __init__(self, node=None):
        raise NotImplemented

class Switch(Device):
    def __init__(self, node=None):
        raise NotImplemented

class Repeater(Device):
    def __init__(self, node=None):
        raise NotImplemented
