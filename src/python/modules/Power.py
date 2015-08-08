from enum import Enum
import time

from action.SimpleAction import SimpleAction
from marantz import send_command
from modules.ActionModule import ActionModule
from modules.Status import get_status
from zone import Zones


class Power(Enum):
    ON = 'ON'
    OFF = 'OFF'


def power(given_zone, state: Power):
    for zone in Zones.get_zones(given_zone):
        send_command(zone, 'PutZone_OnOff', state.value)
        while state is Power.ON and get_status(zone)['zonepower'] is False:
            time.sleep(0.5)
            send_command(zone, 'PutZone_OnOff', state.value)


class PowerModule(ActionModule):
    def get_actions(self):
        return [
            SimpleAction('on', lambda args: power(args.zone, Power.ON)),
            SimpleAction('off', lambda args: power(args.zone, Power.OFF))
        ]
