#!/usr/bin/python

import hashlib
import json
import random
import string
import sys
import time

import numpy
import zmq

import fnode
import ring

#Node data
hash_table = {}

node = json.dumps({
    'ip': '',
    'port': '',
    'id': '',
    'lower_bound': '',
    'lower_bound_ip': '',
})
node = json.loads(node)

context = zmq.Context()
socket = context.socket(zmq.REP)
socket_send = context.socket(zmq.REQ)


# Get a random id. Put in config.json id, port
def get_id(my_ip, socket):
    global node
    rnd = random.randint(0, 2000)
    node['ip'], node['port'] = my_ip.split(':')
    node['id'] = fnode.sha256(rnd)
    socket.bind('tcp://*:' + node['port'])


# Get edges
def get_edges(some_ip):
    global upper_bound, upper_bound_ip, lower_bound, lower_bound_ip
    if some_ip:
        node['lower_bound'] = ''
        node['lower_bound_ip'] = ''
        print 'Other node in the ring'
        req_add = fnode.create_req(
            'add', node['ip'] + ':' + node['port'], some_ip,
            {'origin': node['ip'] + ':' + node['port'],
             'id': node['id']})
        req_add_json = json.loads(req_add)
        socket_send.connect('tcp://' + req_add_json['to'])
        fnode.printJSON(req_add_json)
        socket_send.send(req_add)
        message = socket_send.recv()
        print message
    else:
        node['lower_bound'] = node['id']
        node['lower_bound_ip'] = node['ip'] + ':' + node['port']


def main():
    global node, socket

    fnode.clear()
    print len(sys.argv)
    my_ip = some_ip = ''

    if len(sys.argv) == 3:
        print 'Hay alguien ' + sys.argv[2]
        print my_ip
        some_ip = sys.argv[2]
    elif len(sys.argv) == 2:
        print 'Number 1'
    else:
        print 'No argv'

    if len(sys.argv) >= 2:
        my_ip = sys.argv[1]
        get_id(my_ip, socket)  # Arguments to variables python
        get_edges(some_ip)

        fnode.node_info(node)

        while True:
            #  Wait for next request from client
            print 'Waiting Request...'
            message = socket.recv()
            # print str(message)
            req_json = json.loads(str(message))
            # #  Do some 'work'
            socket.connect('tcp://' + req_json['from'])
            if req_json['req'] == 'add':
                print 'Adding new node'
                socket.send(node['ip'] + ':' + node['port'] + ' --> recv add')
                socket_send = context.socket(zmq.REQ)
                ring.add(node, req_json, socket_send)
            elif req_json['req'] == 'update':
                print 'Updating node information...'
                socket_send = context.socket(zmq.REQ)
                socket.send(node['ip'] + ':' + node['port'] +
                            ' -->  rec to update')
                ring.update(node, req_json)
            else:
                print message


if __name__ == '__main__':
    main()
