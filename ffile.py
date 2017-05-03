#!/usr/bin/python
import hashlib
import json
import os
import random
import string
import sys
import time

import zmq

import fclient
import fnode


def get_file(path):
    try:
        data = open(path, 'r').read()
    except:
        data = ''
    return fclient.toHex(data)


def get_filename(path):
    return os.path.basename(path)


def sha256(toHash):
    return str(hashlib.sha256(str(toHash)).hexdigest())


def write_file(data):
    file = open('Downloads/' + data['name'], 'wb')
    file.write(fclient.hexToDec(data['data']))
    file.close()
