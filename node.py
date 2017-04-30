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

#Node data
node_id = ''
hash_table = {}
lower_bound = ''  # predecessor's id
upper_bound = ''  # successor's id
lower_bound_ip = ''  # predecessor's id
upper_bound_ip = ''  # successor's id
ip = ''
port = ''
context = zmq.Context()
socket = context.socket(zmq.REP)
socket_send = context.socket(zmq.REQ)


# Get a random id. Put in config.json id, port
def get_id(my_ip):
    global ip, port, node_id
    rnd = random.randint(0, 100)
    ip, port = my_ip.split(':')
    print ip
    node_id = fnode.sha256(rnd)


# Get next nodes in the ring
def get_edges(some_ip):
    global lower_bound, upper_bound, lower_bound_ip, upper_bound_ip
    if some_ip:
        # print some_ip
        req = fnode.create_req('add', ip + ':' + port, some_ip,
                               {'origin': ip + ':' + port,
                                'id': node_id})
        req_json = json.loads(req)
        print 'Connecting to ' + req_json['to'] + '...'
        socket_send.connect('tcp://' + req_json['to'])
        print("Sending request %s ..." % req)
        # socket_send.send("Hello")
        socket_send.send(req)

        message = socket_send.recv()
        # print message

    else:  # If I'm the first node in the ring
        print 'Soy el unico'
        lower_bound = upper_bound = node_id
        lower_bound_ip = upper_bound_ip = ip + ':' + port


def add(req):
    global node_id, lower_bound_ip, upper_bound_ip, lower_bound, upper_bound
    socket.send('add')
    check = fnode.check_rank(node_id, lower_bound, req['msg']['id'])
    print check
    # Check if a new node is mine
    if check == 0:
        socket_send.connect('tcp://' + req['msg']['origin'])
        res = fnode.create_req('update', ip + ':' + port, req['msg']['origin'],
                               {
                                   'lower_bound': lower_bound,
                                   'lower_bound_ip': lower_bound_ip,
                                   'upper_bound': node_id,
                                   'upper_bound_ip': ip + ':' + port
                               })
        socket_send.send(res)

        if node_id == upper_bound:
            upper_bound = req['msg']['id']
            upper_bound_ip = req['msg']['origin']
        lower_bound = req['msg']['id']
        lower_bound_ip = req['msg']['origin']
        fnode.node_info(node_id, lower_bound_ip, upper_bound_ip, lower_bound,
                        upper_bound)
    elif check == 1:
        req = fnode.create_req('add', ip + ':' + port, some_ip,
                               {'origin': ip + ':' + port,
                                'id': node_id})
        add(req)
    elif check == -1:
        add()


def update(req):
    global lower_bound, upper_bound, lower_bound_ip, upper_bound_ip
    socket.connect('tcp://' + req['from'])
    socket.send('update request receive!')
    # print req
    lower_bound = req['msg']['lower_bound']
    lower_bound_ip = req['msg']['lower_bound_ip']
    upper_bound = req['msg']['upper_bound']
    upper_bound_ip = req['msg']['upper_bound_ip']


def main():
    global ip, port, socket
    print len(sys.argv)
    my_ip = some_ip = ''

    if len(sys.argv) == 3:
        print 'Hay alguien ' + sys.argv[2]
        print my_ip
        some_ip = sys.argv[2]
    elif len(sys.argv) == 2:
        print 'Nadie'
    else:
        print 'Faltan argv'

    if len(sys.argv) >= 2:
        my_ip = sys.argv[1]
        get_id(my_ip)  # Arguments to variables python
        print 'IP ->' + ip + ' , PORT ->' + port
        #
        fnode.node_listener(port, socket)
        get_edges(some_ip)

        fnode.node_info(node_id, lower_bound_ip, upper_bound_ip, lower_bound,
                        upper_bound)

        while True:
            #  Wait for next request from client
            print 'Waiting Request...'
            message = socket.recv()
            req_json = json.loads(str(message))
            print str(message)
            #  Do some 'work'
            if req_json['req'] == 'add':
                print 'Adding new node'
                add(req_json)
            if req_json['req'] == 'update':
                print 'Updating node information...'
                update(req_json)
                fnode.node_info(node_id, lower_bound_ip, upper_bound_ip,
                                lower_bound, upper_bound)
            # else:
            #     socket.send("Waiting...")
            time.sleep(1)

            #  Send reply back to client


if __name__ == '__main__':
    main()
