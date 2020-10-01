# -*- coding: utf-8 -*-
from .device import (
    FritzhomeAlarmDevice,
    FritzhomePowermeterDevice,
    FritzhomeRepeaterDevice,
    FritzhomeSwitchDevice,
    FritzhomeTemperatureDevice,
    FritzhomeThermostatDevice,
)


class FritzhomeDevice(
    FritzhomeAlarmDevice,
    FritzhomePowermeterDevice,
    FritzhomeRepeaterDevice,
    FritzhomeSwitchDevice,
    FritzhomeTemperatureDevice,
    FritzhomeThermostatDevice,
):
    pass
