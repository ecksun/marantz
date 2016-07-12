from enum import Enum
import time

from action.SimpleAction import SimpleAction
from marantz import send_command
from modules.ActionModule import ActionModule
from modules.Status import get_status


class Power(Enum):
    ON = 'ON'
    OFF = 'OFF'


def power(zones, state: Power):
    for zone in zones:
        send_command(zone, 'PutZone_OnOff', state.value)
        while state is Power.ON and get_status(zone)['zonepower'] is False:
            time.sleep(0.5)
            send_command(zone, 'PutZone_OnOff', state.value)


class PowerModule(ActionModule):
    def __init__(self, zone_handler):
        self.get_zones = zone_handler.get_actionable_zones

    def get_actions(self):
        return [
            SimpleAction('on', lambda args: power(self.get_zones(args), Power.ON)),
            SimpleAction('off', lambda args: power(self.get_zones(args), Power.OFF))
        ]
