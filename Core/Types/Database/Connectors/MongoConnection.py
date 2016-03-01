"""
Allows for connection to the MongoDatabase, along with the relevant
type that is held in the MongoDatabase (MongoPoint).
"""

from datetime import datetime
from pymongo import MongoClient
import os

from Core.Types import Point

from Core import version, licence, copyright

__author__ = "Shorya Raj"
__email__ = "rajshorya@gmail.com"
__version__ = version
__licence__ = licence
__copyright__ = copyright
__status__ = "Development"

class MongoConnection:
	"""
	The MongoDB Database Connector. Contains the relevant access code
	for connection to a MongoDB

	Testing - default is false. If set to true, then the testing database, rather than the
			normal database, is used. This allows for testing code to delete the data
			stored after each test

	Currently just supports point input and getting
	"""

	def __init__(self, Testing = False):
		self.client = MongoClient()

		if Testing == True:
			# Should be the same as that used by the testing code
			self.db = self.client.testing_database
		else:
			# Primary database. TODO - Consider changing this
			self.db = self.client.PrimaryDatabase

		self.points = self.db.points

		# Sets up indexing, ensuring that they are indexed
		self.points.ensure_index('DeviceID')
		self.points.ensure_index('Latitude')
		self.points.ensure_index('Longitude')
		self.points.ensure_index('DateTime')


	def InsertPoint(self, point):
		"""
		Inserts a point into the database. Accepts a point of type
		MongoPoint or Core.Types.Point.
		"""
		if type(point) == MongoPoint:
			# If the input type is MongoPoint, then, should contain the inside data
			self.points.insert(
					# inserts the data using the json document stored inside
					point.data
					)
		elif type(point) == Point:
			# If of type Core.Types.Point, then we can use MongoPoint
			# converter to convert it into the standard format used by the database
			mongo_point = MongoPoint(point)
			self.points.insert(
					mongo_point.data
					)
		else:
			# THe type can not be used
			raise TypeError('Unkown type')
	def GetPoints(self, DeviceID = None, Latitude = None, Longitude = None, DateTime = None):
		"""
		Gets points from the database using the specified values
		"""

		pointQuery = {}

		if DeviceID != None:
			pointQuery['DeviceID'] = DeviceID
		if Latitude != None:
			pointQuery['Latitude'] = Latitude
		if Longitude != None:
			pointQuery['Longitude'] = Longitude
		if DateTime != None:
			pointQuery['DateTime'] = DateTime

		points_data_list = self.points.find(pointQuery)


		points = []

		for point in points_data_list:
			datetime_input = self.TimeConverter(point['DateTime'])

			points.append(Point(
				DeviceID = point['DeviceID'],
				Latitude = point['Latitude'],
				Longitude = point['Longitude'],
				DateTime = datetime_input
				))

		return points

	def TimeConverter(self, DateTime):
		"""
		Helper function to convert time input into a DateTime

		:arg DateTime: The datetime to convert

		:returns: datetime.datetime -- the datetime object
		"""
		try:
			return datetime.strptime(DateTime, "%Y-%m-%d %H:%M:%S.%f")
		except:
			try:
				# If it gets here, then the time does not
				# have milliseconds specified
				return datetime.strptime(DateTime, "%Y-%m-%d %H:%M:%S")
			except:
				return DateTime


	def FileDump(self, path = None):
		"""
		Dumps all data to files. First determines if data has been written
		before. If it finds a file, then it uses the dates after the one
		specified in the file to get points
		"""

		if type(path) is not str:
			BASE_DIR = os.getcwd()
		else:
			BASE_DIR = path

		data_dir = os.path.join(BASE_DIR, "data")
		if not os.path.isdir(data_dir):
			os.makedirs(data_dir)

		dirs = os.listdir(data_dir)

		points = []

		if len(dirs) == 0:
			# Then nothing there, so we get all points
			points = self.GetPoints()
		else:
			years = []
			for dir_name in dirs:
				years.append(int(dir_name))

			years.sort()
			final_year = years[-1]

			year_dir = os.listdir(os.path.join(data_dir, str(final_year)))

			DateTime = None

			if len(year_dir) == 0:
				# Just use year
				DateTime = datetime(final_year, 1, 1)
			else:
				months = []
				for dir_name in year_dir:
					months.append(int(dir_name))

				months.sort()
				final_month = months[-1]

				month_dir = os.listdir(os.path.join(data_dir, str(final_year),\
										str(final_month)))

				if len(month_dir) == 0:
					DateTime = datetime(final_year, final_month, 1)
				else:
					days = []
					for dir_name in month_dir:
						days.append(int(dir_name.split('.')[0]))

					days.sort()

					final_day = days[-1]

					DateTime = datetime(final_year, final_month, final_day)

			points_dat = list(self.points.find({
				"DateTime" : {"$gte" : str(DateTime)}}
			))

			for point in points_dat:
				points.append(Point(
					DeviceID = point['DeviceID'],
					Latitude = point['Latitude'],
					Longitude = point['Longitude'],
					DateTime = point['DateTime']))


		if len(points) == 0:
			print("Nothing to store")
		else:
			self.WriteFile(points)


	def WriteFile(self, points):
		"""
		Writes to file. Here mainly so that filedump does not repeat code
		"""

		BASE_DIR = os.getcwd()
		data_dir = os.path.join(BASE_DIR, "data")

		if type(points) != list:
			raise TypeError("Expected list")

		points.sort(key=lambda item:item.DateTime, reverse = False)


		years = []
		for point in points:
			year = point.DateTime.year
			if year not in years:
				years.append(year)

		for year in years:
			if not os.path.isdir(os.path.join(data_dir, str(year))):
				os.mkdir(os.path.join(data_dir, str(year)))

		year_points = []

		for year in years:
			points_in_year = []
			for point in points:
				if point.DateTime.year == year:
					points_in_year.append(point)
			year_points.append(points_in_year)


		for year_point in year_points:
			# Year points is a list. Year_point is another list, of points
			year = year_point[0].DateTime.year

			months = []

			for point in year_point:
				month = point.DateTime.month
				if month not in months:
					months.append(month)

			# Makes directories for every month
			for month in months:
				dirname = os.path.join(data_dir, str(year), str(month))

				if not os.path.isdir(dirname):
					os.mkdir(dirname)

			month_points = []
			for month in months:
				points_in_month = []
				for point in year_point:
					if point.DateTime.month == month:
						points_in_month.append(point)
				month_points.append(points_in_month)

			for month_point in month_points:
				# Now we can go month by month
				month = month_point[0].DateTime.month

				days = []
				for point in month_point:
					day = point.DateTime.day
					if day not in days:
						days.append(day)

				days_points = []
				for day in days:
					points_in_day = []
					for point in month_point:
						if point.DateTime.day == day:
							points_in_day.append(point)
					days_points.append(points_in_day)

				for x in range(0, len(days)):
					day = days_points[x][0].DateTime.day
					filename = os.path.join(data_dir, str(year), str(month), \
											str(day) + ".points")
					f = open(filename, 'w')
					f.write(str(year) + "/" + str(month) + "/" + str(day) + "\n")

					points = days_points[x]
					f.write(str(len(points)) + "\n")

					for point in days_points[x]:
						point_message = "point " + str(point.DeviceID)
						point_message += " " + str(point.Latitude)
						point_message += " " + str(point.Longitude)
						point_message += " " + str(point.DateTime) + "\n"
						f.write(point_message)

					f.close()




	def close():
		"""
		Closes connection to the mongo database
		"""
		self.client.close()


