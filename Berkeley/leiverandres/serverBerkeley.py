import socket
import sys
import datetime

if __name__ == '__main__':
	host, port = 'localhost', 5050

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sock.bind((host, port))
	except socket.error as e:
	    print(str(e))
		sys.exit()

	sock.listen(10)
	print "Waiting for connection at {0}:{1}".format(host, port)
	while True:
		connection, client_addr = sock.accept()
		try:
			print "connection from {0}".format(client_addr)
			while True:
				data = connection.recv(1000)
				if data:
					print "Getting data: {0}".format(data)
					print "Enviando data to client"
					res = datetime.datetime.now().time()
					connection.sendall(str(res))
				else:
					print "No data recived"
					break
		except socket.error as e:
		    print str(e)
		finally:
			connection.close()
