from urllib import parse
import urllib.request as request

ACTION_URL = 'http://marantz/MainZone/index.put.asp'
STATUS_URL = 'http://marantz/goform/formMainZone_MainZoneXml.xml'


def get(zone):
    data = parse.urlencode({
        'ZoneName': zone.zone_name
    })
    print('getting data {}'.format(data))
    return request.urlopen(STATUS_URL, data.encode('ascii')).read()


def post(arguments):
    data = parse.urlencode(arguments)
    print('posting data {}'.format(data))
    request.urlopen(ACTION_URL, data.encode('ascii'))


def send_command(zone, command, argument):
    cmd0 = '%s/%s' % (command, argument)
    post({
        'cmd0': cmd0,
        'ZoneName': zone.zone_name
    })
