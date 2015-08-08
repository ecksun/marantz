from action.Action import Action
from marantz import send_command
from modules.ActionModule import ActionModule
from zone import Zones


class Input(Action):
    def __init__(self, input_names):
        self.input_names = input_names

    def _set_input(self, zones, source_name):
        if source_name not in self.input_names:
            print('No such input: ' + source_name)
            return
        for zone in zones:
            send_command(zone, 'PutZone_InputFunction', self.input_names[source_name])

    def add_parser(self, subparsers):
        inputparser = subparsers.add_parser('input')
        inputparser.add_argument('input', choices=self.input_names.keys())
        inputparser.set_defaults(func=lambda args: self._set_input(Zones.get_zones(args.zone), args.input))


class InputModule(ActionModule):
    input_names = {}

    def __init__(self, config):
        if 'INPUTS' in config:
            self.input_names = config['INPUTS']

    def get_actions(self):
        return [Input(self.input_names)]
