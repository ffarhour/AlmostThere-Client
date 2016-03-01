"""
This module aims to provide a connection to the s3 system on AWS. This allows
for uploading data, potentially large amounts, to S3, especially as backup
mechanism or to allow for mapreducing to run.
"""

import boto
from boto.s3.connection import Location
from boto.s3.key import Key

class S3Connection:
	"""
	The connection class.

	bucketName - if none specified, then assumes insyt-default-bucket. Bucket must
		already exist. Note, this is the name of the bucjet
	AWS_ACCESS_KEY - if none specified, assumes that the values specified in
			config files or path variables are the ones to use
	AWS_SECRET_KEY - to be used in conjunction with AWS_ACCESS_KEY
	"""

	def __init__(self, bucketName = None, AWS_ACCESS_KEY = None, AWS_SECRET_KEY = \
				 None):

		if bucketName != None:
			self.bucketName = bucketName
		else:
			self.bucketName = "insyt-default-bucket"

		if AWS_ACCESS_KEY != None and AWS_SECRET_KEY != None:
			# Key was specified
			self.AWS_ACCESS_KEY = AWS_ACCESS_KEY
			self.AWS_SECRET_KEY = AWS_SECRET_KEY
			self.conn = boto.connect_s3(AWS_ACCESS_KEY, AWS_SECRET_KEY)
		else:
			self.conn = boto.connect_s3()

		print("Connected to S3 services. Accessing bucket ...")

		self.bucket = self.conn.get_bucket(self.bucketName)

		print("Bucket recieved")

	def GetValue(self, key):
		"""
		Returns the value specified by the key.

		key - string representing the key

		"""

		k = Key(self.bucket)

		k.key = key
		return k.get_contents_as_string()

	def SetValue(self, key, value):
		"""
		Sets the value of a key

		key - the key to store a value to.
		value - the value to store.
		"""
		k = Key(self.bucket)

		if isinstance(key, str) == False:
			raise TypeError("Key must be a string")

		k.key = key

		if isinstance(value, str):
			return k.set_contents_from_string(value)
		else:
			raise TypeError("Value is not a string")

	def GetFile(self, key, data_file_name = None):
		"""
		Reads a file from s3 using the specified key.

		key - the key from which to read
		data_file_name - the filename to which to write to. If not specified,
			assumed to be the same as the key.
		"""

		if not isinstance(key, str):
			raise TypeError("Key must be string")

		k = Key(self.bucket)

		k.key = key

		if data_file_name == None:
			data_file_name = key

		with open(data_file_name, 'wb') as f:
			return k.get_file(f)

	def SendFile(self, key, data_file = None, use_multipart = False):
		"""
		Sends a file to s3.

		key - the key to which to send
		data_file - the file to upload. If it is of file type, then that we
			upload directly, otherwise we use set_contents_from_filename
		use_multipart - do we use multiplat uploading? Better for packets
		"""

		if not isinstance(key, str):
			raise TypeError("Key must be a string")

		k = Key(self.bucket)

		k.key = key

		if data_file == None:
			data_file = key

		if isinstance(data_file, str):
			k.set_contents_from_filename(data_file)
		else:
			k.send_file(data_file)

	def DeleteKey(self, key):
		"""
		Deletes a key (and it's valeu)
		"""
		k = Key(self.bucket)

		return k.delete()
