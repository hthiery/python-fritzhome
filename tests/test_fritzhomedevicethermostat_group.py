#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest.mock import MagicMock

from pyfritzhome import Fritzhome
from pyfritzhome.devicetypes.fritzhomedevicefeatures import FritzhomeDeviceFeatures

from .helper import Helper


class TestFritzhomeDeviceThermostat(object):
    def setup_method(self):
        self.mock = MagicMock()
        self.fritz = Fritzhome("10.0.0.1", "user", "pass")
        self.fritz._request = self.mock
        self.fritz._devices = {}
        self.fritz._sid = "0000001"

    def test_device_alert_on(self):
        self.mock.side_effect = [
            Helper.response("groups/device_list_thermostat"),
            Helper.response("groups/device_list_thermostat_without_tsoll"),
            Helper.response("groups/device_list_thermostat"),
        ]

        self.fritz.update_devices()
        group = self.fritz.get_device_by_ain("grp303E4F-3F7D9BE07")
        assert group.has_thermostat
        assert group.is_group
        assert group.group_members == ["16", "17"]
        assert group.supported_features == [FritzhomeDeviceFeatures.THERMOSTAT]
        assert group.adaptive_heating_active is True
        assert group.adaptive_heating_running is False
        assert group.boost_active is False
        assert group.window_open is False
        assert group.boost_active_endtime == 0
        assert group.window_open_endtime == 0
        assert group.actual_temperature is None
        assert group.target_temperature == 21.5

        self.fritz.update_devices()
        group = self.fritz.get_device_by_ain("grp303E4F-3F7D9BE07")
        assert group.has_thermostat
        assert group.is_group
        assert group.group_members == ["16", "17"]
        assert group.supported_features == [FritzhomeDeviceFeatures.THERMOSTAT]
        assert group.adaptive_heating_active is True
        assert group.adaptive_heating_running is False
        assert group.boost_active is False
        assert group.window_open is False
        assert group.boost_active_endtime == 0
        assert group.window_open_endtime == 0
        assert group.actual_temperature is None
        assert group.target_temperature is None

        self.fritz.update_devices()
        group = self.fritz.get_device_by_ain("grp303E4F-3F7D9BE07")
        assert group.has_thermostat
        assert group.is_group
        assert group.group_members == ["16", "17"]
        assert group.supported_features == [FritzhomeDeviceFeatures.THERMOSTAT]
        assert group.adaptive_heating_active is True
        assert group.adaptive_heating_running is False
        assert group.boost_active is False
        assert group.window_open is False
        assert group.boost_active_endtime == 0
        assert group.window_open_endtime == 0
        assert group.actual_temperature is None
        assert group.target_temperature == 21.5
