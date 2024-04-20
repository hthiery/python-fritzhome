#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest.mock import MagicMock

from pyfritzhome import Fritzhome
from pyfritzhome.devicetypes.fritzhomedevicefeatures import FritzhomeDeviceFeatures

from .helper import Helper


class TestFritzhomeTemplate(object):
    def setup_method(self):
        self.mock = MagicMock()
        self.fritz = Fritzhome("10.0.0.1", "user", "pass")
        self.fritz._request = self.mock
        self.fritz._devices = {}
        self.fritz._sid = "0000001"

        self.mock.side_effect = [Helper.response("templates/template_list")]

        self.fritz.update_templates()

    def test_template_init(self):
        template = self.fritz.get_template_by_ain("tmp0B32F7-1B0650682")

        assert template.ain == "tmp0B32F7-1B0650682"
        assert template._functionsbitmask == 320
        assert not template.apply_hkr_summer
        assert not template.apply_hkr_temperature
        assert not template.apply_hkr_holidays
        assert not template.apply_hkr_time_table
        assert not template.apply_relay_manual
        assert not template.apply_relay_automatic
        assert not template.apply_level
        assert not template.apply_color
        assert not template.apply_dialhelper
        assert template.supported_features == [
            FritzhomeDeviceFeatures.THERMOSTAT,
            FritzhomeDeviceFeatures.TEMPERATURE,
        ]

    def test_template_removed(self):
        self.mock.side_effect = [
            Helper.response("templates/template_list"),
            Helper.response("templates/template_list_removed_template"),
            Helper.response("templates/template_list_removed_template"),
        ]

        self.fritz.update_templates()
        assert len(self.fritz.get_templates()) == 12
        self.fritz.update_templates()
        assert len(self.fritz.get_templates()) == 12
        self.fritz.update_templates(ignore_removed=False)
        assert len(self.fritz.get_templates()) == 11

    def test_template_with_single_device(self):
        template = self.fritz.get_template_by_ain("tmp0B32F7-1B0650234")

        assert template.devices == ["08735 0525249"]

    def test_template_with_multiple_devices(self):
        template = self.fritz.get_template_by_ain("tmp0B32F7-1C40A2B8A")

        # fmt: off
        expected_devices = set(["08735 0525249",
                                "08735 0525249",
                                "08735 0340143",
                                "08735 0526125"])
        # fmt: on
        assert len(expected_devices.intersection(template.devices)) == len(
            expected_devices
        )

    def test_template_applies_hkr_summer(self):
        template = self.fritz.get_template_by_ain("tmp0B32F7-1B064FA20")

        assert template.apply_hkr_summer
        assert not template.apply_hkr_temperature
        assert not template.apply_hkr_holidays
        assert not template.apply_hkr_time_table
        assert not template.apply_relay_manual
        assert not template.apply_relay_automatic
        assert not template.apply_level
        assert not template.apply_color
        assert not template.apply_dialhelper

    def test_template_applies_hkr_temperature(self):
        template = self.fritz.get_template_by_ain("tmp0B32F7-1B064FA21")

        assert not template.apply_hkr_summer
        assert template.apply_hkr_temperature
        assert not template.apply_hkr_holidays
        assert not template.apply_hkr_time_table
        assert not template.apply_relay_manual
        assert not template.apply_relay_automatic
        assert not template.apply_level
        assert not template.apply_color
        assert not template.apply_dialhelper

    def test_template_applies_hkr_holidays(self):
        template = self.fritz.get_template_by_ain("tmp0B32F7-1B064FA22")

        assert not template.apply_hkr_summer
        assert not template.apply_hkr_temperature
        assert template.apply_hkr_holidays
        assert not template.apply_hkr_time_table
        assert not template.apply_relay_manual
        assert not template.apply_relay_automatic
        assert not template.apply_level
        assert not template.apply_color
        assert not template.apply_dialhelper

    def test_template_applies_hkr_time_table(self):
        template = self.fritz.get_template_by_ain("tmp0B32F7-1B064FA23")

        assert not template.apply_hkr_summer
        assert not template.apply_hkr_temperature
        assert not template.apply_hkr_holidays
        assert template.apply_hkr_time_table
        assert not template.apply_relay_manual
        assert not template.apply_relay_automatic
        assert not template.apply_level
        assert not template.apply_color
        assert not template.apply_dialhelper

    def test_template_applies_relay_manual(self):
        template = self.fritz.get_template_by_ain("tmp0B32F7-1B064FA24")

        assert not template.apply_hkr_summer
        assert not template.apply_hkr_temperature
        assert not template.apply_hkr_holidays
        assert not template.apply_hkr_time_table
        assert template.apply_relay_manual
        assert not template.apply_relay_automatic
        assert not template.apply_level
        assert not template.apply_color
        assert not template.apply_dialhelper

    def test_template_applies_relay_automatic(self):
        template = self.fritz.get_template_by_ain("tmp0B32F7-1B064FA25")

        assert not template.apply_hkr_summer
        assert not template.apply_hkr_temperature
        assert not template.apply_hkr_holidays
        assert not template.apply_hkr_time_table
        assert not template.apply_relay_manual
        assert template.apply_relay_automatic
        assert not template.apply_level
        assert not template.apply_color
        assert not template.apply_dialhelper

    def test_template_applies_level(self):
        template = self.fritz.get_template_by_ain("tmp0B32F7-1B064FA26")

        assert not template.apply_hkr_summer
        assert not template.apply_hkr_temperature
        assert not template.apply_hkr_holidays
        assert not template.apply_hkr_time_table
        assert not template.apply_relay_manual
        assert not template.apply_relay_automatic
        assert template.apply_level
        assert not template.apply_color
        assert not template.apply_dialhelper

    def test_template_applies_color(self):
        template = self.fritz.get_template_by_ain("tmp0B32F7-1B064FA27")

        assert not template.apply_hkr_summer
        assert not template.apply_hkr_temperature
        assert not template.apply_hkr_holidays
        assert not template.apply_hkr_time_table
        assert not template.apply_relay_manual
        assert not template.apply_relay_automatic
        assert not template.apply_level
        assert template.apply_color
        assert not template.apply_dialhelper

    def test_template_applies_dialhelper(self):
        template = self.fritz.get_template_by_ain("tmp0B32F7-1B064FA28")

        assert not template.apply_hkr_summer
        assert not template.apply_hkr_temperature
        assert not template.apply_hkr_holidays
        assert not template.apply_hkr_time_table
        assert not template.apply_relay_manual
        assert not template.apply_relay_automatic
        assert not template.apply_level
        assert not template.apply_color
        assert template.apply_dialhelper

    def test_has_template(self):
        self.mock.side_effect = ["invalid_xml"]
        assert not self.fritz.has_templates()
