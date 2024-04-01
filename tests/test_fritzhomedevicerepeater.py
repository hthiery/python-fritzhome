#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest.mock import MagicMock

from pyfritzhome import Fritzhome


class TestFritzhomeDeviceRepeater(object):
    def setup_method(self):
        self.mock = MagicMock()
        self.fritz = Fritzhome("10.0.0.1", "user", "pass")
        self.fritz._request = self.mock
        self.fritz._devices = {}
        self.fritz._sid = "0000001"
