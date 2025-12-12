#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest.mock import MagicMock

from pyfritzhome import Fritzhome

from .helper import Helper


class TestFritzhomeTrigger(object):
    def setup_method(self):
        self.mock = MagicMock()
        self.fritz = Fritzhome("10.0.0.1", "user", "pass")
        self.fritz._request = self.mock
        self.fritz._devices = {}
        self.fritz._sid = "0000001"

        self.mock.side_effect = [Helper.response("triggers/trigger_list")]

        self.fritz.update_triggers()

    def test_trigger_init(self):
        trigger = self.fritz.get_trigger_by_ain("trg303e4f-41979A02D")

        assert trigger.ain == "trg303e4f-41979A02D"
        assert trigger.active

        trigger = self.fritz.get_trigger_by_ain("trg405e4a-57AE9A80A")

        assert trigger.ain == "trg405e4a-57AE9A80A"
        assert not trigger.active

    def test_trigger_removed(self):
        self.mock.side_effect = [
            Helper.response("triggers/trigger_list"),
            Helper.response("triggers/trigger_list_removed_trigger"),
            Helper.response("triggers/trigger_list_removed_trigger"),
        ]

        self.fritz.update_triggers()
        assert len(self.fritz.get_triggers()) == 2
        self.fritz.update_triggers()
        assert len(self.fritz.get_triggers()) == 2
        self.fritz.update_triggers(ignore_removed=False)
        assert len(self.fritz.get_triggers()) == 1

    def test_has_trigger(self):
        self.mock.side_effect = [
            "invalid_xml",
            Helper.response("triggers/trigger_list"),
        ]
        assert not self.fritz.has_triggers()
        assert self.fritz.has_triggers()

    def test_set_trigger_active(self):
        self.mock.side_effect = [
            Helper.response("triggers/trigger_list"),
            "1",
        ]
        self.fritz.update_triggers()

        self.fritz.set_trigger_active("trg303e4f-41979A02D")
        self.fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {
                "switchcmd": "settriggeractive",
                "sid": "0000001",
                "active": "1",
                "ain": "trg303e4f-41979A02D",
            },
        )

    def test_set_trigger_inactive(self):
        self.mock.side_effect = [
            Helper.response("triggers/trigger_list"),
            "1",
        ]
        self.fritz.update_triggers()

        self.fritz.set_trigger_inactive("trg303e4f-41979A02D")
        self.fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {
                "switchcmd": "settriggeractive",
                "sid": "0000001",
                "active": "0",
                "ain": "trg303e4f-41979A02D",
            },
        )
