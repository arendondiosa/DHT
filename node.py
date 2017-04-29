#!/usr/bin/python

import random
import sys
import time
import hashlib
import json
import string
import numpy

import fnode

#Node data
node_id = ''
hash_table = {}
lower_bound = ''  # predecessor's id
upper_bound = ''  # successor's id
ip = ''
port = ''


# Get a random id. Put in config.json id, port
def get_id(my_ip, some_ip):
    global ip

    if some_ip:
        print "Hay mas nodos"
    global node_id, ip
    rnd = random.randint(0, 100)
    return fnode.sha256(rnd)

    # f = open('config.json', 'w')
    # f.write(json.dumps(d, sort_keys=True,
    #                    indent=2))  # python will convert \n to os.linesep
    # f.close()


# def get_edges(some_ip):


def main():
    print len(sys.argv)
    my_ip = some_ip = ''

    if len(sys.argv) == 3:
        print 'Hay alguien ' + sys.argv[2]
        ip = sys.argv[1]
        some_ip = sys.argv[2]
    elif len(sys.argv) == 2:
        print 'Nadie'
    else:
        print 'Faltan argv'

    print get_id(my_ip, some_ip)

if __name__ == '__main__':
    main()
