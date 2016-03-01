"""
Tests Core.Types.Networking.Socket
"""

from Core import version

__author__ = "Shorya Raj"
__copyright__ = "Copyright (C) Insyt"
__licence__ = "n/a"
__version__ = version

from datetime import datetime
import unittest
import socket
import threading
from queue import Queue
import time

# Code by insyt
from Core.Types import Point

# Module to test
from Core.Types.Networking import Socket


class Test_Socket_Initialization(unittest.TestCase):
	"""
	Tests the initialization values, and if they are stored correctly
	"""

	def Test_Is_Server_Storage(self):
		"""
		Tests if the is server variable is correctly stored
		"""
		# Tests when false is stored
		s_socket = Socket(is_server = False)
		self.assertEquals(s_socket.is_server, False)

		# Tests when true is stored
		s_socket = Socket(is_server = True, port = 9090)
		self.assertEquals(s_socket.is_server, True)

class Test_Socket_ExceptionRaises(unittest.TestCase):
	"""
	A series of tests to determine if exceptions are raised when they should
	be
	"""

	def Test_ExceptionWhenAcceptingOnClient(self):
		"""
		Tests if an exception is raised (of type socket.error) when we
		try and accept a connection, when we are running as a client socket
		"""
		clientSocket = Socket()

		with self.assertRaises(socket.error):
			clientSocket.accept()

	def Test_ExceptionWhenConnectFromServer(self):
		"""
		Tests if an exception is thrown when we try and run the connect command
		from a server
		"""

		s_socket = Socket(is_server = True, port = 9090)

		with self.assertRaises(socket.error):
			s_socket.connect(socket.gethostname(), 9090)


class Test_Socket_ExceptionsNotRaised(unittest.TestCase):
	"""
	The counterpart of the Test_Socket_ExceptionRaises, ensuring that
	exceptions are not raised when operations are called as they should be
	"""

	def Test_ConnectOnClientSocket(self):
		"""
		Tests if a connecting using a client socket runs fine
		"""

		sock = Socket(is_server = False)
		sock.connect(host = "www.google.com", port = 80)

class Test_Socket_SendingData(unittest.TestCase):
	"""
	tests if data can be sent using the class
	"""

	def Test_ServerSocket_Send(self):
		"""
		Tests if socket of type server can send data, and if the data received
		is the same as the data sent
		"""

		data = "Hello"

		c_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s_sock = Socket(is_server = True, port = 9090)

		def c_sock_handle(sock, recvData):
			sock.connect((socket.gethostname(), 9090))
			dat_size = sock.recv(2048)
			recvData.put(sock.recv(2048))

		def s_sock_handle(sock, data):
			conn, addr = sock.accept()
			sock.SendData(data, conn)

		received_data = Queue()
		c_sock_thread = threading.Thread(target=c_sock_handle, args=(c_sock, \
																received_data))
		s_sock_thread = threading.Thread(target=s_sock_handle, args = ( \
															s_sock,
															data))

		s_sock_thread.start()
		c_sock_thread.start()

		s_sock_thread.join()
		c_sock_thread.join()

		self.assertEquals(data, received_data.get().decode('utf-8'))

	def Test_Client_Socket_Send(self):
		"""
		Tests if a socket of type client can send data, and if the data
		recevied is the same as the data sent
		"""

		data = "Hello"

		c_sock = Socket(is_server = False)

		s_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s_sock.bind((socket.gethostname(), 9090))
		s_sock.listen(10)

		q_data = Queue()

		def s_sock_handle(sock, q):
			# print commands slow the process down so that the code has enough
			# time to let both threads operate
			conn, addr = sock.accept()
			print(1)
			# The messaging service does not seem to understand how to work
			# This, so we use 1
			dat_size = conn.recv(1)
			print(2)
			q.put(conn.recv(2048))
			print(3)

		def c_sock_handle(sock, data):
			sock.connect(socket.gethostname(), 9090)
			sock.SendData(data)
			sock.Close()

		s_sock_thread = threading.Thread(target=s_sock_handle, args=(
									s_sock, q_data))
		c_sock_thread = threading.Thread(target=c_sock_handle, args=(
			c_sock, data))

		s_sock_thread.start()
		c_sock_thread.start()

		s_sock_thread.join()
		c_sock_thread.join()

		data_recv = q_data.get().decode('utf-8')
		print(data)
		print(data_recv)

		self.assertEquals(data, data_recv)

