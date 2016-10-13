# -*- coding: utf-8 -*-
from SimpleXMLRPCServer import SimpleXMLRPCServer


class Operations:
    def sum(self, l, r):
        suma = 0
        for i in xrange(l, r):
            suma += i
        return suma


def main():
    ip = '192.168.11.113'
    port = 8000
    server = SimpleXMLRPCServer((ip, port))
    server.register_introspection_functions()

    server.register_instance(Operations())

    print 'Listening on port {}'.format(port)
    server.serve_forever()

if __name__ == '__main__':
    main()
