from action.Action import Action
from action.SimpleAction import SimpleAction
from marantz import send_command
from modules.ActionModule import ActionModule


def increasevolume():
    send_command('putmastervolumebtn', '>')


def decreasevolume():
    send_command('putmastervolumebtn', '<')


def set_volume(volume):
    vol = '%.1f' % (volume)
    send_command('PutMasterVolumeSet', vol)


def mute(state):
    send_command('PutVolumeMute', state)


class VolumeAction(Action):
    def add_parser(self, subparsers):
        volparser = subparsers.add_parser('volume', aliases=['vol'])
        volparser.add_argument('volume', type=float)
        volparser.set_defaults(func=lambda args: set_volume(args.volume))


class MuteAction(Action):
    def add_parser(self, subparsers):
        inputparser = subparsers.add_parser('mute')
        inputparser.add_argument('state', choices=['on', 'off'])
        inputparser.set_defaults(func=lambda args: mute(args.state))


class VolumeModule(ActionModule):
    def get_actions(self):
        return [
            SimpleAction('inc', increasevolume),
            SimpleAction('dec', decreasevolume),
            VolumeAction()
        ]