class Test_Socket_RecievingData(unittest.TestCase):
	"""
	Tests the data receiving function
	"""

	def Test_ServerRedceive(self):
		"""
		Tests if the server is able to recieve the message from a client
		thread
		"""

		data = "hello"

		s_sock = Socket(is_server = True, port = 9090)
		c_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		def c_sock_handle(sock, data):
			sock.connect((socket.gethostname(), 9090))
			sock.send(str(len(data)).encode('utf-8'))
			time.sleep(0.01)
			sock.send(data.encode('utf-8'))
			sock.close()

		def s_sock_handle(sock, q):
			conn, addr = sock.accept()
			q.put(sock.ReceiveData(conn))

		q = Queue()

		s_sock_thread = threading.Thread(target=s_sock_handle, args=(s_sock, q))
		c_sock_thread = threading.Thread(target=c_sock_handle, args=(
			c_sock, data))

		s_sock_thread.start()
		c_sock_thread.start()

		s_sock_thread.join()
		c_sock_thread.join()

		self.assertEquals(data, q.get())

	def Test_Server_Recieve_Large(self):
		"""
		Tests if the server can recieve large message (aka can it chunk it)
		"""
		data = "numb"

		for x in range(0, 1000):
			data += str(x)

		s_sock = Socket(is_server = True, port = 9090)
		c_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		def c_sock_handle(sock, data):
			sock.connect((socket.gethostname(), 9090))
			sock.send(str(len(data)).encode('utf-8'))
			time.sleep(0.01)
			sock.send(data.encode('utf-8'))
			sock.close()

		def s_sock_handle(sock, q):
			conn, addr = sock.accept()
			q.put(sock.ReceiveData(conn))

		q = Queue()

		s_sock_thread = threading.Thread(target=s_sock_handle, args=(s_sock, q))
		c_sock_thread = threading.Thread(target=c_sock_handle, args=(
			c_sock, data))

		s_sock_thread.start()
		c_sock_thread.start()

		s_sock_thread.join()
		c_sock_thread.join()

		self.assertEquals(data, q.get())

	def Test_ClientRedceive(self):
		"""
		Tests if the client is able to recieve the message from a server
		thread
		"""

		data = "hello"

		c_sock = Socket()
		s_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s_sock.bind((socket.gethostname(), 9090))
		s_sock.listen(10)

		def c_sock_handle(sock, q):
			sock.connect(socket.gethostname(), 9090)
			q.put(sock.ReceiveData())
			sock.Close()

		def s_sock_handle(sock, data):
			conn, addr = sock.accept()
			conn.send(str(len(data)).encode('utf-8'))
			conn.send(data.encode('utf-8'))

		q = Queue()

		c_sock_thread = threading.Thread(target=c_sock_handle, args=(c_sock, q))
		s_sock_thread = threading.Thread(target=s_sock_handle, args=(
			s_sock, data))

		s_sock_thread.start()
		c_sock_thread.start()

		s_sock_thread.join()
		c_sock_thread.join()

		self.assertEquals(data, q.get())

	def Test_Client_Recieve_Large(self):
		"""
		Tests if the client can recieve large message (aka can it chunk it)
		"""
		data = "numb"

		for x in range(0, 1000):
			data += str(x)

		c_sock = Socket()
		s_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s_sock.bind((socket.gethostname(), 9090))
		s_sock.listen(10)

		def c_sock_handle(sock, q):
			sock.connect(socket.gethostname(), 9090)
			q.put(sock.ReceiveData())
			sock.Close()

		def s_sock_handle(sock, data):
			conn, addr = sock.accept()
			conn.send(str(len(data)).encode('utf-8'))
			conn.send(data.encode('utf-8'))

		q = Queue()

		c_sock_thread = threading.Thread(target=c_sock_handle, args=(c_sock, q))
		s_sock_thread = threading.Thread(target=s_sock_handle, args=(
			s_sock, data))

		s_sock_thread.start()
		c_sock_thread.start()

		s_sock_thread.join()
		c_sock_thread.join()

		self.assertEquals(data, q.get())

