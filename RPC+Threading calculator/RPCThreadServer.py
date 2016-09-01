# -*- coding: utf-8 -*-
from SimpleXMLRPCServer import SimpleXMLRPCServer
from threading import Thread
import time
import json

res = {}
def add(x, y):
    return x + y
def sub(x, y):
    return x - y
def mul(x, y):
    return x * y
def div(x, y):
    return x / y

class ThreadOperation(Thread):
    def __init__(self, x, y, op, op_sym):
        super(ThreadOperation, self).__init__()
        self.x = x
        self.y = y
        self.op = op
        self.op_sym = op_sym

    def run(self):
        global res
        res[self.op_sym] = self.op(self.x, self.y)

def operate(x, y):
    ops = [add, sub, mul, div]
    ops_sym = ['+', '-', '*', '/']
    threads = [ThreadOperation(x, y, op, op_sym) for op, op_sym in zip(ops, ops_sym)]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    return json.dumps(res)

def main():
    ip = '192.168.11.113'
    port = 8000
    server = SimpleXMLRPCServer((ip, port))
    server.register_introspection_functions()
    server.register_function(operate)

    print "Salut les amis, je suis le serveur et je vous écoute dans le port %d..." % port
    server.serve_forever()

if __name__ == '__main__':
    res = {}
    main()
