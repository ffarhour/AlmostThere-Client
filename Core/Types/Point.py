"""
.. module:: Core.Types.Point
.. moduleauthor:: Spider rajshorya@gmail.com

The Point type is the primary workhorse for the system. Point contains the specification of what a Point
should be like. A Point is what is sent from a Client Device, allowing for tracking to occur. It is stored
in a Database on the Sentinel (there, it's created by storing values in the database, as opposed to pickling
this, as pickling is probably not ideal for allowing things like search).

"""

from datetime import datetime

# import cPickle as pickle
import pickle

from Core import version, licence, copyright

__author__ = "Shorya Raj"
__email__ = "rajshorya@gmail.com"
__version__ = version
__licence__ = licence
__copyriht__ = copyright
__status__ = "Development"

class Point:
	"""
	The Point class, for storing Point data.

	Default values are specified, in case a point is needed to be created and its values put in later

	:arg int DeviceID: The DeviceID, default is 0
	:arg float Latitude: The Latitude, default is 0
	:arg float Longitude: The Longitude, default is 0
	:arg datetime.datetime DateTime: The DateTime, default is now. Ideally should be
			datetime.datetime, but if specified as a useable string type, then
			constructor will automatically parse it.
	"""

	def __init__(self, DeviceID = 0, Latitude = 0, Longitude = 0, DateTime =  None):
		"""
			Initializes a Point.

			DeviceID - optional, the id of the device that made the ping
			Latitutde - optional, the latitude of the ping
			Longitude - optional, the longitude of the ping
			DateTime - optional, the Date and Time at which the ping was made
		"""


		try:
			self.DeviceID = int(DeviceID)
			self.Latitude = float(Latitude)
			self.Longitude = float(Longitude)
		except:
			raise TypeError("Input type is not useable")

		if DateTime == None:
			self.DateTime = datetime.now()
		else:
			if type(DateTime) is datetime:
				self.DateTime = datetime(
				year = DateTime.year,
				month = DateTime.month,
				day = DateTime.day,
				hour = DateTime.hour,
				minute = DateTime.minute,
				second = DateTime.second,
				microsecond = round(DateTime.microsecond / 1000) * 1000)
			else:
				try:
					self.DateTime = datetime.strptime(DateTime, "%Y-%m-%d %H:%M:%S.%f")
				except:
					self.DateTime = datetime.strptime(DateTime, "%Y-%m-%d %H:%M:%S")

	def Pickle(self):
		return pickle.dumps(self)

	def unPickle(self, data):
		point = pickle.loads(data)
		if type(point) == Point:
			return point
		else:
			raise TypeError("Could not unpickle")

	def __eq__(self, other):
		"""
		Tries to see if equal
		"""
		if other == None:
			return False

		if self.DeviceID == other.DeviceID:
			if self.Latitude == other.Latitude:
				if self.Longitude == other.Longitude:
					if self.DateTime == other.DateTime:
						return True

		return False

	def __nq__(self, other):
		if other == None:
			return True

		if self.DeviceID == other.DeviceID:
			if self.Latitude == other.Latitude:
				if self.Longitude == other.Longitude:
					if self.DateTime == other.DateTime:
						return False

		return True

	def __str__(self):
		return "point " + str(self.Latitude) + " " + str(self.Longitude) + " " + str(self.DateTime)
