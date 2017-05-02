#!/usr/bin/python

import hashlib
import json
import random
import string
import sys
import time

import numpy
import zmq
from termcolor import colored

import ffile
import fclient

#client data
client = json.dumps({'ip': '', 'port': '', 'data': []})
client = json.loads(client)

context = zmq.Context()
socket = context.socket(zmq.REP)
socket_send = context.socket(zmq.REQ)


def get_id(my_ip):
    client['ip'], client['port'] = my_ip.split(':')


def main():
    global client
    my_ip = some_ip = ''

    if len(sys.argv) == 3:
        some_ip = sys.argv[2]
    elif len(sys.argv) == 2:
        print 'Number 1'
    else:
        print 'No argv'

    if len(sys.argv) >= 2:
        my_ip = sys.argv[1]
        get_id(my_ip)  # Arguments to variables python

        fclient.client_info(client)
        fclient.clear()
        print colored(
            'Welcome to CHORD simulation', 'yellow',
            attrs=['bold']), colored('Terminal', 'yellow')
        while True:
            print colored(
                '(Type help or -h for more information)',
                'yellow',
                attrs=['reverse'])
            inp = raw_input(colored('$ >> ', 'cyan'))
            inp = inp.split()

            if inp[0] == 'help' or inp[0] == '-h':
                fclient.options()
            elif inp[0] == 'send' or inp[0] == '-s':
                file_info = json.dumps({
                    'req': 'save',
                    'from': my_ip,
                    'to': some_ip,
                    'data': fclient.get_file(inp[1]),
                    'name': fclient.get_filename(inp[1])
                })
                file_info_json = json.loads(file_info)
                fclient.printJSON(file_info_json)

                # TO DO: SAVE REQ IN NODE

            elif inp[0] == 'exit':
                print colored('See you later', 'yellow')
                break
            else:
                print colored('Type a correct option', 'red')
            print ''


if __name__ == '__main__':
    main()
