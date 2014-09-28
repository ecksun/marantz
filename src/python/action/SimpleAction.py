from action.Action import Action


class SimpleAction(Action):
    def __init__(self, name, action):
        self.name = name
        self.action = action

    def add_parser(self, subparsers):
        parser = subparsers.add_parser(self.name)
        parser.set_defaults(func=lambda _: self.action())
