import argparse
from enum import Enum
import sys


class Zones(Enum):
    All = 'all'
    MainZone = 'MainZone'
    Zone2 = 'Zone2'
    Zone3 = 'Zone3'

    def __str__(self):
        return self.name

    @property
    def zone_name(self):
        if self is Zones.All:
            raise ValueError('All is not a proper zone, this likely means this action is not yet implemented')
        return self.name

    @staticmethod
    def get_zones(zone):
        if zone is Zones.All:
            return [zone for zone in Zones if zone != Zones.All]
        else:
            return [zone]


class ZoneHandler:
    rooms = {
        'all': Zones.All
    }

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

    def get_configured_rooms(self, zone, args):
        if ZoneHandler.configured_rooms_only(args):
            configured_zones = self.rooms.values()
            return [x for x in Zones.get_zones(zone) if x in configured_zones]
        else:
            return Zones.get_zones(zone)

    @staticmethod
    def configured_rooms_only(args):
        return args.room is not None


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
                setattr(namespace, 'room', True)

        def parse_room(room):
            if room in rooms:
                return room
            raise argparse.ArgumentTypeError('Invalid room: %s' % room)

        parser.add_argument('--room',
                            type=parse_room,
                            choices=sorted(rooms.keys()),
                            action=RoomAction,
                            dest='room',
                            help='Specify --zone by name, all will only use zones mentioned in the config file'
                            )
