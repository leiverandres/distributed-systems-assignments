import socket
import sys
import datetime

if __name__ == '__main__':
	host, port = 'localhost', 5050

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print "Connecting to {0}:{1}".format(host, port)
	try:
		sock.connect((host, port))
	except socket.error as e:
	    print(str(e))

	try:
		time = datetime.datetime.now().time()
		sock.sendall(str(time))
		print "Sending data to server"
		data  = sock.recv(1000)
		print "Getting data from server: {0}".format(data)
	finally:
		print "closing connection"
		sock.close()
