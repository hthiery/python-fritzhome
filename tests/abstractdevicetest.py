#!/usr/bin/env python
# -*- coding: utf-8 -*-


from mock import MagicMock

from pyfritzhome import FritzhomeDevice, Fritzhome

from abc import ABC


class AbstractTestDevice(ABC):

    fritz = None
    mock = None
    __responses = {}

    def setup(self):
        self.mock = MagicMock()
        self.fritz = Fritzhome("10.0.0.1", "user", "pass")
        self.fritz._request = self.mock

    def response(self, file: str):
        if file not in self.__responses:
            with open("tests/responses/" + file + ".xml", "r") as file:
                self.__responses[file] = file.read()
        return self.__responses[file]

    def get_switch_test_device(self):
        self.mock.side_effect = [self.response("device_list"), "1"]
        element = self.fritz.get_device_element("08761 0000434")
        device = FritzhomeDevice(fritz=self.fritz, node=element)
        return device
