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


# Load JSON from a file
def load_json(path):
    json_data = open(path, 'r')
    d = json.load(json_data)
    return d


def node_listener(port, socket):
    socket.bind('tcp://*:' + port)


def create_req(ip, port, req, msg):
    data = json.dumps({'ip': ip, 'port': port, 'req': req, 'msg': msg})
    return data
