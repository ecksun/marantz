from urllib import parse
import urllib.request as request

MARANTZ_URL = 'http://marantz/MainZone/index.put.asp'


def post(arguments):
    data = parse.urlencode(arguments)
    request.urlopen(MARANTZ_URL, data.encode('ascii'))


def send_command(command, argument):
    cmd0 = '%s/%s' % (command, argument)
    post({
        'cmd0': cmd0
    })
