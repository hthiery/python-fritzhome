#!/usr/bin/env python
"""A simple CLI tool."""

from __future__ import annotations

from collections.abc import Sequence
import logging
import argparse


from pyfritzhome import Fritzhome, __version__

_LOGGER = logging.getLogger(__name__)


def list_all(fritz: Fritzhome, args: argparse.Namespace) -> None:
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
        print("  is_group=%s" % device.is_group)
        if device.is_group:
            print("  group_members=%s" % device.group_members)

        if device.present is False:
            continue

        if device.has_switch:
            print(" Switch:")
            print("  switch_state=%s" % device.switch_state)
        if device.has_powermeter:
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
            print("  window_until=%s" % device.window_open_endtime)
            print("  boost=%s" % device.boost_active)
            print("  boost_until=%s" % device.boost_active_endtime)
            print("  adaptive_heating_running=%s" % device.adaptive_heating_running)
            print("  summer=%s" % device.summer_active)
            print("  holiday=%s" % device.holiday_active)
        if device.has_alarm:
            print(" Alert:")
            print("  alert=%s" % device.alert_state)
        if device.has_lightbulb:
            print(" Light bulb:")
            print("  state=%s" % ("Off" if device.state == 0 else "On"))
            if device.has_level:
                print("  level=%s" % device.level)
            if device.has_color:
                print("  hue=%s" % device.hue)
                print("  saturation=%s" % device.saturation)
        if device.has_blind:
            print(" Blind:")
            print("  level=%s" % device.level)
            print("  levelpercentage=%s" % device.levelpercentage)
            print("  endpositionset=%s" % device.endpositionsset)


def device_name(fritz: Fritzhome, args: argparse.Namespace) -> None:
    """Command that prints the device name."""
    print(fritz.get_device_name(args.ain))


def device_presence(fritz: Fritzhome, args: argparse.Namespace) -> None:
    """Command that prints the device presence."""
    print(int(fritz.get_device_present(args.ain)))


def device_statistics(fritz: Fritzhome, args: argparse.Namespace) -> None:
    """Command that prints the device statistics."""
    stats = fritz.get_device_statistics(args.ain)
    print(stats)


def blind_set_open(fritz: Fritzhome, args: argparse.Namespace) -> None:
    """Command to open the blinds."""
    fritz.set_blind_open(args.ain)


def blind_set_close(fritz: Fritzhome, args: argparse.Namespace) -> None:
    """Command close the blinds."""
    fritz.set_blind_close(args.ain)


def blind_set_level_percentage(fritz: Fritzhome, args: argparse.Namespace) -> None:
    """Command that sets the blind level as percentage."""
    fritz.set_level_percentage(args.ain, args.level)


def thermostat_set_target_temperature(
    fritz: Fritzhome, args: argparse.Namespace
) -> None:
    """Command that sets the thermostat temperature."""
    fritz.set_target_temperature(args.ain, args.temperature)


def thermostat_set_window_open(fritz: Fritzhome, args: argparse.Namespace) -> None:
    """Command that sets the thermostats window state."""
    fritz.set_window_open(args.ain, args.timespan)


def thermostat_set_boost_mode(fritz: Fritzhome, args: argparse.Namespace) -> None:
    """Command that sets the thermostats into boost mode."""
    fritz.set_boost_mode(args.ain, args.timespan)


def switch_get(fritz: Fritzhome, args: argparse.Namespace) -> None:
    """Command that get the device switch state."""
    print(fritz.get_switch_state(args.ain))


def switch_on(fritz: Fritzhome, args: argparse.Namespace) -> None:
    """Command that set the device switch state to on."""
    fritz.set_switch_state_on(args.ain)


def switch_off(fritz: Fritzhome, args: argparse.Namespace) -> None:
    """Command that set the device switch state to off."""
    fritz.set_switch_state_off(args.ain)


def switch_toggle(fritz: Fritzhome, args: argparse.Namespace) -> None:
    """Command that toggles the device switch state."""
    fritz.set_switch_state_toggle(args.ain)


def list_templates(fritz: Fritzhome, args: argparse.Namespace) -> None:
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
        if template.devices is not None:
            for device_id in template.devices:
                print("  %s=%s" % (device_id, devices[device_id].name))


def template_apply(fritz: Fritzhome, args: argparse.Namespace) -> None:
    """Command that applies a template."""
    fritz.apply_template(args.ain)


def list_triggers(fritz: Fritzhome, args: argparse.Namespace) -> None:
    """Command that prints all trigger information."""
    triggers = fritz.get_triggers()

    for trigger in triggers:
        print("#" * 30)
        print("name=%s" % trigger.name)
        print("  ain=%s" % trigger.ain)
        print("  active=%s" % trigger.active)


