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
ip = ''
port = ''
context = zmq.Context()
socket = context.socket(zmq.REP)


# Get a random id. Put in config.json id, port
def get_id(my_ip):
    global ip, port, node_id
    rnd = random.randint(0, 100)
    ip, port = my_ip.split(':')
    print ip
    node_id = fnode.sha256(rnd)


# Get next nodes in the ring
def get_edges(some_ip):
    global lower_bound, upper_bound
    if some_ip:
        # print some_ip
        req = fnode.create_req(ip, port, 'add', some_ip)
        req_json = json.loads(req)
        print 'Connecting to ' + req_json['to'] + '...'
        socket_send = context.socket(zmq.REQ)
        socket_send.connect('tcp://' + req_json['to'])
        print("Sending request %s ..." % req)
        # socket_send.send("Hello")
        socket_send.send(req)

        message = socket_send.recv()
        print message

    else:  # If I'm the first node in the ring
        print 'Soy el unico'
        lower_bound = upper_bound = node_id


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
        print 'My ID -->' + node_id[0:7]
        #
        fnode.node_listener(port, socket)
        get_edges(some_ip)
        print 'back and front -> ' + lower_bound[0:7] + '  ' + upper_bound[0:7]

        while True:
            #  Wait for next request from client
            message = socket.recv()
            req_json = json.loads(str(message))
            print str(message)
            #  Do some 'work'
            if req_json['req'] == 'add':
                socket.send('add')
                print fnode.check_rank(
                    node_id,
                    lower_bound, )
            else:
                socket.send("Waiting...")

            time.sleep(1)

            #  Send reply back to client


if __name__ == '__main__':
    main()
