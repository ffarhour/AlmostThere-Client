"""
Cassandra Connection is the connector to allow for communication with the
Cassandra database, able to input and retrieve data of type Core.Types.Point
"""

from cassandra.cluster import Cluster
# from cassandra.encoder import Encoder
import calendar
from datetime import datetime, timedelta
import uuid
import six


from Core.Types import Point

from Core import version, licence, copyright

__author__ = "Shorya Raj"
__email__ = "rajshorya@gmail.com"
__version__ = version
__licence__ = licence
__copyright__ = copyright
__status__ = "Development"


if six.PY3:
    long = int


def cql_encode_datetime(val):
	"""
		Converts a :class:`datetime.datetime` object to a (string) integer
		tamestamp with millisecond precision.
	"""
	timestamp = calendar.timegm(val.utctimetuple())
	return str(long(timestamp * 1e3 + getattr(val, 'microsecond', 0) / 1e3))


class CassandraConnection:

	def __init__(self):
		self.cluster = Cluster()
		# self.cluster = Cluster(
		# ['ec2-54-79-117-181.ap-southeast-2.compute.amazonaws.com'])
		self.session = self.cluster.connect('pointstorage')

	def GetPoints(self, DeviceID=None,
				  Latitude=None,
				  Longitude=None,
				  DateTime=None):

		queryStatement = "Select * from points where "

		changed = False
		multiple_stats = False


		if DeviceID != None:
			changed = True
			queryStatement += "deviceid = "  + str(DeviceID) + " "

		if Latitude != None:
			if DeviceID != None:
				multiple_stats = True
				queryStatement += " and "
			queryStatement += "latitude = "  + str(Latitude) + " "
			changed = True

		if Longitude != None:
			if DeviceID != None or Latitude != None:
				queryStatement += " and "
				multiple_stats = True
			queryStatement += "Longitude = " + str(Longitude) + " "
			changed = True

		if DateTime != None:
			if DeviceID != None or Latitude != None or Longitude != None:
				queryStatement += " and "
				multiple_stats = True
			queryStatement += "DateTime = '" + cql_encode_datetime(DateTime) + "' "
			changed = True


		if changed == False:
			queryStatement = "Select * from points"

		if multiple_stats == True:
			queryStatement += " ALLOW FILTERING "

		print(queryStatement[80:])

		points_dat = self.session.execute(queryStatement)

		points = []

		for point_dat in points_dat:
			points.append(Point(
			DeviceID = point_dat.deviceid,
			Latitude = point_dat.latitude,
			Longitude = point_dat.longitude,
			DateTime = point_dat.datetime))

		# Sorts by datetime
		points.sort(key = lambda x: x.DateTime)


		return(points)

	def CustomRetrievalQuery(self, query):
		"""
		Runs a query specified by the query argument. Allows for customized
		operations to be performed
		"""

		points_dat = self.session.execute(query)

		points = []

		for point_dat in points_dat:
			points.append(Point(
				DeviceID = point_dat.deviceid,
				Latitude = point_dat.latitude,
				Longitude = point_dat.longitude,
				DateTime = point_dat.datetime))
		return points


	def InsertPoint(self, point):

		if type(point) != Point:
			raise TypeError("Unuseable type")

		insertionString = "INSERT INTO points (id, datetime, deviceid, latitude, longitude) "
		insertionString += " values ( "  + str(uuid.uuid4()) + " , '"
		# insertionString += str(point.DateTime.year) + "-"
		# insertionString += str(point.DateTime.month) + "-"
		# insertionString += str(point.DateTime.day) + " "
		# insertionString += str(point.DateTime.hour) + ":"
		# insertionString += str(point.DateTime.minute) + ":"
		# insertionString += str(point.DateTime.second) + ":"

		insertionString += cql_encode_datetime(point.DateTime) + "', "
		insertionString += str(point.DeviceID) + " , "	+ str(point.Latitude) + " , "
		insertionString += str(point.Longitude) + " )"

		self.session.execute(insertionString)
