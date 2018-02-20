from __future__ import print_function
import hashlib
import logging
import xml.dom.minidom
from requests import Session

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
    """Get the value from a node."""
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

    @staticmethod
    def _create_login_secret(challenge, password):
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
        try:
            (sid, challenge) = self._login_request()
            if sid == '0000000000000000':
                secret = self._create_login_secret(challenge, self._password)
                (sid2, challenge) = self._login_request(username=self._user,
                                                        secret=secret)
                if sid2 == '0000000000000000':
                    _LOGGER.warning("login failed %s", sid2)
                    raise LoginError(self._user)
                self._sid = sid2
        except xml.parsers.expat.ExpatError:
            raise LoginError(self._user)

    def logout(self):
        """Logout."""
        self._logout_request()
        self._sid = None

    def get_device_elements(self):
        """Get the DOM elments for the device list."""
        plain = self._aha_request('getdevicelistinfos')
        dom = xml.dom.minidom.parseString(plain)
        _LOGGER.info(dom)
        return dom.getElementsByTagName("device")

    def get_device_element(self, ain):
        """Get the DOM elment for the specified device."""
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
        """Get the device presence."""
        plain = self._aha_request('getswitchpresent', ain=ain)
        return bool(int(plain))

    def get_device_name(self, ain):
        """Get the device name."""
        plain = self._aha_request('getswitchname', ain=ain)
        return plain

    def get_switch_state(self, ain):
        """Get the switch state."""
        plain = self._aha_request('getswitchstate', ain=ain)
        return bool(int(plain))

    def set_switch_state_on(self, ain):
        """Set the switch to on state."""
        plain = self._aha_request('setswitchon', ain=ain)
        return bool(int(plain))

    def set_switch_state_off(self, ain):
        """Set the switch to off state."""
        plain = self._aha_request('setswitchoff', ain=ain)
        return bool(int(plain))

    def set_switch_state_toggle(self, ain):
        """Toglle the switch state."""
        plain = self._aha_request('setswitchtoggle', ain=ain)
        return bool(int(plain))

    def get_switch_power(self, ain):
        """Get the switch power consumption."""
        plain = self._aha_request('getswitchpower', ain=ain)
        return int(plain)

    def get_switch_energy(self, ain):
        """Get the switch energy."""
        plain = self._aha_request('getswitchenergy', ain=ain)
        return int(plain)

    def get_temperature(self, ain):
        """Get the device temperature sensor value."""
        plain = self._aha_request('gettemperature', ain=ain)
        return float(int(plain) / 10.0)

    def get_target_temperature(self, ain):
        """Get the thermostate target temperature."""
        plain = self._aha_request('gethkrtsoll', ain=ain)
        return (float(plain) - 16) / 2 + 8

    def set_target_temperature(self, ain, temperature):
        """Set the thermostate target temperature."""
        param = 16 + ((temperature - 8) * 2)

        if param < min(range(16, 56)):
            param = 253
        elif param > max(range(16, 56)):
            param = 254
        self._aha_request('sethkrtsoll', ain=ain, param=int(param))

    def get_comfort_temperature(self, ain):
        """Get the thermostate comfort temperature."""
        plain = self._aha_request('gethkrkomfort', ain=ain)
        return (float(plain) - 16) / 2 + 8

    def get_eco_temperature(self, ain):
        """Get the thermostate eco temperature."""
        plain = self._aha_request('gethkrabsenk', ain=ain)
        return (float(plain) - 16) / 2 + 8


