from __future__ import division
import socket
import time
import json

class TimeServer:
	def __init__(self, host, port):
		self.port = port
		self.host = host
		self.master_time = time.time()
		self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		try:
			self.server_sock.bind((host, port))
		except socket.error as e:
		    print(str(e))
		    sys.exit()
		self.server_sock.listen(10)
		self.connection_list = [self.server_sock]
		print "Waiting for connection at {0}:{1}".format(host, port)

	def run(self):
		try:
			while True:
				self.accept_new_connection()
		except socket.error as e:
			print "Error ", e
		finally:
			self.server_sock.close()

	def sync_time(self, _str):
		acum_time = 0
		local_time = time.time()
		for sock in self.connection_list:
			if sock != self.server_sock:
				start = time.time()
				sock.send("get " + str(time.time())) # send current time
				client_offset = float(sock.recv(4094)) # + or -
				end = time.time()
				client_offset += ((end - start) / 2) # + (time of sending)
				acum_time += local_time + client_offset
				print "client offset: {0}".format(client_offset)
		print "current_time: {0}".format(local_time)
		print "acum time: {0}".format(acum_time)
		avg = (acum_time + local_time) / (len(self.connection_list))
		for sock in self.connection_list:
			if sock != self.server_sock:
				sock.send("post " + str(avg))
		# also set local time

	def accept_new_connection(self):
		new_sock, addr = self.server_sock.accept()
		print "New connection from {0}".format(addr)
		self.connection_list.append(new_sock)
		self.sync_time("send me time")


if __name__ == '__main__':
		server = TimeServer('localhost', 5000)
		server.run()
