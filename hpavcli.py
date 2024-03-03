#!/usr/bin/env python3

import os
import sys
import argparse
import time



from scapy.all import *
from mqtt_client import publish_message

def get_default_interface() -> str:
    return conf.iface.name


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="hpavcli - Powerline (HPAV) management and query utility")
    parser.add_argument('--interface', '-i',
                        type=str,
                        help="Comma separated list of interfaces to search for devices")
    parser.add_argument('--verbose', '-v',
                        action='store_true',
                        help="Verbose mode")
    parser.add_argument('command',
                        choices=['scan', 'networks'],
                        default='scan')
    parser.add_argument("--mqtt_server", help="MQTT server address")
    parser.add_argument("--mqtt_port", type=int, default=1883, help="MQTT server port")
    parser.add_argument("--mqtt_topic", help="MQTT topic to publish the messages")
    parser.add_argument("--mqtt_user", help="MQTT user")
    parser.add_argument("--mqtt_password", help="MQTT password")

    return parser.parse_args()


def main(in_args: argparse.Namespace):
    if in_args.interface:
        interface_list = in_args.interface.split(',')
    else:
        interface_list = [get_default_interface()]

    interfaces = list()
    for iface in interface_list:
        try:
            interfaces.append(PowerlineInterface(ifaces.dev_from_name(iface), verbose=in_args.verbose))
        except (ValueError, PermissionError) as exc:
            print(f"Error creating PowerlineInterface for {iface}: {exc}")

    if not len(interfaces):
        print("No ethernet interfaces could be initialized, exiting.")
        sys.exit(-1)

    if in_args.command == "scan":
        devices = []
        for iface in interfaces:
            devices.extend(iface.discover_devices())

        for device in devices:

            if args.mqtt_server and args.mqtt_topic:
                # Assuming `data` is the information you want to publish
                message = str("data")  # Ensure `data` is in a publishable format
                message = f"[{device.interface.interface_name}] {device.mac.pretty} ({HPAVVersion(device.hpav_version).name} " + f"{OUI(device.oui).name}) STAs:{len(device.sta_list)} NETs:{len(device.net_list)} HFID:'{device.hfid}'"
                publish_message(server=args.mqtt_server, username=args.mqtt_user,password=args.mqtt_password, topic=args.mqtt_topic, message=message)
            else:
            # Existing logic to print `data` to the console

                print(
                    f"[{device.interface.interface_name}] {device.mac.pretty} ({HPAVVersion(device.hpav_version).name} "
                    f"{OUI(device.oui).name}) STAs:{len(device.sta_list)} NETs:{len(device.net_list)} HFID:'{device.hfid}'")
                for net in device.networks():
                    print(f"  {net}")

    elif args.command == "networks":
        for iface in interfaces:
            iface.discover_networks(args)


def run_every_30_seconds(args):
    while True:
        main(args)
        time.sleep(30)


if __name__ == "__main__":
    app_dir = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(app_dir)

    from venvtools import activate
    activate(app_dir)

    from interface import *

    args = parse_args()
    run_every_30_seconds(args)