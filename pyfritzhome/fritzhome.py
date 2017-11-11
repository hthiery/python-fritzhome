from __future__ import print_function
from requests import Session
import hashlib
import logging
import xml.dom.minidom

from .errors import (InvalidError, LoginError)

_LOGGER = logging.getLogger(__name__)


def get_text(nodelist):
    """Get the value from a text node."""
    value = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            value.append(node.data)
    return ''.join(value)


def get_node_value(node, name):
    return get_text(node.getElementsByTagName(name)[0].childNodes)


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
        """Send a request with paramerters."""
        rsp = self._session.get(url, params=params, timeout=timeout)
        rsp.raise_for_status()
        return rsp.text.strip()

    def _login_request(self, username=None, secret=None):
        """Send a login request with paramerters."""
        url = 'http://' + self._host + '/login_sid.lua'
        params = {}
        if username:
            params['username'] = username
        if secret:
            params['response'] = secret

        plain = self._request(url, params)
        dom = xml.dom.minidom.parseString(plain)
        sid = get_text(dom.getElementsByTagName('SID')[0].childNodes)
        challenge = get_text(
            dom.getElementsByTagName('Challenge')[0].childNodes)

        return (sid, challenge)

    def _logout_request(self):
        """Send a logout request."""
        _LOGGER.info('logout')
        url = 'http://' + self._host + '/login_sid.lua'
        params = {
            'security:command/logout': '1',
            'sid': self._sid
        }

        self._request(url, params)

    def _create_login_secret(self, challenge, password):
        """Create a login secret."""
        to_hash = (challenge + '-' + password).encode('UTF-16LE')
        hashed = hashlib.md5(to_hash).hexdigest()
        return '{0}-{1}'.format(challenge, hashed)

    def _aha_request(self, cmd, ain=None, param=None):
        """Send an AHA request."""
        url = 'http://' + self._host + '/webservices/homeautoswitch.lua'
        params = {
            'switchcmd': cmd,
            'sid': self._sid
        }
        if param:
            params['param'] = param
        if ain:
            params['ain'] = ain

        plain = self._request(url, params)
        if plain == 'inval':
            raise InvalidError
        return plain

    def login(self):
        """Login and get a valid session ID."""
        (sid, challenge) = self._login_request()
        if sid == '0000000000000000':
            secret = self._create_login_secret(challenge, self._password)
            (sid2, challenge) = self._login_request(username=self._user,
                                                    secret=secret)
            if sid2 == '0000000000000000':
                _LOGGER.warning("login failed %s", sid2)
                raise LoginError(self._user)
        self._sid = sid2

    def logout(self):
        """Logout."""
        self._logout_request()
        self._sid = None

    def get_device_elements(self):
        plain = self._aha_request('getdevicelistinfos')
        dom = xml.dom.minidom.parseString(plain)
        return dom.getElementsByTagName("device")

    def get_device_element(self, ain):
        elements = self.get_device_elements()
        for element in elements:
            if element.getAttribute('identifier') == ain:
                return element
        return None

    def get_devices(self):
        """Get the list of all known devices."""
        devices = []
        for element in self.get_device_elements():
            device = FritzhomeDevice(self, node=element)
            devices.append(device)
        return devices

    def get_device_by_ain(self, ain):
        """Returns a device specified by the AIN."""
        devices = self.get_devices()
        for device in devices:
            if device.ain == ain:
                return device

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
        return int(plain)

    def get_switch_energy(self, ain):
        plain = self._aha_request('getswitchenergy', ain=ain)
        return int(plain)

    def get_temperature(self, ain):
        plain = self._aha_request('gettemperature', ain=ain)
        return float(int(plain) / 10.0)

    def get_target_temperature(self, ain):
        plain = self._aha_request('gethkrtsoll', ain=ain)
        return ((float(plain) - 16) / 2 + 8)

    def set_target_temperature(self, ain, temperature):
        param = 16 + ((temperature - 8) * 2)

        r = range(16, 56)
        if param < r[0]:
            param = 253
        elif param > r[-1]:
            param = 254
        self._aha_request('sethkrtsoll', ain=ain, param=int(param))

    def get_comfort_temperature(self, ain):
        plain = self._aha_request('gethkrkomfort', ain=ain)
        return ((float(plain) - 16) / 2 + 8)

    def get_eco_temperature(self, ain):
        plain = self._aha_request('gethkrabsenk', ain=ain)
        return ((float(plain) - 16) / 2 + 8)


