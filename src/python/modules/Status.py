import pprint
import re
from action.SimpleAction import SimpleAction
from marantz import get
from modules.ActionModule import ActionModule


def get_status():
    statusXml = get().decode('UTF8')
    return {
        'volume': float(get_property('MasterVolume', statusXml)),
        'mute': get_binary(get_property('Mute', statusXml)),
        'power': get_binary(get_property('Power', statusXml))
    }


def get_binary(on_off):
    return True if on_off.lower() == 'on' else False


# We are using regexes because the builtin xml parsers have vulnerabilities and
# should thus not be used for parsing of unauthorized content. We should use
# defusedxml however pypi was down when writing this.
def get_property(name, xml):
    res = re.search('<%s><value>(.*)</value></%s>' % (name, name), xml)
    return res.group(1)


def print_status():
    pprint.pprint(get_status())


class StatusModule(ActionModule):
    def get_actions(self):
        return [SimpleAction('status', print_status)]
