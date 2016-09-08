import socket
import sys
import time

if __name__ == '__main__':
	host, port = 'localhost', 5000

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print "Connecting to {0}:{1}".format(host, port)
	try:
		sock.connect((host, port))
	except socket.error as e:
		print(str(e))
	try:
		while True:
			data  = sock.recv(1000).split(' ')
			print "Getting time from server: {0}".format(data)
			if data[0] == 'get':
				offset = time.time() - float(data[1])
				print "local time: {0}".format(offset)
				sock.sendall(str(offset))
				print "Sending time to server"
			elif data[0] == 'post':
				local_time = float(data[1])
				print "new time: {0}".format(local_time)
			elif data[0] == '':
				break
	except socket.error as e:
		print(str(e))
	finally:
		print "closing connection"
		sock.close()
