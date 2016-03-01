"""
The socket implementation.
"""

from Core import version, licence, copyright

__author__ = "Shorya Raj"
__copyright__ = "Copyright (C) Insyt"
__licence__ = "n/a"
__version__ = version
__licence__ = licence
__copyright__ = copyright

import socket
import threading
import ssl
import time

class Socket:
	"""
	A base socket class, allowing systems to implement a single definition
	of a socket.

	port - the port to use, if creating a server
	is_server - is this a server? If yes, then binds rather than connects

	use_ssl - if set to true (default), then uses ssl connection instead
	of normal socket
	"""

	def __init__(self, port = None, is_server = False, use_ssl = True):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.is_server = is_server

		if is_server == True:
			self.socket.bind(('', port))
			self.socket.listen(10)
		else:
			self.socket_connected = False

	def accept(self, action = None):
		"""
		Listens for a connection on the socket.
		Requires that the socket has been created as a server socket

		action - the action to perform when we succeed with receving a
		connection. The purpose is that it simplifies threading this sort of
		connection. Defaults to none - what this means is that if action is none,
		then it returns the connection object and the address, and if it is
		specified, then it returns whatever action returns. Note that action
		must take only two arguements - conn and address

		"""
		if not self.is_server:
			raise socket.error("""Is not a server, yet was requested to
					  accept a connection""")

		conn, address = self.socket.accept()


		if action == None:
			return conn, address
		else:
			return action(conn, address)


	def connect(self, host, port):
		"""
		If we are a client socket, then we connect to the specified host and
		port

		Host - the host to connect to
		Port - the port to connect to
		"""
		if self.is_server:
			raise socket.error("""A server socket was used in place of a client
							   socket for connecting""")

		self.socket.connect((host, port))
		self.socket_connected = True


	def SendData(self, data, conn = None, is_string = True):
		"""
		Sends data to the connection object specified.

		This assumes that the data being sent is a string.

		data = the data to send
		conn - the connection to which to send the data. Defaults to none.
		If the socket is a server socket, then the conn must be specified.
		Otherwise, if it is a client socket, then you do not need to specify
		the connection (however, connect should have been run).

		is_string - the data being sent a string? If yes, then we encode,
			otherwise we ssumes that the data being sent is in binary format
		"""
		if self.is_server == False:
			if self.socket_connected:
				conn = self.socket
			else:
				raise Exception("Socket not connected to anything")
		else:
			if conn == None:
				raise AttributeError("conn was not specified")

		# THis works regardless of bnrary format or not
		sent = conn.sendall(str(len(data)).encode('utf-8'))

		# Very small timer so that the reciving socket has enough time to
		# process
		time.sleep(0.001)

		if sent == 0:
			raise RuntimeError("Socket connection broken")

		if is_string:
			# IF string, then encode in utf-8 and then send
			sent = conn.sendall(data.encode('utf-8'))
		else:
			sent = conn.sendall(data)

		if sent == 0:
			raise RuntimeError("socket connection broken")

	def ReceiveData(self, conn = None, is_string = True):
		"""
		Receives the data from the socket. If this is a server, then the
		connection object needs to be specified, otherwise not.

		conn - Connection object
		is_string - is a string being returned expected? IF yes (default), then
			we decode it usnig utf-8, otherwise we just return the binary format
		"""

		if self.is_server == False:
			if self.socket_connected:
				conn = self.socket
			else:
				raise IOError("Socket not connected to anything")
		else:
			if conn == None:
				raise AttributeError("connection was not specified for server \
									 socket")

		# Turns the input message into a number specified number of butes
		msg_len = int(conn.recv(24).decode('utf-8'))

		bytes_left = msg_len
		data = None

		while bytes_left > 0:
			chunk = None

			chunk = conn.recv(2048)

			if bytes_left == msg_len:
				data = chunk
			else:
				data += chunk

			bytes_left -= len(chunk)

		if is_string:
			# If string, decode
			return data.decode('utf-8')
		else:
			# otherwise leave it
			return data

	def Close(self):
		"""
		closes the socket
		"""
		if self.is_server == False:
			self.socket.close()
