import pprint
import re

from action.SimpleAction import SimpleAction
from marantz import get
from modules.ActionModule import ActionModule


def get_status(zone):
    status_xml = get(zone).decode('UTF8')
    return {
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
    pprint.pprint(get_status(args.zone))


class StatusModule(ActionModule):
    def get_actions(self):
        return [SimpleAction('status', print_status)]
