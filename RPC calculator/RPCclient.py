# -*- coding: utf-8 -*-
import xmlrpclib
import os
import time
import getpass
import json

ip = '192.168.0.108'
port = '8000'
proxy = xmlrpclib.ServerProxy('http://{0}:{1}/'.format(ip, port))

def main_menu(user, token):
    end = False
    while not end:
        os.system('clear')
        print 'RPC CLIENT - Welcome, {0}'.format(user)
        print '1. Addition'
        print '2. Substraction'
        print '3. Multiplication'
        print '4. Division'
        print '0. Exit'

        opc = raw_input('--> ')
        if opc == '1':
            func = proxy.add
            op = '+'
        elif opc == '2':
            func = proxy.sub
            op = '-'
        elif opc == '3':
            func = proxy.mul
            op = '*'
        elif opc == '4':
            func = proxy.div
            op = '/'
        elif opc == '0':
            print 'You have logged out'
            end = True
            time.sleep(1)
            break
        else:
            print 'Invalid option'
            time.sleep(1)
            continue

        try:
            a = int(raw_input('A: '))
            b = int(raw_input('B: '))
            data = json.dumps({'user': user, 'token': token})
            res = json.loads(func(data, a, b))
            if res['response'] == 'ok':
                print a, op, b, '=', res['result']
            else:
                print res['message']
            raw_input('Press ENTER to continue')
        except ValueError:
            print 'Invalid data'
            time.sleep(1)

        time.sleep(1.0 / 30)

def login_menu():
    end = False
    while not end:
        os.system('clear')
        print 'RPC CLIENT'
        print '1. Log in'
        print '2. Sign up'
        print '0. Exit'

        opc = raw_input('--> ')
        if opc == '1':
            user = raw_input('user: ')
            password = str(getpass.getpass('pass: '))
            data = json.dumps({'user': user, 'password': password})
            res = json.loads(proxy.login(data))

            if res['response'] == 'ok':
                main_menu(user, res['token'])
            else:
                print res['message']
                time.sleep(1)
                continue
        elif opc == '2':
            user = raw_input('user: ')
            password = str(getpass.getpass('pass: '))
            data = json.dumps({'user': user, 'password': password})
            res = json.loads(proxy.sign_up(data))
            print res['message']
            time.sleep(1)
            continue
        elif opc == '0':
            print 'Au revoir'
            end = True
            break
        else:
            print 'Invalid option'
            time.sleep(1)
            continue

        time.sleep(1.0 / 30)

if __name__ == '__main__':
    login_menu()
