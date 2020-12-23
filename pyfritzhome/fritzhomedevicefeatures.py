from enum import IntFlag


class FritzhomeDeviceFeatures(IntFlag):
    # Bit 0: HAN-FUN Gerät
    # Bit 2: Licht/Lampe
    ALARM = 0x0010          # Bit 4: Alarm-Sensor
    BUTTON = 0x0020         # Bit 5: AVM-Button
    THERMOSTAT = 0x0040     # Bit 6: Heizkörperregler
    POWER_METER = 0x0080    # Bit 7: Energie Messgerät
    TEMPERATURE = 0x0100    # Bit 8: Temperatursensor
    SWITCH = 0x0200         # Bit 9: Schaltsteckdose
    DECT_REPEATER = 0x0400  # Bit 10: AVM DECT Repeater
    MICROPHONE = 0x0800     # Bit 11: Mikrofon
    HANFUN = 0x2000         # Bit 13: HAN-FUN-Unit
    # Bit 15: an-/ausschaltbares Gerät/Steckdose/Lampe/Aktor
    # Bit 16: Gerät mit einstellbarem Dimm-, Höhen- bzw. Niveau-Level
    # Bit 17: Lampe mit einstellbarer Farbe/Farbtemperatur
