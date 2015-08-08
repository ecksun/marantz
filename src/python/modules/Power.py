from enum import Enum
from action.SimpleAction import SimpleAction
from marantz import send_command
from modules.ActionModule import ActionModule
from zone import Zones


class Power(Enum):
    ON = 'ON'
    OFF = 'OFF'


def power(given_zone, state: Power):
    for zone in Zones.get_zones(given_zone):
        send_command(zone, 'PutZone_OnOff', state.value)


class PowerModule(ActionModule):
    def get_actions(self):
        return [
            SimpleAction('on', lambda args: power(args.zone, Power.ON)),
            SimpleAction('off', lambda args: power(args.zone, Power.OFF))
        ]
