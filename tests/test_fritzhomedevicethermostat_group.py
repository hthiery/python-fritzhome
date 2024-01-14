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

    def test_device_alert_on(self):
        self.mock.side_effect = [
            Helper.response("groups/device_list_thermostat"),
        ]

        self.fritz.update_devices()
        group = self.fritz.get_device_by_ain("grp303E4F-3F7D9BE07")
        assert group.has_thermostat
        assert group.is_group
        assert group.group_members == ["16", "17"]
        assert group.supported_features == [FritzhomeDeviceFeatures.THERMOSTAT]
