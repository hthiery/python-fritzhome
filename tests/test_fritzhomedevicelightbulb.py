#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest.mock import MagicMock

from pyfritzhome import Fritzhome
from pyfritzhome.devicetypes.fritzhomedevicefeatures import FritzhomeDeviceFeatures

from .helper import Helper


class TestFritzhomeDeviceLightBulb(object):
    def setup_method(self):
        self.mock = MagicMock()
        self.fritz = Fritzhome("10.0.0.1", "user", "pass")
        self.fritz._request = self.mock
        self.fritz._devices = {}
        self.fritz._sid = "0000001"

    def test_device_init(self):
        self.mock.side_effect = [
            Helper.response("lightbulb/device_FritzDECT500_34_12_16")
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345")

        assert device.ain == "12345"
        assert device.fw_version == "34.10.16.16.009"
        assert device.present  # Lightbulb has power and is connected
        assert device.supported_features == [FritzhomeDeviceFeatures.HANFUN_DEVICE]

        # Get sub-device
        device = self.fritz.get_device_by_ain("12345-1")
        assert device.has_lightbulb
        assert device.has_level
        assert device.has_color
        assert device.state  # Lightbulb is switched on
        assert device.color_mode == "1"
        assert device.supported_color_mode == "5"
        assert device.fullcolorsupport
        assert device.hue == 358
        assert device.saturation == 180
        assert device.color_temp is None
        assert device.name == "FRITZ!DECT 500 Büro"
        assert device.supported_features == [
            FritzhomeDeviceFeatures.LIGHTBULB,
            FritzhomeDeviceFeatures.HANFUN_UNIT,
            FritzhomeDeviceFeatures.SWITCHABLE,
            FritzhomeDeviceFeatures.LEVEL,
            FritzhomeDeviceFeatures.COLOR,
        ]

    def test_device_init_non_color_bulb(self):
        self.mock.side_effect = [
            Helper.response("lightbulb/device_Telekom_Magenta_NonColorBulb")
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12701 0072784")

        assert device.ain == "12701 0072784"
        assert device.fw_version == "34.09.15.16.018"
        assert device.present  # Lightbulb has power and is connected

        # Get sub-device
        device = self.fritz.get_device_by_ain("12701 0072784-1")
        assert device.has_lightbulb
        assert device.has_level
        assert not device.fullcolorsupport
        assert device.state  # Lightbulb is switched on
        assert device.name == "Telekom White Dimmable Bulb"

    def test_device_init_color_temp_mode(self):
        self.mock.side_effect = [
            Helper.response("lightbulb/device_FritzDECT500_34_12_16_color_temp_mode")
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345")

        assert device.ain == "12345"
        assert device.fw_version == "34.10.16.16.009"
        assert device.present  # Lightbulb has power and is connected

        # Get sub-device
        device = self.fritz.get_device_by_ain("12345-1")
        assert device.has_lightbulb
        assert device.state  # Lightbulb is switched on
        assert device.color_mode == "4"
        assert device.supported_color_mode == "5"
        assert device.fullcolorsupport
        assert device.hue is None
        assert device.saturation is None
        assert device.color_temp == 2800
        assert device.name == "FRITZ!DECT 500 Büro"

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
        # fmt: off
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
        # fmt: on
        assert colors == expected_colors

    def test_get_colors_NonColorBulb(self):
        self.mock.side_effect = [
            Helper.response("lightbulb/device_Telekom_Magenta_NonColorBulb")
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12701 0072784")

        temps = device.get_colors()
        # No colors and no exception
        assert temps == {}

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
            "2700",
            "3000",
            "3400",
            "3800",
            "4200",
            "4700",
            "5300",
            "5900",
            "6500",
        ]
        assert temps == expected_temps

    def test_get_color_temps_NonColorBulb(self):
        self.mock.side_effect = [
            Helper.response("lightbulb/device_Telekom_Magenta_NonColorBulb")
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12701 0072784")

        temps = device.get_color_temps()
        # No color temps and no exception
        assert temps == []

    def test_set_color(self):
        self.mock.side_effect = [
            Helper.response("lightbulb/device_FritzDECT500_34_12_16"),
            "1",
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345-1")

        device.set_color(["180", "200"], 0)

        device._fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {
                "switchcmd": "setcolor",
                "sid": "0000001",
                "hue": 180,
                "saturation": 200,
                "duration": 0,
                "ain": "12345-1",
            },
        )

    def test_set_color_temp(self):
        self.mock.side_effect = [
            Helper.response("lightbulb/device_FritzDECT500_34_12_16"),
            "1",
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345-1")

        device.set_color_temp(3000, 0)

        device._fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {
                "switchcmd": "setcolortemperature",
                "sid": "0000001",
                "temperature": 3000,
                "duration": 0,
                "ain": "12345-1",
            },
        )

    def test_set_unmapped_color(self):
        self.mock.side_effect = [
            Helper.response("lightbulb/device_FritzDECT500_34_12_16"),
            "1",
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345-1")

        device.set_unmapped_color(["180", "200"], 0)

        device._fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {
                "switchcmd": "setunmappedcolor",
                "sid": "0000001",
                "hue": 180,
                "saturation": 200,
                "duration": 0,
                "ain": "12345-1",
            },
        )

    def test_set_state_off(self):
        self.mock.side_effect = [
            Helper.response("lightbulb/device_FritzDECT500_34_12_16"),
            "1",
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345-1")

        device.set_state_off()

        device._fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {
                "switchcmd": "setsimpleonoff",
                "sid": "0000001",
                "onoff": 0,
                "ain": "12345-1",
            },
        )

    def test_set_state_on(self):
        self.mock.side_effect = [
            Helper.response("lightbulb/device_FritzDECT500_34_12_16"),
            "1",
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345-1")

        device.set_state_on()

        device._fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {
                "switchcmd": "setsimpleonoff",
                "sid": "0000001",
                "onoff": 1,
                "ain": "12345-1",
            },
        )

    def test_set_state_toggle(self):
        self.mock.side_effect = [
            Helper.response("lightbulb/device_FritzDECT500_34_12_16"),
            "1",
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("12345-1")

        device.set_state_toggle()

        device._fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {
                "switchcmd": "setsimpleonoff",
                "sid": "0000001",
                "onoff": 2,
                "ain": "12345-1",
            },
        )
