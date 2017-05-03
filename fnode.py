#!/env/bin/python

import hashlib
import json
import random
import string
import sys
import time

import zmq
from termcolor import colored


def clear():
    sys.stderr.write("\x1b[2J\x1b[H")


def node_data(data):
    for i in data:
        print colored(i, 'magenta')


def node_info(node):
    print colored('#############', 'magenta')
    print colored('My IP -->' + node['ip'] + ':' + node['port'], 'magenta')
    print colored('My ID -->' + node['id'][0:7], 'magenta')
    print colored('back IP -> ' + node['lower_bound_ip'], 'magenta')
    print colored('back -> ' + node['lower_bound'][0:7], 'magenta')
    print colored('FILES: ', 'magenta')
    node_data(node['file'])
    print colored('#############', 'magenta')


def sha256(toHash):
    return str(hashlib.sha256(str(toHash)).hexdigest())


# Load JSON from a file
def load_json(path):
    json_data = open(path, 'r')
    d = json.load(json_data)
    return d


def printJSON(varJSON):
    print json.dumps(varJSON, indent=2, sort_keys=True)


# Create a JSON request
def create_req(req, who, to, msg):
    data = json.dumps({'req': req, 'from': who, 'to': to, 'msg': msg})
    return data


def check_rank(my_id, lower_id, target):
    if lower_id > my_id:
        if target > lower_id or (target >= 0 and target < my_id):
            return 0
        else:
            return -1
    else:
        if (target <= my_id and target > lower_id) or (my_id == lower_id):
            return 0
        else:
            return -1


def file_to_ring(node, filename, binary, fileid):
    node['file'][fileid] = {'name': filename, 'data': binary}


def remove_file_ring(node, fileid):
    del node['file'][fileid]
