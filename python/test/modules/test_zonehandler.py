from collections import namedtuple
from unittest import TestCase

from zone import ZoneHandler, Zones

ArgsMock = namedtuple('Config', ['room', 'zone'])


class TestZoneHandler(TestCase):
    def test_configured_rooms_with_room(self):
        config = {
            'ROOMS': {
                'livingroom': 'MainZone',
                'kitchen': 'Zone2'
            }
        }

        args = ArgsMock(room=True, zone=Zones.All)

        zone_handler = ZoneHandler(config)

        zones = zone_handler.get_actionable_zones(args)

        self.assertCountEqual(zones, [Zones.MainZone, Zones.Zone2])

    def test_configured_rooms_with_zone(self):
        config = {
            'ROOMS': {
                'livingroom': 'MainZone',
                'kitchen': 'Zone2'
            }
        }

        args = ArgsMock(room=None, zone=Zones.All)
        zone_handler = ZoneHandler(config)
        zones = zone_handler.get_actionable_zones(args)

        self.assertCountEqual(zones, [Zones.MainZone, Zones.Zone2, Zones.Zone3])