class FritzhomeDevice(object):

    ALARM_MASK = 0x010
    UNKNOWN_MASK = 0x020
    THERMOSTAT_MASK = 0x040
    POWER_METER_MASK = 0x080
    TEMPERATURE_MASK = 0x100
    SWITCH_MASK = 0x200
    DECT_REPEATER_MASK = 0x400
    UNKNOWN2_MASK = 0x800

    ain = None
    _id = None
    manufacturer = None
    productname = None
    actual_temperature = None
    target_temperature = None
    eco_temperature = None
    comfort_temperature = None
    lock = None
    device_lock = None
    error_code = None
    battery_low = None
    switch_state = None
    switch_mode = None
    power = None
    energy = None
    offset = None
    temperature = None

    def __init__(self, fritz=None, node=None, *args, **kwargs):
        if fritz is not None:
            self._fritz = fritz
        if node is not None:
            self._update_from_node(node)

    def _update_from_node(self, node):
        _LOGGER.debug(node.toprettyxml())
        self.ain = node.getAttribute("identifier")
        self.id = node.getAttribute("id")
        self._functionsbitmask = int(node.getAttribute("functionbitmask"))
        self.fw_version = node.getAttribute("fwversion")
        self.manufacturer = node.getAttribute("manufacturer")
        self.productname = node.getAttribute("productname")

        self.name = get_node_value(node, 'name')
        self.present = bool(int(get_node_value(node, 'present')))

        if self.present is False:
            return

        if self.has_thermostat:
            n = node.getElementsByTagName('hkr')[0]
            self.actual_temperature = int(get_node_value(n, 'tist')) / 2
            self.target_temperature = int(get_node_value(n, 'tsoll')) / 2
            self.eco_temperature = int(get_node_value(n, 'absenk')) / 2
            self.comfort_temperature = int(get_node_value(n, 'komfort')) / 2
            self.lock = bool(int(get_node_value(n, 'lock')))
            self.error_code = int(get_node_value(n, 'errorcode'))
            self.battery_low = bool(int(get_node_value(n, 'batterylow')))
            # optional value
            try:
                self.device_lock = bool(int(get_node_value(n, 'devicelock')))
            except IndexError:
                pass

        if self.has_switch:
            n = node.getElementsByTagName('switch')[0]
            self.switch_state = bool(int(get_node_value(n, 'state')))
            self.switch_mode = get_node_value(n, 'mode')
            self.lock = bool(get_node_value(n, 'lock'))
            # optional value
            try:
                self.device_lock = bool(int(get_node_value(n, 'devicelock')))
            except IndexError:
                pass

        if self.has_powermeter:
            n = node.getElementsByTagName('powermeter')[0]
            self.power = int(get_node_value(n, 'power'))
            self.energy = int(get_node_value(n, 'energy'))

        if self.has_temperature_sensor:
            n = node.getElementsByTagName('temperature')[0]
            self.offset = int(get_node_value(n, 'offset')) / 10
            self.temperature = int(get_node_value(n, 'celsius')) / 10

    def __repr__(self):
        return '{} {} {} {}'.format(self.ain, self._id,
                                    self.manufacturer, self.productname)

    def update(self):
        node = self._fritz.get_device_element(self.ain)
        self._update_from_node(node)

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
        return self._fritz.get_device_present(self.ain)

    def get_switch_state(self):
        return self._fritz.get_switch_state(self.ain)

    def set_switch_state_on(self):
        return self._fritz.set_switch_state_on(self.ain)

    def set_switch_state_off(self):
        return self._fritz.set_switch_state_off(self.ain)

    def set_switch_state_toggle(self):
        return self._fritz.set_switch_state_toggle(self.ain)

    def get_switch_power(self):
        return self._fritz.get_switch_power(self.ain)

    def get_switch_energy(self):
        return self._fritz.get_switch_energy(self.ain)

    def get_temperature(self):
        return self._fritz.get_temperature(self.ain)

    def get_target_temperature(self):
        return self._fritz.get_target_temperature(self.ain)

    def set_target_temperature(self, temperature):
        return self._fritz.set_target_temperature(self.ain, temperature)

    def get_comfort_temperature(self):
        return self._fritz.get_comfort_temperature(self.ain)

    def get_eco_temperature(self):
        return self._fritz.get_eco_temperature(self.ain)
