#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import logging
import argparse

try:
    from version import __version__
except ImportError:
    __version__ = "dev"

from pyfritzhome import Fritzhome

_LOGGER = logging.getLogger(__name__)


def list_all(fritz, args):
    """Command that prints all device information."""
    devices = fritz.get_devices()

    for device in devices:
        print("#" * 30)
        print("name=%s" % device.name)
        print("  ain=%s" % device.ain)
        print("  id=%s" % device.identifier)
        print("  productname=%s" % device.productname)
        print("  manufacturer=%s" % device.manufacturer)
        print("  present=%s" % device.present)
        print("  lock=%s" % device.lock)
        print("  devicelock=%s" % device.device_lock)

        if device.present is False:
            continue

        if device.has_switch:
            print(" Switch:")
            print("  switch_state=%s" % device.switch_state)
        if device.has_switch:
            print(" Powermeter:")
            print("  power=%s" % device.power)
            print("  energy=%s" % device.energy)
            print("  voltage=%s" % device.voltage)
        if device.has_temperature_sensor:
            print(" Temperature:")
            print("  temperature=%s" % device.temperature)
            print("  offset=%s" % device.offset)
        if device.has_thermostat:
            print(" Thermostat:")
            print("  battery_low=%s" % device.battery_low)
            print("  battery_level=%s" % device.battery_level)
            print("  actual=%s" % device.actual_temperature)
            print("  target=%s" % device.target_temperature)
            print("  comfort=%s" % device.comfort_temperature)
            print("  eco=%s" % device.eco_temperature)
            print("  window=%s" % device.window_open)
            print("  summer=%s" % device.summer_active)
            print("  holiday=%s" % device.holiday_active)
        if device.has_alarm:
            print(" Alert:")
            print("  alert=%s" % device.alert_state)
        if device.has_lightbulb:
            print(" Light bulb:")
            print("  state=%s" % ("Off" if device.state == 0 else "On"))
            print("  level=%s" % device.level)
            print("  hue=%s" % device.hue)
            print("  saturation=%s" % device.saturation)


def device_name(fritz, args):
    """Command that prints the device name."""
    print(fritz.get_device_name(args.ain))


def device_presence(fritz, args):
    """Command that prints the device presence."""
    print(int(fritz.get_device_present(args.ain)))


def device_statistics(fritz, args):
    """Command that prints the device statistics."""
    stats = fritz.get_device_statistics(args.ain)
    print(stats)


def switch_get(fritz, args):
    """Command that get the device switch state."""
    print(fritz.get_switch_state(args.ain))


def switch_on(fritz, args):
    """Command that set the device switch state to on."""
    fritz.set_switch_state_on(args.ain)


def switch_off(fritz, args):
    """Command that set the device switch state to off."""
    fritz.set_switch_state_off(args.ain)


def switch_toggle(fritz, args):
    """Command that toggles the device switch state."""
    fritz.set_switch_state_toggle(args.ain)


def list_templates(fritz, args):
    """Command that prints all template information."""
    templates = fritz.get_templates()
    devices = fritz.get_devices_as_dict()

    for template in templates:
        print("#" * 30)
        print("name=%s" % template.name)
        print("  ain=%s" % template.ain)

        print(" Apply:")
        print("  hkr_summer=%s" % template.apply_hkr_summer)
        print("  hkr_temperature=%s" % template.apply_hkr_temperature)
        print("  hkr_holidays=%s" % template.apply_hkr_holidays)
        print("  hkr_time_table=%s" % template.apply_hkr_time_table)
        print("  relay_manual=%s" % template.apply_relay_manual)
        print("  relay_automatic=%s" % template.apply_relay_automatic)
        print("  level=%s" % template.apply_level)
        print("  color=%s" % template.apply_color)
        print("  dialhelper=%s" % template.apply_dialhelper)

        print(" Devices:")
        for device_id in template.devices:
            print("  %s=%s" % (device_id, devices[device_id].name))


def template_apply(fritz, args):
    """Command that applies a template."""
    fritz.apply_template(args.ain)


def main(args=None):
    """The main function."""
    parser = argparse.ArgumentParser(description="Fritz!Box Smarthome CLI tool.")
    parser.add_argument(
        "-v", action="store_true", dest="verbose", help="be more verbose"
    )
    parser.add_argument(
        "-f",
        "--fritzbox",
        type=str,
        dest="host",
        help="Fritz!Box IP address",
        default="fritz.box",
    )
    parser.add_argument("-u", "--user", type=str, dest="user", help="Username")
    parser.add_argument("-p", "--password", type=str, dest="password", help="Username")
    parser.add_argument(
        "-a",
        "--ain",
        type=str,
        dest="ain",
        help="Actor/Template Identification",
        default=None,
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="{version}".format(version=__version__),
        help="Print version",
    )

    _sub = parser.add_subparsers(title="Commands")

    # list all devices
    subparser = _sub.add_parser("list", help="List all available devices")
    subparser.set_defaults(func=list_all)

    # device
    subparser = _sub.add_parser("device", help="Device/Actor commands")
    _sub_switch = subparser.add_subparsers()

    # device name
    subparser = _sub_switch.add_parser("name", help="get the device name")
    subparser.add_argument("ain", type=str, metavar="AIN", help="Actor Identification")
    subparser.set_defaults(func=device_name)

    # device presence
    subparser = _sub_switch.add_parser("present", help="get the device presence")
    subparser.add_argument("ain", type=str, metavar="AIN", help="Actor Identification")
    subparser.set_defaults(func=device_presence)

    # device stats
    subparser = _sub_switch.add_parser("stats", help="get the device statistics")
    subparser.add_argument("ain", type=str, metavar="AIN", help="Actor Identification")
    subparser.set_defaults(func=device_statistics)

    # switch
    subparser = _sub.add_parser("switch", help="Switch commands")
    _sub_switch = subparser.add_subparsers()

    # switch get
    subparser = _sub_switch.add_parser("get", help="get state")
    subparser.add_argument("ain", type=str, metavar="AIN", help="Actor Identification")
    subparser.set_defaults(func=switch_get)

    # switch on
    subparser = _sub_switch.add_parser("on", help="set on state")
    subparser.add_argument("ain", type=str, metavar="AIN", help="Actor Identification")
    subparser.set_defaults(func=switch_on)

    # switch off
    subparser = _sub_switch.add_parser("off", help="set off state")
    subparser.add_argument("ain", type=str, metavar="AIN", help="Actor Identification")
    subparser.set_defaults(func=switch_off)

    # switch toggle
    subparser = _sub_switch.add_parser("toggle", help="set off state")
    subparser.add_argument("ain", type=str, metavar="AIN", help="Actor Identification")
    subparser.set_defaults(func=switch_toggle)

    # templates
    subparser = _sub.add_parser("template", help="Template commands")
    _sub_switch = subparser.add_subparsers()

    # list templates
    subparser = _sub_switch.add_parser("list", help="List all available templates")
    subparser.set_defaults(func=list_templates)

    # apply templates
    subparser = _sub_switch.add_parser("apply", help="Apply template")
    subparser.set_defaults(func=template_apply)

    args = parser.parse_args(args)

    logging.basicConfig()
    if args.verbose:
        logging.getLogger("pyfritzhome").setLevel(logging.DEBUG)

    fritzbox = None
    try:
        fritzbox = Fritzhome(host=args.host, user=args.user, password=args.password)
        fritzbox.login()
        args.func(fritzbox, args)
    finally:
        if fritzbox is not None:
            fritzbox.logout()


if __name__ == "__main__":
    main()
