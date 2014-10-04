from action.Action import Action
from action.SimpleAction import SimpleAction
from marantz import send_command
from modules.ActionModule import ActionModule
from modules.Status import get_status


def increasevolume():
    send_command('putmastervolumebtn', '>')


def decreasevolume():
    send_command('putmastervolumebtn', '<')


def set_volume(volume):
    vol = '%.1f' % volume
    send_command('PutMasterVolumeSet', vol)


def change_volume(volume_change):
    volume = get_status()['volume']
    set_volume(volume + volume_change)


def handle_volume(args):
    set_volume(args.volume) if args.set else change_volume(args.volume)


def mute(state):
    send_command('PutVolumeMute', state)


def mute_state(state):
    if state == 'on' or state == 'off':
        mute(state)
    else:
        is_mute = get_status()['mute']
        mute('off' if is_mute else 'on')


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
        inputparser.set_defaults(func=lambda args: mute_state(args.state))


class VolumeModule(ActionModule):
    def get_actions(self):
        return [
            SimpleAction('inc', increasevolume),
            SimpleAction('dec', decreasevolume),
            VolumeAction(),
            MuteAction()
        ]