class FritzhomeDevice(object):
    """The Fritzhome Device class."""
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

    def __init__(self, fritz=None, node=None):
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
            val = node.getElementsByTagName('hkr')[0]
            self.actual_temperature = int(get_node_value(val, 'tist')) / 2
            self.target_temperature = int(get_node_value(val, 'tsoll')) / 2
            self.eco_temperature = int(get_node_value(val, 'absenk')) / 2
            self.comfort_temperature = int(get_node_value(val, 'komfort')) / 2

            # optional value
            try:
                self.device_lock = bool(int(get_node_value(val, 'devicelock')))
            except IndexError:
                pass

            try:
                self.lock = bool(int(get_node_value(val, 'lock')))
            except IndexError:
                pass

            try:
                self.error_code = int(get_node_value(val, 'errorcode'))
            except IndexError:
                pass

            try:
                self.battery_low = bool(int(get_node_value(val, 'batterylow')))
            except IndexError:
                pass

        if self.has_switch:
            val = node.getElementsByTagName('switch')[0]
            self.switch_state = bool(int(get_node_value(val, 'state')))
            self.switch_mode = get_node_value(val, 'mode')
            self.lock = bool(get_node_value(val, 'lock'))
            # optional value
            try:
                self.device_lock = bool(int(get_node_value(val, 'devicelock')))
            except IndexError:
                pass

        if self.has_powermeter:
            val = node.getElementsByTagName('powermeter')[0]
            self.power = int(get_node_value(val, 'power'))
            self.energy = int(get_node_value(val, 'energy'))

        if self.has_temperature_sensor:
            val = node.getElementsByTagName('temperature')[0]
            try:
                self.offset = int(get_node_value(val, 'offset')) / 10
            except ValueError:
                pass

            try:
                self.temperature = int(get_node_value(val, 'celsius')) / 10
            except ValueError:
                pass

    def __repr__(self):
        """Return a string."""
        return '{} {} {} {}'.format(self.ain, self._id,
                                    self.manufacturer, self.productname)

    def update(self):
        """Update the device values."""
        node = self._fritz.get_device_element(self.ain)
        self._update_from_node(node)

    @property
    def has_alarm(self):
        """Check if the device has alarm function."""
        return bool(self._functionsbitmask & self.ALARM_MASK)

    @property
    def has_thermostat(self):
        """Check if the device has thermostat function."""
        return bool(self._functionsbitmask & self.THERMOSTAT_MASK)

    @property
    def has_powermeter(self):
        """Check if the device has powermeter function."""
        return bool(self._functionsbitmask & self.POWER_METER_MASK)

    @property
    def has_temperature_sensor(self):
        """Check if the device has temperature function."""
        return bool(self._functionsbitmask & self.TEMPERATURE_MASK)

    @property
    def has_switch(self):
        """Check if the device has switch function."""
        return bool(self._functionsbitmask & self.SWITCH_MASK)

    @property
    def has_repeater(self):
        """Check if the device has repeater function."""
        return bool(self._functionsbitmask & self.DECT_REPEATER_MASK)

    def get_present(self):
        """Check if the device is present."""
        return self._fritz.get_device_present(self.ain)

    def get_switch_state(self):
        """Get the switch state."""
        return self._fritz.get_switch_state(self.ain)

    def set_switch_state_on(self):
        """Set the switch state to on."""
        return self._fritz.set_switch_state_on(self.ain)

    def set_switch_state_off(self):
        """Set the switch state to off."""
        return self._fritz.set_switch_state_off(self.ain)

    def set_switch_state_toggle(self):
        """Toggle the switch state."""
        return self._fritz.set_switch_state_toggle(self.ain)

    def get_switch_power(self):
        """ the switch state."""
        return self._fritz.get_switch_power(self.ain)

    def get_switch_energy(self):
        """Get the switch energy."""
        return self._fritz.get_switch_energy(self.ain)

    def get_temperature(self):
        """Get the device temperature value."""
        return self._fritz.get_temperature(self.ain)

    def get_target_temperature(self):
        """Get the thermostate target temperature."""
        return self._fritz.get_target_temperature(self.ain)

    def set_target_temperature(self, temperature):
        """Set the thermostate target temperature."""
        return self._fritz.set_target_temperature(self.ain, temperature)

    def get_comfort_temperature(self):
        """Get the thermostate comfort temperature."""
        return self._fritz.get_comfort_temperature(self.ain)

    def get_eco_temperature(self):
        """Get the thermostate eco temperature."""
        return self._fritz.get_eco_temperature(self.ain)