class MongoPoint:
	"""
	A mapping of Mongo data points to Core.Types.Point

	If ConversionPoint specified, then checks if the input type is a Core.Types.Point, and
	if it is, then maps the data as required.
	"""
	def __init__(self, ConversionPoint = None):
		if ConversionPoint != None:
			# Sets the internal data variable to the one specified
			self.data = self.ConvertPoint(ConversionPoint)

			# An internal variable so that the data can be accessed in a normal format
			self.point = ConversionPoint

	def SetData(self, DeviceID, Latitude, Longitude,  DateTime):
		"""
		Creates a MongoPoint with Json Data variables using the specified data
		"""
		# Leverage the Point information, as it automatially checks that the values are
		# of the correct type
		point = Point(DeviceID, Latitude, Longitude, DateTime)

		self.data = self.ConvertPoint(point)
		self.point = point

	def ConvertToPoint(self):
		"""
		Converts the internal data to a Core.Types.Point type, and returns it.

		We don't need to worry about this being called before the MongoPoint has data
		in it - the self.data variable is only set when the data is actually changed.
		It will throw an error by itself if something goes wrong.
		"""

		# Just return the included point
		return point

	def ConvertPoint(self,ConversionPoint):
		"""
		Converts the input point into the data type of the mongoPoint, a json
		document.
		It then returns this vdocument
		"""
		if ConversionPoint != None:
			if type(ConversionPoint) == Point:
				jsonData = {
					'DeviceID' : ConversionPoint.DeviceID,
					'Latitude' : ConversionPoint.Latitude,
					'Longitude' : ConversionPoint.Longitude,
					'DateTime' : ConversionPoint.DateTime
						}
				return jsonData
			else:
				raise TypeError("Can not work with the type")

