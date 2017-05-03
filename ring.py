#!/usr/bin/python
import hashlib
import json
import random
import string
import sys
import time

import zmq
from termcolor import colored

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


def save(node, req, socket_send):
    fnode.printJSON(req)
    check = fnode.check_rank(node['id'], node['lower_bound'], req['id'])
    print 'CHECK --> ' + str(check)

    if check == 0:
        fnode.file_to_ring(node, req['name'], req['data'], req['id'])

        fnode.node_info(node)
    elif check == -1:
        req_save = json.dumps({
            'req': 'save',
            'from': node['ip'] + ':' + node['port'],
            'to': node['lower_bound_ip'],
            'data': req['data'],
            'name': req['name'],
            'id': req['id']
        })
        req_save_json = json.loads(req_save)
        socket_send.connect('tcp://' + req_save_json['to'])
        # fnode.printJSON(req_add_json)
        socket_send.send(req_save)
        message = socket_send.recv()
        print message


def remove_file(node, req, socket_send):
    fnode.printJSON(req)
    check = fnode.check_rank(node['id'], node['lower_bound'], req['id'])
    print 'CHECK --> ' + str(check)

    if check == 0:
        fnode.remove_file_ring(node, req['id'])

        fnode.node_info(node)
    elif check == -1:
        req_remove = json.dumps({
            'req': 'remove',
            'from': node['ip'] + ':' + node['port'],
            'to': node['lower_bound_ip'],
            'id': req['id']
        })
        req_remove_json = json.loads(req_remove)
        socket_send.connect('tcp://' + req_remove_json['to'])
        # fnode.printJSON(req_add_json)
        socket_send.send(req_remove)
        message = socket_send.recv()
        print message


def check_file(node, file_id):
    for i in node:
        print i
        if i == file_id:
            return node[i]
            break
    return 'No file'


def get_file(node, req, socket_send):
    fnode.printJSON(req)
    check = check_file(node['file'], req['id'])

    if check != 'No file':
        print colored(check, 'cyan')
        # fnode.node_info(node)
        req_send = json.dumps({
            'from': node['ip'] + ':' + node['port'],
            'to': req['client_origin'],
            'info': check
        })

        req_send_json = json.loads(req_send)
        socket_send.connect('tcp://' + req_send_json['to'])
        socket_send.send(req_send)
        message = socket_send.recv()
        print message

    else:
        print colored('File does not exist in this node :(', 'red')

        if req['node_origin'] == node['lower_bound_ip']:
            req_send = json.dumps({
                'from': node['ip'] + ':' + node['port'],
                'to': req['client_origin'],
                'info': 'No'
            })

            req_send_json = json.loads(req_send)
            socket_send.connect('tcp://' + req_send_json['to'])
            socket_send.send(req_send)
            message = socket_send.recv()
            print message

        else:
            get_req = json.dumps({
                'req': 'get',
                'from': req['from'],
                'to': node['lower_bound_ip'],
                'id': req['id'],
                'node_origin': req['node_origin'],
                'client_origin': req['client_origin']
            })
            get_req_json = json.loads(get_req)

            socket_send.connect('tcp://' + get_req_json['to'])
            socket_send.send(get_req)
            message = socket_send.recv()
            print colored(message, 'green')
