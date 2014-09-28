#!/usr/bin/env python3

import urllib.request as request
import urllib.parse as parse
import argparse

MARANTZ_URL = 'http://marantz/MainZone/index.put.asp'

INPUT_MAPPING = {
    'saga': 'MPLAY',
    'xbox': 'GAME'
}


def post(arguments):
    data = parse.urlencode(arguments)
    request.urlopen(MARANTZ_URL, data.encode('ascii'))


def sendCommand(command, argument):
    cmd0 = '%s/%s' % (command, argument)
    post({
        'cmd0': cmd0
    })


def increaseVolume():
    sendCommand('PutMasterVolumeBtn', '>')


def decreaseVolume():
    sendCommand('PutMasterVolumeBtn', '<')


def powerOn():
    sendCommand('PutZone_OnOff', 'ON')


def powerOff():
    sendCommand('PutZone_OnOff', 'OFF')


def setVolume(volume):
    vol = '%.1f' % (volume)
    sendCommand('PutMasterVolumeSet', vol)


def setInput(input):
    if input not in INPUT_MAPPING:
        print('No such input: ' + input)
        return
    sendCommand('PutZone_InputFunction', INPUT_MAPPING[input])


def mute(state):
    sendCommand('PutVolumeMute', state)

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='action')


def add_action(name, func):
    parser = subparsers.add_parser(name)
    parser.set_defaults(func=lambda _: func())


add_action('inc', increaseVolume)
add_action('dec', decreaseVolume)
add_action('on', powerOn)
add_action('off', powerOff)


volparser = subparsers.add_parser('volume', aliases=['vol'])
volparser.add_argument('volume', type=float)
volparser.set_defaults(func=lambda args: setVolume(args.volume))

inputparser = subparsers.add_parser('input')
inputparser.add_argument('input', choices=INPUT_MAPPING.keys())
inputparser.set_defaults(func=lambda args: setInput(args.input))

inputparser = subparsers.add_parser('mute')
inputparser.add_argument('state', choices=['on', 'off'])
inputparser.set_defaults(func=lambda args: mute(args.state))

args = parser.parse_args()

args.func(args)

