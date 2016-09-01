# -*- coding: utf-8 -*-
import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer
import hashlib
import string
import random
import json

users = {
    # 'leiverandres': 'pass'
}

secret = {
    # 'leiverandres': 'string cifrado'
}

def token_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class DB(object):
    def __init__(self, filename='db.json'):
        super(DB, self).__init__()
        self.filename = filename

    def write(self, data):
        f = open(self.filename, 'w')
        json.dump(data, f)

    def read(self):
        try:
            f = open(self.filename, 'r')
            return json.load(f)
        except IOError:
            self.write({})

# Se definen las funciones que estarán al lado del servidor
class Operations:
    def div(self, data, x, y):
        __data = json.loads(data)
        user = __data['user']
        token = __data['token']
        if user in secret:
            if secret[user] == token:
                if y == 0:
                    return json.dumps({'response': 'fail', 'message': 'Math error'})
                return json.dumps({'response': 'ok', 'result': x / y})
            else:
                return json.dumps({'response': 'fail', 'message': 'Access failed'})
        return json.dumps({'response': 'fail', 'message': 'User does not exists'})

    def add(self, data, x, y):
        __data = json.loads(data)
        user = __data['user']
        token = __data['token']
        if user in secret:
            if secret[user] == token:
                return json.dumps({'response': 'ok', 'result': x + y})
            else:
                return json.dumps({'response': 'fail', 'message': 'Access failed'})
        return json.dumps({'response': 'fail', 'message': 'User does not exists'})

    def sub(self, data, x, y):
        __data = json.loads(data)
        user = __data['user']
        token = __data['token']
        if user in secret:
            if secret[user] == token:
                return json.dumps({'response': 'ok', 'result': x - y})
            else:
                return json.dumps({'response': 'fail', 'message': 'Access failed'})
        return json.dumps({'response': 'fail', 'message': 'User does not exists'})

    def mul(self, data, x, y):
        __data = json.loads(data)
        user = __data['user']
        token = __data['token']
        if user in secret:
            if secret[user] == token:
                return json.dumps({'response': 'ok', 'result': x * y})
            else:
                return json.dumps({'response': 'fail', 'message': 'Access failed'})
        return json.dumps({'response': 'fail', 'message': 'User does not exists'})

    def mod(self, data, x, y):
        __data = json.loads(data)
        user = __data['user']
        token = __data['token']
        if user in secret:
            if secret[user] == token:
                if y == 0:
                    return json.dumps({'response': 'fail', 'message': 'Math error'})
                return json.dumps({'response': 'ok', 'result': x % y})
            else:
                return json.dumps({'response': 'fail', 'message': 'Access failed'})
        return json.dumps({'response': 'fail', 'message': 'User does not exists'})

    def login(self, data):
        __data = json.loads(data)
        user = __data['user']
        password = hashlib.sha224(__data['password']).hexdigest()
        if user in users:
            if users[user] == password:
                secret[user] = token_generator()
                return json.dumps({'response': 'ok', 'message': 'User logged', 'token': secret[user]})
            else:
                return json.dumps({'response': 'fail', 'message': 'Wrong password'})
        return json.dumps({'response': 'fail', 'message': 'User does not exists'})

    def sign_up(self, data):
        global db
        __data = json.loads(data)
        user = __data['user']
        password = __data['password']
        if user not in users:
            users[user] = hashlib.sha224(password).hexdigest()
            db.write(users)
            return json.dumps({'response': 'ok', 'message': 'User created'})
        else:
            return json.dumps({'response': 'fail', 'message': 'User already exists'})

def main():
    global users
    # Se le dice al servidor que acepte peticiones por la ip y puerto especificados.
    port = 8000
    server = SimpleXMLRPCServer(('192.168.0.108', port))
    server.register_introspection_functions()

    # Para permitir llamadas remotas es necesario registrar las funciones
    server.register_instance(Operations())

    db = DB()
    users = db.read()

    print "Hola amigos soy el Servidor y estoy escuchando por el puerto %d..." % port
    server.serve_forever()

if __name__ == '__main__':
    main()
