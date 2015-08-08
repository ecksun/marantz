from action.SimpleAction import SimpleAction
from marantz import send_command
from modules.ActionModule import ActionModule


def power_on(args):
    send_command(args.zone, command='PutZone_OnOff', argument='ON')


def power_off(args):
    send_command(args.zone, 'PutZone_OnOff', 'OFF')


class PowerModule(ActionModule):
    def get_actions(self):
        return [
            SimpleAction('on', power_on),
            SimpleAction('off', power_off)
        ]
