"""
Tests the functionality of the Core.Types.Database.Connectors.MongoConnection
module
"""

# Base unittesting module
import unittest

# Direct access library to Mongo, so that the expected values can be retrieved
# and thus allow us to compare the values we get with the ones we should have
# TODO - replace with mock / fake, so that the functionality of the code can
# be tested without an actual physical database
from pymongo import MongoClient

# General libraries that are needed
from datetime import datetime, timedelta


from Core.Types import Point
from Core.Types.Database.Connectors.MongoConnection import MongoConnection, \
    MongoPoint

from Core import version, licence, copyright

__author__ = "Shorya Raj"
__email__ = "rajshorya@gmail.com"
__version__ = version
__licence__ = licence
__copyright__ = copyright


class Mongo_Point_Conversion_Tests(unittest.TestCase):
	"""
	Tests the conversion methods of the MongoPoint class
	"""
	def setUp(self):

		self.mongoPoint = MongoPoint()
		self.point = Point(123, 123, 123, datetime.now())

	def Test_NoInputPoint(self):
		"""
		Tests when there is no input into MongoPoint - that there is nothing set.
		This is achieved by checking if an exception is thrown when we try and access
		"""
		self.assertRaises(AttributeError, lambda: self.mongoPoint.data)
		self.assertRaises(AttributeError, lambda: self.mongoPoint.point)

	def Test_InputCorePoint(self):
		"""
		Tests if the correct data type is converted
		"""
		mongo_point = MongoPoint(self.point)

		data = mongo_point.data

		# Tests if the point stored is the same as the point that was put in
		self.assertEquals(mongo_point.point, self.point)

		self.assertEquals(data['DeviceID'], self.point.DeviceID)
		self.assertEquals(data['Latitude'], self.point.Latitude)
		self.assertEquals(data['Longitude'], self.point.Longitude)
		self.assertEquals(data['DateTime'], self.point.DateTime)

	def Test_SetData(self):
		"""
		Tests the set data function
		"""
		time_val = datetime.now()
		self.mongoPoint.SetData(123, 123, 123, time_val)
		point = Point(123, 123, 123, time_val)

		self.assertEquals(point, self.mongoPoint.point)

class Mongo_Database(unittest.TestCase):
	"""
	Tests the database code
	"""

	@classmethod
	def setUpClass(cls):
		cls.client = MongoClient()
		cls.db = cls.client.testing_database
		cls.con = MongoConnection(Testing = True)

	def setUp(self):
		self.points = self.db.points
		self.point = Point(123, 123, 123, datetime.now())
		self.point2 = Point(234, 234, 234, datetime.now() + timedelta(days = 1))

	def tearDown(self):
		self.points.drop()

	@classmethod
	def tearDownClass(cls):
		cls.client.close()

	def Test_InsertCorePoint(self):
		"""
		Tests the insertion of a Core.Types.Point
		"""
		self.con.InsertPoint(self.point)

		points = list(self.points.find({
			'DeviceID' : self.point.DeviceID,
			'Latitude' : self.point.Latitude,
			'Longitude' : self.point.Longitude,
			'DateTime' : self.point.DateTime}))

		self.assertEquals(len(points), 1)

		point = points[0]

		self.assertEquals(point['DeviceID'], self.point.DeviceID)
		self.assertEquals(point['Latitude'], self.point.Latitude)
		self.assertEquals(point['Longitude'], self.point.Longitude)
		self.assertEquals(point['DateTime'], self.point.DateTime)

	def Test_InsertMongoPoint(self):
		"""
		Tests the insertion of a MongoPoint
		"""

		# THe mongo point created from the data
		mongo_point = MongoPoint(self.point)
		self.con.InsertPoint(mongo_point)

		# Gets point based on info in the CorePoint
		points = list(self.points.find({
			'DeviceID' : self.point.DeviceID,
			'Latitude' : self.point.Latitude,
			'Longitude' : self.point.Longitude,
			'DateTime' : self.point.DateTime}))

		# Gets the point from the MongoPoint definition
		points_from_mongo = list(self.points.find( mongo_point.data))

		self.assertEquals(len(points), 1)
		self.assertEquals(len(points_from_mongo), 1)

		# Does the Json match
		self.assertEquals(points[0], points_from_mongo[0])

		point = points[0]

		self.assertEquals(point['DeviceID'], self.point.DeviceID)
		self.assertEquals(point['Latitude'], self.point.Latitude)
		self.assertEquals(point['Longitude'], self.point.Longitude)
		self.assertEquals(point['DateTime'], self.point.DateTime)

	def Test_InsertUnusable(self):
		"""
		Tests if an error is raised when a non useable type is specified
		"""

		self.assertRaises(TypeError, self.con.InsertPoint, None)
		self.assertRaises(TypeError, self.con.InsertPoint, 123)

	def Test_GetPoint_OneVal_DeviceiD(self):
		"""
		Tests if a single deviceid can be used to search for points
		"""

		self.con.InsertPoint(self.point)
		self.con.InsertPoint(self.point2)

		points = self.con.GetPoints(DeviceID = self.point.DeviceID)

		self.assertEquals(len(points), 1)

		point = points[0]

		self.assertEquals(point, self.point)

	def Test_GetPoint_OneVal_Latitude(self):
		"""
		Tests if a single Latitude can be used to search for points
		"""
		self.con.InsertPoint(self.point)
		self.con.InsertPoint(self.point2)

		points = self.con.GetPoints(Latitude = self.point.Latitude)

		self.assertEquals(len(points), 1)

		self.assertEquals(points[0], self.point)

	def Test_GetPoint_OneVal_Longitude(self):
		"""
		Tests if a single Longitude can be used to search for points
		"""
		self.con.InsertPoint(self.point)
		self.con.InsertPoint(self.point2)

		points = self.con.GetPoints(Longitude = self.point.Longitude)

		self.assertEquals(len(points), 1)
		self.assertEquals(points[0], self.point)

	def Test_Getpoint_OneVal_DateTime(self):
		"""
		Tests if a single DateTime can be used to search for ppoints
		"""

		self.con.InsertPoint(self.point)
		self.con.InsertPoint(self.point2)

		points = self.con.GetPoints(DateTime = self.point.DateTime)

		self.assertEquals(len(points), 1)
		self.assertEquals(points[0], self.point)

	def Test_GetPoint_MultipleVals_General(self):
		"""
		Tests if multiple values can be returned by the method
		"""

		self.con.InsertPoint(self.point)
		self.con.InsertPoint(self.point2)

		point3 = Point(123, 123, 123, datetime.now())
		self.con.InsertPoint(point3)

		points = self.con.GetPoints(DeviceID = self.point.DeviceID)

		self.assertEquals(len(points), 2)

		self.assertEquals(points[0], self.point)
		self.assertEquals(points[1], point3)

	def Test_GetPoint_OneVal_AllSpeciifed(self):
		"""
		Tests if multiple values can be specified to get the correct
		point from the database
		"""

		self.con.InsertPoint(self.point)
		self.con.InsertPoint(self.point2)

		points = self.con.GetPoints(
				DeviceID = self.point.DeviceID,
				Latitude = self.point.Latitude,
				Longitude = self.point.Longitude,
				DateTime = self.point.DateTime)

		self.assertEquals(len(points), 1)

		self.assertEquals(points[0], self.point)
