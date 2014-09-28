from action.SimpleAction import SimpleAction
from marantz import send_command
from modules.ActionModule import ActionModule


def power_on():
    send_command('PutZone_OnOff', 'ON')


def power_off():
    send_command('PutZone_OnOff', 'OFF')


class PowerModule(ActionModule):
    def get_actions(self):
        return [
            SimpleAction('on', power_on),
            SimpleAction('off', power_off)
        ]
