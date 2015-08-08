from enum import Enum
import math

from action.Action import Action
from action.SimpleAction import SimpleAction
from marantz import send_command
from modules.ActionModule import ActionModule
from modules.Status import get_status


class IncDec(Enum):
    INC = '>'
    DEC = '<'


def incdec(zones, direction: IncDec):
    for zone in zones:
        send_command(zone, 'PutMasterVolumeBtn', direction.value)


def set_zone_volume(zone, volume):
    vol = '%.1f' % volume
    send_command(zone, 'PutMasterVolumeSet', vol)


def change_zone_volume(zone, volume_change):
    volume = get_status(zone)['volume']

    vol_current = volume
    target_delta = abs(volume_change)
    while target_delta > 0:
        current_change = min(1, target_delta)
        target_delta -= current_change
        vol_current += math.copysign(current_change, volume_change)
        set_volume(zone, vol_current)


def set_volume(zones, volume):
    for zone in zones:
        set_zone_volume(zone, volume)


def change_volume(zones, volume):
    for zone in zones:
        change_zone_volume(zone, volume)


def mute_state(zone, given_state):
    def mute(state):
        send_command(zone, 'PutVolumeMute', state)

    if given_state == 'on' or given_state == 'off':
        mute(given_state)
    else:
        is_mute = get_status(zone)['mute']
        mute('off' if is_mute else 'on')


class VolumeAction(Action):
    def __init__(self, get_zones):
        self.get_zones = get_zones

    def add_parser(self, subparsers):
        def _volume_action(args):
            zones = self.get_zones(args)
            if args.set:
                set_volume(zones, args.volume)
            else:
                change_volume(zones, args.volume)

        volparser = subparsers.add_parser('volume', aliases=['vol'])
        volparser.add_argument('volume', type=float)
        volparser.add_argument('--set', action='store_true')
        volparser.set_defaults(func=_volume_action)


class MuteAction(Action):
    def __init__(self, get_zones):
        self.get_zones = get_zones

    def add_parser(self, subparsers):
        def _mute_zones(args):
            for zone in self.get_zones(args):
                mute_state(zone, args.state)

        inputparser = subparsers.add_parser('mute')
        inputparser.add_argument('state',
                                 choices=['on', 'off', 'toggle'],
                                 default='toggle',
                                 nargs='?')
        inputparser.set_defaults(func=_mute_zones)


class VolumeModule(ActionModule):
    def __init__(self, zone_handler):
        self.get_zones = zone_handler.get_actionable_zones

    def get_actions(self):
        return [
            SimpleAction('inc', lambda args: incdec(self.get_zones(args), IncDec.INC)),
            SimpleAction('dec', lambda args: incdec(self.get_zones(args), IncDec.DEC)),
            VolumeAction(self.get_zones),
            MuteAction(self.get_zones)
        ]
