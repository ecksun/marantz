from collections import namedtuple
from unittest import TestCase

from zone import Zones, ZoneHandler

ConfigMock = namedtuple('Config', ['room'])


class TestZoneHandler(TestCase):
    def test_configured_rooms_with_room(self):
        config = {
            'ROOMS': {
                'livingroom': 'MainZone',
                'kitchen': 'Zone2'
            }
        }

        args = ConfigMock(room=True)

        zone_handler = ZoneHandler(config)

        zones = zone_handler.get_actionable_zones(Zones.All, args)

        self.assertCountEqual(zones, [Zones.MainZone, Zones.Zone2])

    def test_configured_rooms_with_zone(self):
        config = {
            'ROOMS': {
                'livingroom': 'MainZone',
                'kitchen': 'Zone2'
            }
        }

        args = ConfigMock(room=None)
        zone_handler = ZoneHandler(config)
        zones = zone_handler.get_actionable_zones(Zones.All, args)

        self.assertCountEqual(zones, [Zones.MainZone, Zones.Zone2, Zones.Zone3])
