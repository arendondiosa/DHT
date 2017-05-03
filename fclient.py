#!/usr/bin/python
import base64
import hashlib
import json
import os
import random
import string
import sys
import time

import zmq
from termcolor import colored

import ffile


def toHex(data):
    return base64.b16encode(data)


def hexToDec(data):
    return base64.b16decode(data)


def client_data(data):
    for i in data:
        print colored(i, 'magenta')


def client_info(client):
    print colored('#############', 'magenta')
    print colored('My IP -->' + client['ip'] + ':' + client['port'], 'magenta')
    print colored('FILES:', 'magenta')
    client_data(client['data'])
    print colored('#############', 'magenta')


def options():
    print colored('Options', 'blue', attrs=['bold'])
    print colored('    exit   ->    Close client connection', 'blue')
    print colored('-h, help   ->    Get help', 'blue')
    print colored('ls         ->    List of my files in DHT', 'blue')
    print colored('-s or send <filename.ext>   ->    Send a file', 'blue')


def list_file(client):
    for i in client['data']:
        print colored(
            client['data'][i]['name'], 'magenta',
            attrs=['bold']) + ':' + colored(i, 'magenta')


def printJSON(varJSON):
    print colored(
        json.dumps(varJSON, indent=2, sort_keys=True), 'cyan', attrs=['bold'])


def clear():
    sys.stderr.write("\x1b[2J\x1b[H")


def send_msg(client, to, inp):
    data = ffile.get_file(inp[1])

    if data:
        file_info = json.dumps({
            'req': 'save',
            'from': client['ip'] + ':' + client['port'],
            'to': to,
            'data': data,
            'name': ffile.get_filename(inp[1]),
            'id': ffile.sha256(ffile.get_file(inp[1]))
        })
        file_info_json = json.loads(file_info)

        client['data'][ffile.sha256(ffile.get_file(inp[1]))] = {
            'name': ffile.get_filename(inp[1]),
            'data': data
        }

        client_info(client)

        printJSON(file_info_json)
        return file_info_json
    else:
        return 'Err: No file'


def send(req, socket):
    socket.connect('tcp://' + req['to'])
    print colored(
        'connection to ' + 'tcp://' + req['to'], 'yellow', attrs=['bold'])
    socket.send(json.dumps(req))
    message = socket.recv()
    print colored(message, 'green')
