#!/usr/bin/python
import hashlib
import json
import random
import string
import sys
import time

import zmq


def sha256(toHash):
    return str(hashlib.sha256(str(toHash)).hexdigest())


# Load JSON from a file
def load_json(path):
    json_data = open(path, 'r')
    d = json.load(json_data)
    return d


def node_listener(port, socket):
    socket.bind('tcp://*:' + port)


# Create a JSON request
def create_req(ip, port, to, req, msg):
    data = json.dumps({
        'from': ip + ':' + port,
        'to': to,
        'req': req,
        'msg': msg
    })
    return data


def check_rank(node, lower, target):
    if target <= node and target > lower:
        return True
    return False