class Test_Socket_BinarySend(unittest.TestCase):
	"""
	Tests the sending of binary data
	"""

	def Test_Server_SendBinary(self):
		"""
		Tests if a server can send binary data
		"""

		data = "Hello".encode("utf-8")

		c_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s_sock = Socket(is_server = True, port = 9090)

		def c_sock_handle(sock, q):
			sock.connect((socket.gethostname(), 9090))
			sock.recv(10)
			q.put(sock.recv(2048))

		def s_sock_handle(sock, data):
			conn, addr = sock.accept()
			sock.SendData(data, conn, is_string = False)

		q = Queue()

		c_sock_thread = threading.Thread(target=c_sock_handle, args=(
			c_sock, q))
		s_sock_thread = threading.Thread(target=s_sock_handle, args=(
			s_sock, data))

		s_sock_thread.start()
		c_sock_thread.start()

		self.assertEquals(data, q.get())

	def Test_Client_SendBinary(self):
		"""
		Tests if a client can send binary data
		"""

		data = "Hello".encode('utf-8')

		c_sock = Socket(is_server = False)
		s_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s_sock.bind((socket.gethostname(), 9090))
		s_sock.listen(10)

		def c_sock_handle(sock, data):
			sock.connect(socket.gethostname(), 9090)
			sock.SendData(data, is_string = False)

		def s_sock_handle(sock, q):
			conn, addr = sock.accept()
			conn.recv(2048)
			q.put(conn.recv(2048))

		q = Queue()

		c_sock_thread = threading.Thread(target=c_sock_handle, args=(
			c_sock, data))
		s_sock_thread = threading.Thread(target=s_sock_handle, args=(
			s_sock, q))

		s_sock_thread.start()
		c_sock_thread.start()

		self.assertEquals(data, q.get())

class Test_Socket_ReciveBinaryData(unittest.TestCase):
	"""
	Tests if bianry data can be recieved
	"""

	def Test_Server_RecieveBinaryData(self):
		"""
		Tests if binary data can be received by server socket
		"""
		data = "Hello".encode('utf-8')

		c_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s_sock = Socket(is_server = True, port = 9090)

		def c_sock_handle(sock, data):
			sock.connect((socket.gethostname(), 9090))

			sock.sendall(str(len(data)).encode('utf-8'))
			time.sleep(0.1)
			sock.sendall(data)

		def s_sock_handle(sock, q):
			conn, addr = sock.accept()
			q.put(sock.ReceiveData(conn, is_string = False))

		q = Queue()

		c_sock_thread = threading.Thread(target=c_sock_handle, args=(
			c_sock, data))
		s_sock_thread = threading.Thread(target=s_sock_handle, args=(
			s_sock, q))
		s_sock_thread.start()
		c_sock_thread.start()

		s_sock_thread.join()
		c_sock_thread.join()

		self.assertEquals(data, q.get())

	def Test_Client_RecieveBinaryData(self):
		"""
		Tests if binary data can be recieved by client socket
		"""
		data = "Hello".encode('utf-8')

		c_sock = Socket(is_server = False)
		s_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s_sock.bind((socket.gethostname(), 9090))
		s_sock.listen(10)

		def c_sock_handle(sock, q):
			sock.connect(socket.gethostname(), 9090)
			q.put(sock.ReceiveData(is_string = False))

		def s_sock_handle(sock, data):
			conn, addr = s_sock.accept()
			conn.sendall(str(len(data)).encode('utf-8'))
			conn.sendall(data)

		q = Queue()

		s_sock_thread = threading.Thread(target=s_sock_handle, args=(
			s_sock, data))
		c_sock_thread = threading.Thread(target=c_sock_handle, args=(
			c_sock, q))

		s_sock_thread.start()
		c_sock_thread.start()

		s_sock_thread.join()
		c_sock_thread.join()

		self.assertEquals(data, q.get())
