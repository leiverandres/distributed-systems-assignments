from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory
from twisted.python import log
from twisted.internet import reactor
import os
import time
import json
# import sys

client_id = 0
loc_time = 0
time_before = 0
server_order = ''

class Client(WebSocketClientProtocol):
    def onConnect(self, response):
        print 'Server connected: {0}'.format(response.peer)
        msg = json.dumps({ 'type': 'hi' })
        self.sendMessage(msg)

    def onOpen(self):
        print('WebSocket connection open.')

    def onMessage(self, payload, isBinary):
        global client_id, loc_time, server_order, time_before
        # print loc_time,
        # if isBinary:
        #     print 'Binary message received: {0} bytes'.format(len(payload))
        # else:
        #     print 'Text message received: {0}'.format(payload.decode('utf8'))
        data = json.loads(payload)
        if data['type'] == 'time':
            msg = json.dumps({
                'type': 'time',
                'id': client_id,
                'time': loc_time - data['time']
            })
            self.sendMessage(msg)
        elif data['type'] == 'id':
            client_id = int(data['id'])
        elif data['type'] == 'update':
            time_before = loc_time
            loc_time += data['dt']
            server_order = str(data['dt'])

    def onClose(self, wasClean, code, reason):
        print 'WebSocket connection closed: {0}'.format(reason)

def set_time():
    global loc_time, server_order
    loc_time = float(time.time() + 10.00)
    server_order = ''
    time_before = 0

def sim_time():
    set_time()
    def run():
        global loc_time, server_order, time_before
        loc_time += 0.1
        os.system('cls' if os.name == 'nt' else 'clear')
        print 'Unix time', loc_time, '\n'
        if server_order != '':
            print 'Server order:', server_order
        if time_before > 0:
            time_before += 0.1
            print 'Time before:', time_before
        reactor.callLater(0.1, run)
    run()

def main():
    # log.startLogging(sys.stdout)
    sim_time()
    factory = WebSocketClientFactory(u'ws://127.0.0.1:9000')
    factory.protocol = Client
    reactor.connectTCP('127.0.0.1', 9000, factory)
    reactor.run()

if __name__ == '__main__':
    main()
