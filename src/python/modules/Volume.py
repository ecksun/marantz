from enum import Enum
import math
from action.Action import Action
from action.SimpleAction import SimpleAction
from marantz import send_command
from modules.ActionModule import ActionModule
from modules.Status import get_status
from zone import Zones


class IncDec(Enum):
    INC = '>'
    DEC = '<'


def incdec(zones, direction: IncDec):
    for zone in zones:
        send_command(zone, 'PutMasterVolumeBtn', direction.value)


def set_volume(zone, volume):
    vol = '%.1f' % volume
    send_command(zone, 'PutMasterVolumeSet', vol)


def change_volume(zone, volume_change):
    volume = get_status(zone)['volume']

    vol_current = volume
    target_delta = abs(volume_change)
    while target_delta > 0:
        current_change = min(1, target_delta)
        target_delta -= current_change
        vol_current += math.copysign(current_change, volume_change)
        set_volume(zone, vol_current)


def handle_volume(args):
    for zone in Zones.get_zones(args.zone):
        if args.set:
            set_volume(zone, args.volume)
        else:
            change_volume(zone, args.volume)


def mute_state(zone, given_state):
    def mute(state):
        send_command(zone, 'PutVolumeMute', state)

    if given_state == 'on' or given_state == 'off':
        mute(given_state)
    else:
        is_mute = get_status(zone)['mute']
        mute('off' if is_mute else 'on')


class VolumeAction(Action):
    def add_parser(self, subparsers):
        volparser = subparsers.add_parser('volume', aliases=['vol'])
        volparser.add_argument('volume', type=float)
        volparser.add_argument('--set', action='store_true')
        volparser.set_defaults(func=handle_volume)


class MuteAction(Action):
    def add_parser(self, subparsers):
        def _mute_zones(args):
            for zone in Zones.get_zones(args.zone):
                mute_state(zone, args.state)

        inputparser = subparsers.add_parser('mute')
        inputparser.add_argument('state',
                                 choices=['on', 'off', 'toggle'],
                                 default='toggle',
                                 nargs='?')
        inputparser.set_defaults(func=_mute_zones)


class VolumeModule(ActionModule):
    def get_actions(self):
        return [
            SimpleAction('inc', lambda args: incdec(Zones.get_zones(args.zone), IncDec.INC)),
            SimpleAction('dec', lambda args: incdec(Zones.get_zones(args.zone), IncDec.DEC)),
            VolumeAction(),
            MuteAction()
        ]
