#!/usr/bin/python
import hashlib
import json
import random
import string
import sys
import time

import zmq


def node_info(node):
    print '#############'
    print 'My IP -->' + node['ip']
    print 'My ID -->' + node['id'][0:7]
    print 'back IP -> ' + node['lower_bound_ip']
    print 'back -> ' + node['lower_bound'][0:7]
    print '#############'


def sha256(toHash):
    return str(hashlib.sha256(str(toHash)).hexdigest())


# Load JSON from a file
def load_json(path):
    json_data = open(path, 'r')
    d = json.load(json_data)
    return d


def printJSON(varJSON):
    print json.dumps(varJSON, indent=2, sort_keys=True)


def node_listener(port, socket):
    socket.bind('tcp://*:' + port)


# Create a JSON request
def create_req(req, who, to, msg):
    data = json.dumps({'req': req, 'from': who, 'to': to, 'msg': msg})
    return data


def check_rank(my_id, lower_id, target):
    if my_id == lower_id:
        return 2
    elif (target <= my_id and target > lower_id):
        return 0
    elif (target > my_id):
        return 1
    elif (target <= lower_id):
        return -1
