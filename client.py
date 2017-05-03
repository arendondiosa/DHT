#!/env/bin/python

import hashlib
import json
import random
import string
import sys
import time

import numpy
import zmq
from termcolor import colored

import fclient
import ffile

#client data
client = json.dumps({'ip': '', 'port': '', 'data': {}})
client = json.loads(client)

context = zmq.Context()
socket = context.socket(zmq.REP)
socket_send = context.socket(zmq.REQ)


def get_id(my_ip):
    client['ip'], client['port'] = my_ip.split(':')
    socket.bind('tcp://*:' + client['port'])


def main():
    global client, socket, socket_send
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
            'Welcome to CHORD simulation', 'yellow', attrs=['bold']), colored(
                'Terminal', 'yellow')
        try:
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
                    send_req = fclient.send_msg(client, some_ip, inp)
                    if send_req == 'Err: No file':
                        print colored('Send a correct file', 'red')
                    else:
                        socket_send = context.socket(zmq.REQ)
                        socket_send.connect('tcp://' + send_req['to'])
                        socket_send.send(json.dumps(send_req))
                        message = socket_send.recv()
                        print colored(message, 'green')
                elif inp[0] == 'ls':
                    fclient.list_file(client)
                elif inp[0] == '-rm' or inp[0] == 'remove':
                    remove_req = fclient.remove_msg(client, some_ip, inp)
                    if remove_req == 'Err: No file':
                        print colored('Send a correct file', 'red')
                    else:
                        socket_send = context.socket(zmq.REQ)
                        socket_send.connect('tcp://' + remove_req['to'])
                        socket_send.send(json.dumps(remove_req))
                        message = socket_send.recv()
                        print colored(message, 'green')
                elif inp[0] == '-g' or inp[0] == 'get':
                    get_req = fclient.get_msg(client, some_ip, inp)
                    socket_send = context.socket(zmq.REQ)
                    socket_send.connect('tcp://' + get_req['to'])
                    socket_send.send(json.dumps(get_req))
                    message = socket_send.recv()
                    print colored(message, 'green')

                    message = socket.recv()
                    message = json.loads(message)
                    print message
                    socket.connect('tcp://' + message['from'])
                    socket.send('Thanks <3')

                    if message['info'] == 'No':
                        print colored(
                            'File does not exist in DHT',
                            'red',
                            attrs=['bold'])
                    else:
                        ffile.write_file(message['info'])
                elif inp[0] == 'exit':
                    print colored('See you later', 'yellow')
                    break
                else:
                    print colored('Type a correct option', 'red')
                #
                #     socket_send.connect('tcp://' + inp[0])
                #     print colored(
                #         'connection to ' + 'tcp://' + inp[0],
                #         'yellow',
                #         attrs=['bold'])
                #     socket_send.send(json.dumps({'msg': ':)'}))
                #     message = socket_send.recv()
                #     print colored(message, 'green')
                print ''
        except KeyboardInterrupt:
            print ''
            print colored('See you later', 'yellow')
            exit(0)


if __name__ == '__main__':
    main()
