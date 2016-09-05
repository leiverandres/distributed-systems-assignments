from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
from twisted.python import log
from twisted.internet import reactor
import json
import time
import os
# import sys

clients = []
times = {}
loc_time = 0

class Server(WebSocketServerProtocol):
    def onConnect(self, request):
        global clients
        print 'Client connecting: {0}'.format(request.peer)
        clients.append(self)

    def getTime(self):
        msg = json.dumps({
            'type': 'time',
            'time': loc_time
        })
        for cl in clients:
            cl.sendMessage(msg)

    def adjustTime(self):
        global loc_time
        if len(times) > 0:
            avg = sum(times.values()) / (len(times) + 1)
            loc_time += avg
            for cl, t in zip(clients, times.values()):
                msg = json.dumps({
                    'type': 'update',
                    'dt': avg - t
                })
                cl.sendMessage(msg)

    def onOpen(self):
        print('WebSocket connection open.')
        def loop():
            self.factory.reactor.callLater(0.01, self.getTime)
            self.factory.reactor.callLater(0.02, self.adjustTime)
        loop()

    def onMessage(self, payload, isBinary):
        # print loc_time,
        # if isBinary:
        #     print 'Binary message received: {0} bytes'.format(len(payload))
        # else:
        #     print 'Text message received: {0}'.format(payload.decode('utf8'))
        data = json.loads(payload)
        if data['type'] == 'hi':
            _id = len(clients)
            msg = json.dumps({
                'type': 'id',
                'id': _id
            })
            self.sendMessage(msg)
        elif data['type'] == 'time':
            times[data['id']] = data['time']

    def onClose(self, wasClean, code, reason):
        print 'WebSocket connection closed: {0}'.format(reason)
        clients.remove(self)

def set_time():
    global loc_time
    loc_time = float(time.time())
    server_order = ''

def sim_time():
    set_time()
    def run():
        global loc_time, server_order
        loc_time += 0.1
        os.system('cls' if os.name == 'nt' else 'clear')
        print 'Unix time', loc_time
        reactor.callLater(0.1, run)
    run()

def main():
    # log.startLogging(sys.stdout)
    sim_time()
    factory = WebSocketServerFactory(u'ws://127.0.0.1:9000')
    factory.protocol = Server
    reactor.listenTCP(9000, factory)
    reactor.run()

if __name__ == '__main__':
    main()
