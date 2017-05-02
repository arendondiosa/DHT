#!/usr/bin/python
import base64
import hashlib
import json
import os
import random
import string
import sys
import time

from termcolor import colored

import zmq


def toHex(data):
    return base64.b16encode(data)


def hexToDec(data):
    return base64.b16decode(data)


def client_info(client):
    print colored('#############', 'magenta')
    print colored('My IP -->' + client['ip'] + ':' + client['port'], 'magenta')
    print colored('FILES:', 'magenta')
    print colored(client['data'], 'magenta')
    print colored('#############', 'magenta')


def options():
    print colored('Options', 'blue', attrs=['bold'])
    print colored('    exit   ->    Close client connection', 'blue')
    print colored('-h, help   ->    Get help', 'blue')
    print colored('-s or send <filename.ext>   ->    Get help', 'blue')


def get_file(path):
    data = open(path, 'r').read()
    return toHex(data)


def get_filename(path):
    return os.path.basename(path)


def printJSON(varJSON):
    print json.dumps(varJSON, indent=2, sort_keys=True)


def clear():
    sys.stderr.write("\x1b[2J\x1b[H")
