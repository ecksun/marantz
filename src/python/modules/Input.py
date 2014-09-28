from action.Action import Action
from marantz import send_command
from modules.ActionModule import ActionModule

INPUT_MAPPING = {
    'saga': 'MPLAY',
    'xbox': 'GAME'
}


def set_input(source_name):
    if source_name not in INPUT_MAPPING:
        print('No such input: ' + source_name)
        return
    send_command('PutZone_InputFunction', INPUT_MAPPING[source_name])


class Input(Action):
    def add_parser(self, subparsers):
        inputparser = subparsers.add_parser('input')
        inputparser.add_argument('input', choices=INPUT_MAPPING.keys())
        inputparser.set_defaults(func=lambda args: set_input(args.input))


class InputModule(ActionModule):
    def get_actions(self):
        return [Input()]

