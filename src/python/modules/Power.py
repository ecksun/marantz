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
        self.zone_lookup = zone_handler.get_configured_rooms

    def get_actions(self):
        return [
            SimpleAction('on', lambda args: power(self.zone_lookup(args.zone, args), Power.ON)),
            SimpleAction('off', lambda args: power(self.zone_lookup(args.zone, args), Power.OFF))
        ]
