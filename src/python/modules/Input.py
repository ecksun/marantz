from action.Action import Action
from marantz import send_command
from modules.ActionModule import ActionModule


class Input(Action):
    def __init__(self, zone_lookup, input_names):
        self.input_names = input_names
        self.zone_lookup = zone_lookup

    def _set_input(self, zones, source_name):
        if source_name not in self.input_names:
            print('No such input: ' + source_name)
            return
        for zone in zones:
            send_command(zone, 'PutZone_InputFunction', self.input_names[source_name])

    def add_parser(self, subparsers):
        inputparser = subparsers.add_parser('input')
        inputparser.add_argument('input', choices=self.input_names.keys())
        inputparser.set_defaults(func=lambda args: self._set_input(self.zone_lookup(args.zone), args.input))


class InputModule(ActionModule):
    input_names = {}

    def __init__(self, zone_handler, config):
        self.zone_handler = zone_handler
        if 'INPUTS' in config:
            self.input_names = config['INPUTS']

    def get_actions(self):
        return [Input(self.zone_handler.get_configured_rooms, self.input_names)]
