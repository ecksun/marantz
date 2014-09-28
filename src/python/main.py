#!/usr/bin/env python3
import argparse
import itertools

from modules.Input import InputModule
from modules.Power import PowerModule
from modules.Status import StatusModule
from modules.Volume import VolumeModule


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='action')


modules = [InputModule(), VolumeModule(), PowerModule(), StatusModule()]
module_actions = map(lambda module: module.get_actions(), modules)
actions = itertools.chain(*module_actions)

for action in actions:
    action.add_parser(subparsers)

args = parser.parse_args()

args.func(args)

