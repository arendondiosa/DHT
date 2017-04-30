#!/usr/bin/python
import hashlib
import json
import random
import string
import sys
import time

import zmq


def node_info(node_id, lower_bound_ip, upper_bound_ip, lower_bound,
              upper_bound):
    print '#############'
    print 'My ID -->' + node_id[0:7]
    print 'back and front IPs -> ' + lower_bound_ip + '  ' + upper_bound_ip
    print 'back and front -> ' + lower_bound[0:7] + '  ' + upper_bound[0:7]
    print '#############'


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
def create_req(req, who, to, msg):
    data = json.dumps({'req': req, 'from': who, 'to': to, 'msg': msg})
    return data


def check_rank(node, lower, target):
    if (target <= node and target > lower) or node == lower:
        return 0
    elif target > node:
        return 1
    else:
        return -1
