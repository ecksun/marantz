import argparse
from enum import Enum


class Zones(Enum):
    MainZone = 'MainZone',
    Zone2 = 'Zone2',
    Zone3 = 'Zone3'

    def __str__(self):
        return self.name


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
