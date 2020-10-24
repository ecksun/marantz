import time

import zone

from action.Action import Action
from marantz import send_command
from modules.ActionModule import ActionModule
from modules.Status import get_status


class SoundMode(Action):
    def __init__(self):
        self.sound_modes = {
                'movie': 'MOVIE',
                'music': 'MUSIC',
                'game': 'GAME',
                'pure': 'PURE DIRECT',
                'direct': 'DIRECT',
                'stereo': 'STEREO'
        }

    def _set_mode(self, mode):
        if mode not in self.sound_modes:
            print('No such sound mode: ' + mode)
            return
        if mode in ('pure', 'direct', 'stereo'):
            desired = self.sound_modes[mode]
            while True:
                current = get_status(zone.Zones.MainZone)['mode']
                if current == desired:
                    break
                print("The current mode is '%s', changing" % current)
                send_command(zone.Zones.MainZone, 'PutSurroundMode', 'PURE DIRECT')
                time.sleep(2)
        else:
            send_command(zone.Zones.MainZone, 'PutSurroundMode', self.sound_modes[mode])

    def add_parser(self, subparsers):
        modeparser = subparsers.add_parser('mode')
        modeparser.add_argument('mode', choices=self.sound_modes.keys())
        modeparser.set_defaults(func=lambda args: self._set_mode(args.mode))


class SoundModeModule(ActionModule):
    def get_actions(self):
        return [SoundMode()]
