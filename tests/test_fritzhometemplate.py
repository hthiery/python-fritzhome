#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest.mock import MagicMock

from nose.tools import assert_false, assert_true, eq_

from pyfritzhome import Fritzhome

from .helper import Helper


class TestFritzhomeTemplate(object):
    def setup(self):
        self.mock = MagicMock()
        self.fritz = Fritzhome("10.0.0.1", "user", "pass")
        self.fritz._request = self.mock
        self.fritz._devices = {}

        self.mock.side_effect = [Helper.response("templates/template_list")]

        self.fritz.update_templates()

    def test_template_init(self):
        template = self.fritz.get_template_by_ain("tmp0B32F7-1B0650682")

        eq_(template.ain, "tmp0B32F7-1B0650682")
        eq_(template._functionsbitmask, 320)
        assert_false(template.apply_hkr_summer)
        assert_false(template.apply_hkr_temperature)
        assert_false(template.apply_hkr_holidays)
        assert_false(template.apply_hkr_time_table)
        assert_false(template.apply_relay_manual)
        assert_false(template.apply_relay_automatic)
        assert_false(template.apply_level)
        assert_false(template.apply_color)
        assert_false(template.apply_dialhelper)

    def test_template_with_single_device(self):
        template = self.fritz.get_template_by_ain("tmp0B32F7-1B0650234")

        eq_(template.devices, ["08735 0525249"])

    def test_template_with_multiple_devices(self):
        template = self.fritz.get_template_by_ain("tmp0B32F7-1C40A2B8A")

        # fmt: off
        expected_devices = set(["08735 0525249",
                                "08735 0525249",
                                "08735 0340143",
                                "08735 0526125"])
        # fmt: on

        eq_(len(expected_devices.intersection(template.devices)), len(expected_devices))

    def test_template_applies_hkr_summer(self):
        template = self.fritz.get_template_by_ain("tmp0B32F7-1B064FA20")

        assert_true(template.apply_hkr_summer)
        assert_false(template.apply_hkr_temperature)
        assert_false(template.apply_hkr_holidays)
        assert_false(template.apply_hkr_time_table)
        assert_false(template.apply_relay_manual)
        assert_false(template.apply_relay_automatic)
        assert_false(template.apply_level)
        assert_false(template.apply_color)
        assert_false(template.apply_dialhelper)

    def test_template_applies_hkr_temperature(self):
        template = self.fritz.get_template_by_ain("tmp0B32F7-1B064FA21")

        assert_false(template.apply_hkr_summer)
        assert_true(template.apply_hkr_temperature)
        assert_false(template.apply_hkr_holidays)
        assert_false(template.apply_hkr_time_table)
        assert_false(template.apply_relay_manual)
        assert_false(template.apply_relay_automatic)
        assert_false(template.apply_level)
        assert_false(template.apply_color)
        assert_false(template.apply_dialhelper)

    def test_template_applies_hkr_holidays(self):
        template = self.fritz.get_template_by_ain("tmp0B32F7-1B064FA22")

        assert_false(template.apply_hkr_summer)
        assert_false(template.apply_hkr_temperature)
        assert_true(template.apply_hkr_holidays)
        assert_false(template.apply_hkr_time_table)
        assert_false(template.apply_relay_manual)
        assert_false(template.apply_relay_automatic)
        assert_false(template.apply_level)
        assert_false(template.apply_color)
        assert_false(template.apply_dialhelper)

    def test_template_applies_hkr_time_table(self):
        template = self.fritz.get_template_by_ain("tmp0B32F7-1B064FA23")

        assert_false(template.apply_hkr_summer)
        assert_false(template.apply_hkr_temperature)
        assert_false(template.apply_hkr_holidays)
        assert_true(template.apply_hkr_time_table)
        assert_false(template.apply_relay_manual)
        assert_false(template.apply_relay_automatic)
        assert_false(template.apply_level)
        assert_false(template.apply_color)
        assert_false(template.apply_dialhelper)

    def test_template_applies_relay_manual(self):
        template = self.fritz.get_template_by_ain("tmp0B32F7-1B064FA24")

        assert_false(template.apply_hkr_summer)
        assert_false(template.apply_hkr_temperature)
        assert_false(template.apply_hkr_holidays)
        assert_false(template.apply_hkr_time_table)
        assert_true(template.apply_relay_manual)
        assert_false(template.apply_relay_automatic)
        assert_false(template.apply_level)
        assert_false(template.apply_color)
        assert_false(template.apply_dialhelper)

    def test_template_applies_relay_automatic(self):
        template = self.fritz.get_template_by_ain("tmp0B32F7-1B064FA25")

        assert_false(template.apply_hkr_summer)
        assert_false(template.apply_hkr_temperature)
        assert_false(template.apply_hkr_holidays)
        assert_false(template.apply_hkr_time_table)
        assert_false(template.apply_relay_manual)
        assert_true(template.apply_relay_automatic)
        assert_false(template.apply_level)
        assert_false(template.apply_color)
        assert_false(template.apply_dialhelper)

    def test_template_applies_level(self):
        template = self.fritz.get_template_by_ain("tmp0B32F7-1B064FA26")

        assert_false(template.apply_hkr_summer)
        assert_false(template.apply_hkr_temperature)
        assert_false(template.apply_hkr_holidays)
        assert_false(template.apply_hkr_time_table)
        assert_false(template.apply_relay_manual)
        assert_false(template.apply_relay_automatic)
        assert_true(template.apply_level)
        assert_false(template.apply_color)
        assert_false(template.apply_dialhelper)

    def test_template_applies_color(self):
        template = self.fritz.get_template_by_ain("tmp0B32F7-1B064FA27")

        assert_false(template.apply_hkr_summer)
        assert_false(template.apply_hkr_temperature)
        assert_false(template.apply_hkr_holidays)
        assert_false(template.apply_hkr_time_table)
        assert_false(template.apply_relay_manual)
        assert_false(template.apply_relay_automatic)
        assert_false(template.apply_level)
        assert_true(template.apply_color)
        assert_false(template.apply_dialhelper)

    def test_template_applies_dialhelper(self):
        template = self.fritz.get_template_by_ain("tmp0B32F7-1B064FA28")

        assert_false(template.apply_hkr_summer)
        assert_false(template.apply_hkr_temperature)
        assert_false(template.apply_hkr_holidays)
        assert_false(template.apply_hkr_time_table)
        assert_false(template.apply_relay_manual)
        assert_false(template.apply_relay_automatic)
        assert_false(template.apply_level)
        assert_false(template.apply_color)
        assert_true(template.apply_dialhelper)
