#!/usr/bin/python
import zmq
import random
import sys
import time
import hashlib
import json
import string


def sha256(toHash):
    return str(hashlib.sha256(str(toHash)).hexdigest())


def load_json(path):
    json_data = open(path, 'r')
    d = json.load(json_data)
    return d
