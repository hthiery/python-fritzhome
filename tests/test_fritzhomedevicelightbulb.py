#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import eq_, assert_true
from unittest.mock import MagicMock
from .helper import Helper

from pyfritzhome import Fritzhome


class TestFritzhomeDeviceLightBulb(object):
    def setup(self):
        self.mock = MagicMock()
        self.fritz = Fritzhome("10.0.0.1", "user", "pass")
        self.fritz._request = self.mock
        self.fritz._devices = {}

    def test_device_init(self):
        self.mock.side_effect = [
            Helper.response("lightbulb/device_FritzDECT500_34_12_16")
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345")

        eq_(device.ain, "12345")
        eq_(device.fw_version, "34.10.16.16.009")
        assert_true(device.present)  # Lightbulb has power and is connected

        # Get sub-device
        device = self.fritz.get_device_by_ain("12345-1")
        assert_true(device.has_lightbulb)
        assert_true(device.state)  # Lightbulb is switched on
        eq_(device.name, u"FRITZ!DECT 500 Büro")

    def test_get_colors(self):
        self.mock.side_effect = [
            Helper.response("lightbulb/device_FritzDECT500_34_12_16")
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345-1")

        self.mock.side_effect = [
            Helper.response("lightbulb/getcolors_FritzDECT500_34_12_16")
        ]

        colors = device.get_colors()
        expected_colors = {
            'Rot': [
                ('358', '180', '230'),
                ('358', '112', '237'),
                ('358', '54', '245')
                ],
            'Orange': [
                ('35', '214', '255'),
                ('35', '140', '255'),
                ('35', '72', '255')
                ],
            'Gelb': [
                ('52', '153', '252'),
                ('52', '102', '252'),
                ('52', '51', '255')
                ],
            'Grasgrün': [
                ('92', '123', '248'),
                ('92', '79', '250'),
                ('92', '38', '252')
                ],
            'Grün': [
                ('120', '160', '220'),
                ('120', '82', '232'),
                ('120', '38', '242')
                ],
            'Türkis': [
                ('160', '145', '235'),
                ('160', '84', '242'),
                ('160', '41', '248')
                ],
            'Cyan': [
                ('195', '179', '255'),
                ('195', '118', '255'),
                ('195', '59', '255')
                ],
            'Himmelblau': [
                ('212', '169', '252'),
                ('212', '110', '252'),
                ('212', '56', '255')
                ],
            'Blau': [
                ('225', '204', '255'),
                ('225', '135', '255'),
                ('225', '67', '255')
                ],
            'Violett': [
                ('266', '169', '250'),
                ('266', '110', '250'),
                ('266', '54', '252')
                ],
            'Magenta': [
                ('296', '140', '250'),
                ('296', '92', '252'),
                ('296', '46', '255')
                ],
            'Pink': [
                ('335', '180', '255'),
                ('335', '107', '248'),
                ('335', '51', '250')
                ]
            }
        eq_(colors, expected_colors)

    def test_get_color_temps(self):
        self.mock.side_effect = [
            Helper.response("lightbulb/device_FritzDECT500_34_12_16")
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345-1")

        self.mock.side_effect = [
            Helper.response("lightbulb/getcolors_FritzDECT500_34_12_16")
        ]

        temps = device.get_color_temps()
        expected_temps = [
            '2700',
            '3000',
            '3400',
            '3800',
            '4200',
            '4700',
            '5300',
            '5900',
            '6500'
            ]
        eq_(temps, expected_temps)
