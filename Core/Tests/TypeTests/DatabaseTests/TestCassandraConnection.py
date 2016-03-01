"""
Tests the functionality of point insertion and retreival from a Cassandra
database, using the Core.Types.Database.Connectors.CassandraConnection
connector
"""

# Base unit testing library
import unittest

# Cassandra library, to allow for testing expected against actual values
# Todo - replace with a mock / fake, so that tests can be ran without an actual
# live Cassandra db running
from cassandra.cluster import Cluster

# General libraries that are needed for testing
from datetime import datetime, timedelta
import uuid

# Libraries by Insyt that are used
from Core.Types import Point

# The module that is being tested
from Core.Types.Database.Connectors import CassandraConnection


# Meta
from Core import version, copyright, licence

__author__ = "Shorya Raj"
__email__ = "rajshorya@gmail.com"
__version__ = version
__copyright__ = copyright
__licence__ = licence

class Test_CassandraConnection_PointInsertion(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.con = Cluster()
		cls.session = cls.con.connect('pointstorage')
		cls.db = CassandraConnection()

	@classmethod
	def tearDownClass(cls):
		cls.session.cluster.shutdown()
		cls.session.shutdown()

	def setUp(self):
		self.point = Point(123, 123, 123, datetime.now())

	def tearDown(self):
		self.session.execute("""
		truncate points
		""")

	def Test_Point_Insertion_PointType(self):
		self.db.InsertPoint(self.point)

		points_dat = self.session.execute("""
		Select * from points
		""")

		self.assertEquals(len(points_dat), 1)

		point_dat = points_dat[0]

		point = Point(
			DeviceID = point_dat.deviceid,
			Latitude = point_dat.latitude,
			Longitude = point_dat.longitude,
			DateTime = point_dat.datetime)

		print(self.point)
		print(point)

		self.assertEquals(point, self.point)

class Test_CassandraConnection_PointRetrieval(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.con = Cluster()
		cls.session = cls.con.connect('pointstorage')
		cls.db = CassandraConnection()

	@classmethod
	def tearDownClass(cls):
		cls.session.cluster.shutdown()
		cls.session.shutdown()

	def setUp(self):
		self.point = Point(123, 123, 123, datetime.now())

	def tearDown(self):
		self.session.execute("""
		truncate points
		""")

	def Test_SinglePoint_DeviceID(self):
		"""
		Tests the retrieval of a single point, given just the deviceid
		"""
		self.db.InsertPoint(self.point)

		points = self.db.GetPoints(DeviceID = self.point.DeviceID)

		self.assertEquals(len(points), 1)
		self.assertEquals(points[0], self.point)

	def Test_SinglePoint_Latitude(self):
		"""
		Tests the retrieval of a single point, given just the latitude
		"""
		self.db.InsertPoint(self.point)

		points = self.db.GetPoints(Latitude = self.point.Latitude)

		self.assertEquals(len(points), 1)
		self.assertEquals(points[0], self.point)

	def Test_SinglePoint_Longitude(self):
		"""
		Tests the retrieval of a single point, given just the longitude
		"""

		self.db.InsertPoint(self.point)

		points = self.db.GetPoints(Longitude = self.point.Longitude)

		self.assertEquals(len(points), 1)
		self.assertEquals(points[0], self.point)

	def Test_SinglePoint_DateTime(self):
		"""
		Tests the retrieveal of a single point, given just the datetime
		"""
		self.db.InsertPoint(self.point)

		points = self.db.GetPoints(DateTime = self.point.DateTime)

		self.assertEquals(len(points), 1)
		self.assertEquals(points[0], self.point)

	def Test_MultiplePoint(self):
		"""
		Tests the retrieval of a two points, to ensure that the system
		can aggregrate points
		"""

		self.db.InsertPoint(self.point)

		point2 = Point(123, 456, 789, datetime.now() + timedelta(minutes = 1))
		self.db.InsertPoint(point2)

		point3 = Point(123, 456, 789, datetime.now() + timedelta(days = 1))
		self.db.InsertPoint(point3)

		points = self.db.GetPoints(DeviceID = 123)

		print(self.point)
		print(points[0])
		print(point2)
		print(points[1])
		print(point3)
		print(points[2])

		self.assertEquals(len(points), 3)
		self.assertEquals(points[0], self.point)
		self.assertEquals(points[1], point2)
		self.assertEquals(points[2], point3)

	def Test_LotsOfInfoSpecified(self):
		"""
		All things are spec'd
		"""
		self.db.InsertPoint(self.point)

		points = self.db.GetPoints(
			DeviceID = self.point.DeviceID,
			Latitude = self.point.Latitude,
			Longitude = self.point.Longitude,
			DateTime = self.point.DateTime)

		self.assertEquals(len(points), 1)
		self.assertEquals(points[0], self.point)


class Test_CassandraConnection_CustomQuery(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.con = Cluster()
        cls.session = cls.con.connect('pointstorage')
        cls.db = CassandraConnection()

    @classmethod
    def tearDownClass(cls):
        cls.session.cluster.shutdown()
        cls.session.shutdown()

    def setUp(self):
        self.point = Point(123, 123, 123, datetime.now())

    def tearDown(self):
        self.session.execute("""
                             Truncate points
                             """)

    def Test_SimpleGet(self):
        """
        A simple getting function
        """
        self.db.InsertPoint(self.point)

        points = self.db.CustomRetrievalQuery("""
                                              Select * from points
                                              """)

        self.assertEquals(len(points), 1)
        self.assertEquals(points[0], self.point)
