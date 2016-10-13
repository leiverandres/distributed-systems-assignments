# -*- coding: utf-8 -*-
from SimpleXMLRPCServer import SimpleXMLRPCServer
import threading
import random
import string

sums = {}

def token_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class Mult(threading.Thread):
    def __init__(self, A, B, idx):
        super(Mult, self).__init__()
        self.A = A
        self.B = B
        self.idx = idx

    def run(self):
        global sums
        suma = 0
        for a, b  in zip(self.A, self.B):
            suma += a * b
        print self.A, self.B, suma
        sums[self.idx] = suma

class Operations:
    def mult(self, A, B):
        idx = token_generator()
        t = Mult(A, B, idx)
        t.start()
        t.join()
        return sums[idx]

def main():
    ip = '192.168.11.19'
    port = 8000
    server = SimpleXMLRPCServer((ip, port))
    server.register_introspection_functions()

    server.register_instance(Operations())

    print 'Listening on port {}'.format(port)
    server.serve_forever()

if __name__ == '__main__':
    main()
