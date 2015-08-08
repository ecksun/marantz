import re

from action.SimpleAction import SimpleAction
from marantz import get
from modules.ActionModule import ActionModule
from zone import Zones


def get_status(zone):
    status_xml = get(zone).decode('UTF8')
    return {
        'name': get_property('RenameZone', status_xml).strip(),
        'volume': float(get_property('MasterVolume', status_xml)),
        'mute': get_binary(get_property('Mute', status_xml)),
        'zonepower': get_binary(get_property('ZonePower', status_xml)),
        'power': get_binary(get_property('Power', status_xml))
    }


def get_binary(on_off):
    return True if on_off.lower() == 'on' else False


# We are using regexes because the builtin xml parsers have vulnerabilities and
# should thus not be used for parsing of unauthorized content. We should use
# defusedxml however pypi was down when writing this.
def get_property(name, xml):
    res = re.search('<%s><value>(.*)</value></%s>' % (name, name), xml)
    return res.group(1)


def print_status(args):
    zones = Zones.get_zones(args.zone)
    statuses = list(map(get_status, zones))

    main_power = statuses[0]['power']

    print('{:<16}{}'.format('Power:', 'On' if main_power else 'Off'))
    for status in statuses:
        print('{:<16}{}'.format('Zone:', status['name']))
        print('{:<16}{}'.format('Zone power:', 'On' if status['zonepower'] else 'Off'))
        print('{:<16}{}{}'.format('Volume:', status['volume'], ' (Muted)' if status['mute'] else ''))


class StatusModule(ActionModule):
    def get_actions(self):
        return [SimpleAction('status', print_status)]
