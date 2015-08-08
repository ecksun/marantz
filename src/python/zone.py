import argparse
from enum import Enum
import sys


class Zones(Enum):
    MainZone = 'MainZone',
    Zone2 = 'Zone2',
    Zone3 = 'Zone3'

    def __str__(self):
        return self.name


class ZoneHandler:
    rooms = {}

    def __init__(self, config):
        if 'ROOMS' in config:
            rooms = config['ROOMS']
            for key in rooms:
                room = rooms[key]
                try:
                    self.rooms[key] = Zones[room]
                except KeyError:
                    sys.stderr.write('Invalid zone in config file: %s\n' % room)

    def add_arguments(self, parser):
        ZoneParser.add_argument(parser)
        RoomParser.add_argument(self.rooms, parser)


class ZoneParser:
    @staticmethod
    def add_argument(parser):
        def parse_zone(zone):
            try:
                return Zones[zone]
            except KeyError:
                raise argparse.ArgumentTypeError('Invalid zone: %s' % zone)

        parser.add_argument('--zone',
                            type=parse_zone,
                            choices=list(Zones),
                            default=Zones.MainZone,
                            help='The zone to perform the action in'
                            )


class RoomParser:
    @staticmethod
    def add_argument(rooms, parser):
        class RoomAction(argparse.Action):
            def __call__(self, action_parser, namespace, values, option_string=None):
                setattr(namespace, 'zone', rooms[values])

        def parse_room(room):
            if room in rooms:
                return room
            raise argparse.ArgumentTypeError('Invalid room: %s' % room)

        parser.add_argument('--room',
                            type=parse_room,
                            choices=rooms.keys(),
                            action=RoomAction,
                            dest='zone',
                            help='A convenient way of specifying --zone by its name'
                            )
