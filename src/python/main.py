#!/usr/bin/env python3
import argparse
from configparser import ConfigParser
import itertools

import os
from modules.Input import InputModule
from modules.Power import PowerModule
from modules.Status import StatusModule
from modules.Volume import VolumeModule
from zone import ZoneHandler

config = ConfigParser()
config.read(os.path.expanduser('~/.marantzrc'))

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='action')

zone_handler = ZoneHandler(config)
zone_handler.add_arguments(parser)

modules = [
    InputModule(zone_handler, config),
    VolumeModule(zone_handler),
    PowerModule(zone_handler),
    StatusModule(zone_handler)
]
module_actions = map(lambda module: module.get_actions(), modules)
actions = itertools.chain(*module_actions)

for action in actions:
    action.add_parser(subparsers)

args = parser.parse_args()

args.func(args)