def trigger_set_active(fritz: Fritzhome, args: argparse.Namespace) -> None:
    """Command that enables a trigger."""
    fritz.set_trigger_active(args.ain)


def trigger_set_inactive(fritz: Fritzhome, args: argparse.Namespace) -> None:
    """Command that disables a trigger."""
    fritz.set_trigger_inactive(args.ain)


def main(args: Sequence[str] | None = None) -> None:
    """Enter the main function of the CLI tool."""
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
    parser.add_argument("--port", type=int, dest="port", help="Port")
    parser.add_argument(
        "--insecure",
        action="store_true",
        dest="insecure",
        help="Don't verify SSL certificates",
    )
    parser.add_argument("-u", "--user", type=str, dest="user", help="Username")
    parser.add_argument("-p", "--password", type=str, dest="password", help="Password")
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

    # blind
    subparser = _sub.add_parser("blind", help="Blind commands")
    _sub_switch = subparser.add_subparsers()

    # blind open
    subparser = _sub_switch.add_parser("open", help="open blinds")
    subparser.add_argument("ain", type=str, metavar="AIN", help="Actor Identification")
    subparser.set_defaults(func=blind_set_open)

    # blind close
    subparser = _sub_switch.add_parser("close", help="close blinds")
    subparser.add_argument("ain", type=str, metavar="AIN", help="Actor Identification")
    subparser.set_defaults(func=blind_set_close)

    # blind set level in percentage
    subparser = _sub_switch.add_parser(
        "set_level", help="set level of blinds in percentage (0=open)"
    )
    subparser.add_argument("ain", type=str, metavar="AIN", help="Actor Identification")
    subparser.add_argument(
        "level", type=float, metavar="LEVEL", help="blind level in percentage (0=open)"
    )
    subparser.set_defaults(func=blind_set_level_percentage)

    # thermostat
    subparser = _sub.add_parser("thermostat", help="Thermostat commands")
    _sub_switch = subparser.add_subparsers()

    # thermostat target temperature
    subparser = _sub_switch.add_parser(
        "set_target_temperature", help="set target temperature"
    )
    subparser.add_argument("ain", type=str, metavar="AIN", help="Actor Identification")
    subparser.add_argument(
        "temperature",
        type=float,
        metavar="TEMPERATURE",
        help="target temperature in (C)",
    )
    subparser.set_defaults(func=thermostat_set_target_temperature)

    # thermostat window_open
    subparser = _sub_switch.add_parser(
        "set_window_open", help="set window state to open"
    )
    subparser.add_argument("ain", type=str, metavar="AIN", help="Actor Identification")
    subparser.add_argument(
        "timespan",
        type=int,
        metavar="TIMESPAN",
        nargs="?",
        default=300,
        help="Open timespan in seconds (default=300s)",
    )
    subparser.set_defaults(func=thermostat_set_window_open)

    # thermostat boost_mpde
    subparser = _sub_switch.add_parser("set_boost_mode", help="activate the boost mode")
    subparser.add_argument("ain", type=str, metavar="AIN", help="Actor Identification")
    subparser.add_argument(
        "timespan",
        type=int,
        choices=range(0, 86400),
        metavar="TIMESPAN",
        nargs="?",
        default=300,
        help="Boost timespan in seconds (default=300s)",
    )
    subparser.set_defaults(func=thermostat_set_boost_mode)

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
    subparser.add_argument("ain", type=str, metavar="AIN", help="Actor Identification")
    subparser.set_defaults(func=template_apply)

    # triggers
    subparser = _sub.add_parser("trigger", help="Trigger commands")
    _sub_switch = subparser.add_subparsers()

    # list triggers
    subparser = _sub_switch.add_parser("list", help="List all available triggers")
    subparser.set_defaults(func=list_triggers)

    # activate triggers
    subparser = _sub_switch.add_parser("activate", help="Activate a trigger")
    subparser.add_argument("ain", type=str, metavar="AIN", help="Actor Identification")
    subparser.set_defaults(func=trigger_set_active)

    # deactivate triggers
    subparser = _sub_switch.add_parser("deactivate", help="Deactivate a trigger")
    subparser.add_argument("ain", type=str, metavar="AIN", help="Actor Identification")
    subparser.set_defaults(func=trigger_set_inactive)

    parsed_args = parser.parse_args(args)

    logging.basicConfig()
    if parsed_args.verbose:
        logging.getLogger("pyfritzhome").setLevel(logging.DEBUG)

    fritzbox = None
    try:
        fritzbox = Fritzhome(
            host=parsed_args.host,
            user=parsed_args.user,
            password=parsed_args.password,
            port=parsed_args.port or None,
            ssl_verify=not parsed_args.insecure,
        )
        fritzbox.login()
        parsed_args.func(fritzbox, parsed_args)
    finally:
        if fritzbox is not None:
            fritzbox.logout()


if __name__ == "__main__":
    main()
