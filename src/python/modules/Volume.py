import math
from action.Action import Action
from action.SimpleAction import SimpleAction
from marantz import send_command
from modules.ActionModule import ActionModule
from modules.Status import get_status


def increasevolume(args):
    send_command(args.zone, 'putmastervolumebtn', '>')


def decreasevolume(args):
    send_command(args.zone, 'putmastervolumebtn', '<')


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
    if args.set:
        set_volume(args.zone, args.volume)
    else:
        change_volume(args.zone, args.volume)


def mute(zone, state):
    send_command(zone, 'PutVolumeMute', state)


def mute_state(zone, state):
    if state == 'on' or state == 'off':
        mute(zone, state)
    else:
        is_mute = get_status(zone)['mute']
        mute(zone, 'off' if is_mute else 'on')


class VolumeAction(Action):
    def add_parser(self, subparsers):
        volparser = subparsers.add_parser('volume', aliases=['vol'])
        volparser.add_argument('volume', type=float)
        volparser.add_argument('--set', action='store_true')
        volparser.set_defaults(func=handle_volume)


class MuteAction(Action):
    def add_parser(self, subparsers):
        inputparser = subparsers.add_parser('mute')
        inputparser.add_argument('state',
                                 choices=['on', 'off', 'toggle'],
                                 default='toggle',
                                 nargs='?')
        inputparser.set_defaults(func=lambda args: mute_state(args.zone, args.state))


class VolumeModule(ActionModule):
    def get_actions(self):
        return [
            SimpleAction('inc', increasevolume),
            SimpleAction('dec', decreasevolume),
            VolumeAction(),
            MuteAction()
        ]
