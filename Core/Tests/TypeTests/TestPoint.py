"""
Tests the Point module, mostly the initializer

.. moduleauthor: SbSpider rajshorya@gmail.com
"""

# Base tetsing module
import unittest

# general usage libraries
from datetime import datetime
import uuid

# Module to test
from Core.Types import Point

from Core import version, copyright, licence

__author__ = "Shorya Raj"
__email__ = "rajshorya@gmail.com"
__version__ = version
__copyright__ = copyright
__licence__ = licence

class Test_PointInitialization(unittest.TestCase):
	"""
	Tests the initialization of points
	"""

	def Test_NoDataSpecified(self):
		"""
		Tests the initialization of the point when no data is specified
		"""
		point = Point()

		self.assertEquals(point.DeviceID, 0)
		self.assertEquals(point.Latitude, 0)
		self.assertEquals(point.Longitude, 0)
		# self.assertEquals(point.DateTime, datetime.now())

	def Test_DateTimeSpecified(self):
		"""
		Tests if the datetime is specified
		"""

		time = datetime.now()

		point = Point(DateTime = time)

		time = datetime(
			year = time.year,
			month = time.month,
			day = time.day,
			hour = time.hour,
			minute = time.minute,
			second = time.second,
			microsecond = round(time.microsecond / 1000) * 1000)

		self.assertEquals(point.DateTime, time)

	def Test_ExceptionThrownWhenWrongInput_DeviceID(self):
		"""
		Tests if an error is given if the DeviceID is not an integer
		"""
		with self.assertRaises(TypeError):
			point = Point(DeviceID = 'asd')

	def Test_ExceptionThrownWhenWrongInput_Latitude(self):
		"""
		TEsts if an error is given if the Latitude is not a float
		"""
		with self.assertRaises(TypeError):
			point = Point(Latitude = 'asd')

	def Test_ExceptionThrownWhenWrongInput_Longitude(self):
		"""
		Tests if an error is given if the Longitude is not a float
		"""
		with self.assertRaises(TypeError):
			point = Point(Longitude = 'asd')


	def Test_ExceptionThrownWhenWrongInput_DateTime(self):
		"""
		Tests if an error is given if the DateTime is not parseable
		"""
		with self.assertRaises(ValueError):
			point = Point(DateTime = 'asd')
