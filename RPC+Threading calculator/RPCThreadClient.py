# -*- coding: utf-8 -*-
import xmlrpclib
import os
import time
import getpass
import json

ip = '192.168.11.113'
port = '8000'
proxy = xmlrpclib.ServerProxy('http://{0}:{1}/'.format(ip, port))

def main_menu():
    end = False
    try:
        a = int(raw_input('A: '))
        b = int(raw_input('B: '))
        res = proxy.operate(a, b)
        __res = json.loads(res)
        for key, value in __res.iteritems():
            print "{0} {1} {2} = {3}".format(a, key, b, value)
    except ValueError:
        print 'Invalid data'

if __name__ == '__main__':
    main_menu()
