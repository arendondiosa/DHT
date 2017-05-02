#!/usr/bin/python
import hashlib
import json
import random
import string
import sys
import time

import zmq

import fnode


def add(node, req, socket_send):
    fnode.printJSON(req)
    check = fnode.check_rank(node['id'], node['lower_bound'], req['msg']['id'])
    print 'CHECK --> ' + str(check)

    if check == 0:
        req_update = fnode.create_req(
            'update', node['ip'] + ':' + node['port'], req['msg']['origin'], {
                'lower_bound': node['lower_bound'],
                'lower_bound_ip': node['lower_bound_ip']
            })
        req_update_json = json.loads(req_update)
        print 'Update to ' + 'tcp://' + req_update_json['to']
        time.sleep(5)
        socket_send.connect('tcp://' + req_update_json['to'])
        # fnode.printJSON(req_update_json)
        socket_send.send(req_update)
        message = socket_send.recv()
        print message

        node['lower_bound'] = req['msg']['id']
        node['lower_bound_ip'] = req['msg']['origin']

        fnode.node_info(node)
    elif check == -1:
        req_add = fnode.create_req(
            'add', node['ip'] + ':' + node['port'], node['lower_bound_ip'],
            {'origin': req['msg']['origin'],
             'id': req['msg']['id']})
        req_add_json = json.loads(req_add)
        socket_send.connect('tcp://' + req_add_json['to'])
        # fnode.printJSON(req_add_json)
        socket_send.send(req_add)
        message = socket_send.recv()
        print message


def update(node, req):
    fnode.printJSON(req)
    node['lower_bound'] = req['msg']['lower_bound']
    node['lower_bound_ip'] = req['msg']['lower_bound_ip']

    print '############ UPDATE OK'
    fnode.node_info(node)
