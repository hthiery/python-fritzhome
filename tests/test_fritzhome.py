# -*- coding: utf-8 -*-

from requests.exceptions import ConnectionError
from unittest.mock import MagicMock, patch

import pytest

from pyfritzhome import Fritzhome, InvalidError, LoginError

from .helper import Helper


class TestFritzhome(object):
    def setup_method(self):
        self.mock = MagicMock()
        self.fritz = Fritzhome("10.0.0.1", "user", "pass")
        self.fritz._request = self.mock

    def test_login_fail(self):
        self.mock.side_effect = [
            Helper.response("login_rsp_without_valid_sid"),
            Helper.response("login_rsp_without_valid_sid"),
        ]

        with pytest.raises(LoginError) as ex:
            self.fritz.login()
        assert str(ex.value) == 'login for user="user" failed'

    def test_login_connection_error(self):
        self.mock.side_effect = ConnectionError

        with pytest.raises(ConnectionError):
            self.fritz.login()

    def test_login(self):
        self.mock.side_effect = [
            Helper.response("login_rsp_without_valid_sid"),
            Helper.response("login_rsp_with_valid_sid"),
        ]

        self.fritz.login()

    def test_logout(self):
        self.fritz.logout()
        self.fritz._request.assert_called_with(
            "http://10.0.0.1/login_sid.lua",
            {"sid": None, "security:command/logout": "1"},
        )

    def test_aha_request(self):
        self.fritz._aha_request(cmd="testcmd")
        self.fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {"sid": None, "switchcmd": "testcmd"},
        )

        self.fritz._aha_request(cmd="testcmd", ain="1")
        self.fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {"sid": None, "switchcmd": "testcmd", "ain": "1"},
        )

        self.fritz._aha_request(cmd="testcmd", ain="1", param={"a": "1", "b": "2"})
        self.fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {
                "sid": None,
                "switchcmd": "testcmd",
                "ain": "1",
                "a": "1",
                "b": "2",
            },
        )

    def test_aha_request_invalid(self):
        self.mock.side_effect = [
            "inval",
        ]

        with pytest.raises(InvalidError):
            self.fritz._aha_request(cmd="estcmd")

    def test_get_device_element(self):
        self.mock.side_effect = [
            Helper.response("base/device_list"),
            Helper.response("base/device_list"),
            Helper.response("base/device_list"),
        ]

        element = self.fritz.get_device_element("08761 0000434")
        assert element.attrib["identifier"] == "08761 0000434"
        assert element.attrib["fwversion"] == "03.33"

        element = self.fritz.get_device_element("08761 1048079")
        assert element.attrib["identifier"] == "08761 1048079"
        assert element.attrib["fwversion"] == "03.44"

        element = self.fritz.get_device_element("unknown")
        assert element is None

    def test_get_device_by_ain(self):
        self.mock.side_effect = [
            Helper.response("base/device_list"),
            Helper.response("base/device_list"),
        ]

        self.fritz.update_devices()
        device = self.fritz.get_device_by_ain("08761 0000434")
        assert device.ain == "08761 0000434"

    def test_aha_get_devices(self):
        self.mock.side_effect = [
            Helper.response("base/device_list"),
        ]
        self.fritz.update_devices()

        devices = self.fritz.get_devices()
        assert devices[0].name == "Steckdose"
        assert devices[1].name == "FRITZ!DECT Rep 100 #1"

        self.fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {"sid": None, "switchcmd": "getdevicelistinfos"},
        )

    def test_get_device_name(self):
        self.mock.side_effect = ["testname"]

        assert self.fritz.get_device_name(ain="1234") == "testname"

        self.fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {"sid": None, "ain": "1234", "switchcmd": "getswitchname"},
        )

    def test_get_template_by_ain(self):
        self.mock.side_effect = [
            Helper.response("templates/template_list"),
            Helper.response("templates/template_list"),
        ]

        self.fritz.update_templates()
        device = self.fritz.get_template_by_ain("tmp0B32F7-1B0650682")
        assert device.ain == "tmp0B32F7-1B0650682"

    def test_aha_get_templates(self):
        self.mock.side_effect = [
            Helper.response("templates/template_list"),
        ]
        self.fritz.update_templates()

        templates = self.fritz.get_templates()
        assert templates[0].name == "Base Data"
        assert templates[1].name == "One Device"

        self.fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {"sid": None, "switchcmd": "gettemplatelistinfos"},
        )

    def test_aha_apply_template(self):
        self.fritz.apply_template("1234")

        self.fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {"sid": None, "ain": "1234", "switchcmd": "applytemplate"},
        )

    def test_set_target_temperature(self):
        self.fritz.set_target_temperature("1", 25.5)
        self.fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {"sid": None, "ain": "1", "switchcmd": "sethkrtsoll", "param": 51},
        )

        self.fritz.set_target_temperature("1", 0.0)
        self.fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {"sid": None, "ain": "1", "switchcmd": "sethkrtsoll", "param": 253},
        )

        self.fritz.set_target_temperature("1", 32.0)
        self.fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {"sid": None, "ain": "1", "switchcmd": "sethkrtsoll", "param": 254},
        )

    @patch("time.time", MagicMock(return_value=1000))
    def test_set_window_open(self):
        self.fritz.set_window_open("1", 25)
        self.fritz._request.assert_called_with(
            "http://10.0.0.1/webservices/homeautoswitch.lua",
            {
                "sid": None,
                "ain": "1",
                "switchcmd": "sethkrwindowopen",
                "endtimestamp": 1000 + 25,
            },
        )
