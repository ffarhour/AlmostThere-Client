"""
A basic prediction algorithm impelentation, allowing for general predictions
to be made on arrival time. This implentation allows for past history, current
positions and other such variables to influence the outcome of the predicted
time that the object will arive.

Please note that this will later be swapped with code to connect to the
Prediction Engine
"""

# If set to true, then the native code in _Predictor is loaded, instead of
# the code here

Native = False

import math

from Core.Types import Point

from Core.Functions.Geographic.Coordinate import Distance_LatLongs, \
    ToGeo, ToCartesian
from Core.Functions.Math.Interpolation import Interpolate_Linear, \
    Interpolate_Linear_3Points

from Core import version, licence, copyright

__author__ = "Shorya Raj"
__email__ = "rajshorya@gmail.com"
__version__ = version
__licence__ = licence
__copyright__ = copyright
__status__ = "Development"

class Predictor:
	"""
	The python code for the Predictor
	"""

	def __init__(self):
		# The path that will be followed
		self.path = None

		# The destination that we aim to reach
		self.destination = None

		# THe current position, updated once we recieve data or interpolate
		self.currentPosition = None
		# List of all of the previous positions, updated whenever we add a new
        # point
		self.previousPositions = []

		# Record of the last point that has been completed by the object
		self.position_indexInPath = None

		# The predicted arrival time
		self.prediction = None

		self.average_speed = None

	def SetCurrentPosition(self, point):
		"""
		Sets the current position
		"""
		# So that we can correctly determine the position on a path
		self.previousPositions.append(self.currentPosition)

		self.currentPosition = point

		# self.Calculate()

	def SetDestination(self, point):
		"""
		Sets the destination - allowing us to make a prediction on the arrival
        time to the destination
		"""
		if type(point) != Point:
			raise TypeError("Incorrect Type")

		self.destination = point

	def SetPath(self, path):
		"""
		Sets the path to follow. If not set, then assumes straight distance
		"""

		for point in path:
			# Check if correct type
			if type(point) != Point:
				raise TypeError("Not of type Core.Types.Point")

		self.path = path

	def SetSpeed(self, speed):

		self.average_speed = speed


	def Calculate(self, average_speed = None):
		"""
		Calculates the time needed to go along the path
		"""
		if self.destination == None:
			raise ValueError("Destination not set")

		if average_speed == None:
			average_speed = self.average_speed

		if self.path == None:
			# If not path set, then assumes straight line, taking first point
            # as the current position and the final point as destination
			self.path = []
			self.path.append(self.currentPosition)
			self.path.append(self.destination)

		prediction = self.Modifier_Base(average_speed)

		self.prediction = prediction

		return prediction


	def Modifier_Base(self, average_speed = None, path = None, destination = None, currentPosition = None):
		"""
		The base modifier. This calculates the time based on distance and
        speed.

		Should be able to calculate the values based on data from within the
        class.

		However, there are optional parameters made available if this method
        is called outside of the Predictor class - such as from a unit test


		Params
		average_speed - The average speed of the object.
		path - The path to folllow
		destination - The destination point
		currentPosition - The current position, so that the distance may
        correctly be calculated

		Returns
		The expected time that the bus should take, in hours (as the
        great-circle formula is calculating the distance in km).
		"""

		if average_speed == None:
			average_speed = self.average_speed

		if path == None:
			path = self.path

		if destination == None:
			destination = self.destination

		if currentPosition == None:
			currentPosition = self.currentPosition

		distance = 0

		index = self.DeterminePath_Index()
		index_destination = self.DeterminePath_Index(currentPosition = destination)


		self.position_indexInPath = index

		# First we calculate the distance to travel
		for x in range(index, len(path)):
		# A for loop that loops through all of the points in the path above the last point that the object was on
			if x == index:
				# We are going to calculatethe distance between the point and the one before, rather than this point and the one after
				if index == index_destination:
					# Here, something different, as on same segment
					distance += Distance_LatLongs(currentPosition.Latitude, currentPosition.Longitude, destination.Latitude, destination.Longitude)
					break
				continue
			if x == index + 1:
				# if 1 + index, thenw we use the current position
				distance += Distance_LatLongs(path[x].Latitude, path[x].Longitude, currentPosition.Latitude, currentPosition.Longitude)
				continue

			if x == index_destination:
				# We are at the final point. Since this may not be the final path, we do a different calcilation here
				distance += Distance_LatLongs(path[x].Latitude, path[x].Longitude, destination.Latitude, destination.Longitude)
				break


			# Calculate the great circle distance between points in the path
			distance += Distance_LatLongs(path[x].Latitude, path[x].Longitude, path[x-1].Latitude, path[x-1].Longitude)

		timeTaken = distance / average_speed

		# returns the time
		return timeTaken

	def DeterminePath_Index(self, path = None, currentPosition = None):
		"""
		Determines which section of the path that the object is on
		"""
		if path == None:
			path = self.path

		if currentPosition == None:
			currentPosition = self.currentPosition

		# Lowest distance
		lowest_d = 0
		# lowest index
		lowest_i = 0

		# print(len(path))

		for index in range(len(path)):
			# print(index)
			if index == len(path) - 1:
				# We are interpolating forward
				break
			segment = self.InterpolateSection(path[index], path[index + 1])

			lowestDistance = 0

			for x in range(len(segment)):
				if x == 0:
					# As required for initial value
					lowestDistance = Distance_LatLongs(segment[x].Latitude, segment[x].Longitude, currentPosition.Latitude, currentPosition.Longitude)
					continue

				distance = Distance_LatLongs(segment[x].Latitude, segment[x].Longitude, currentPosition.Latitude, currentPosition.Longitude)

				if distance < lowestDistance:
					lowestDistance = distance

			if index == 0:
				lowest_d = lowestDistance
				lowest_i = index
			else:
				if lowestDistance < lowest_d:
					lowest_d = lowestDistance
					lowest_i = index

		return lowest_i



	def InterpolateSection(self, pointA, pointB, Resolution = 50):
		"""
		Interpolates the section of te path.
		"""
		if type(pointA) != Point:
			raise TypeError()
		if type(pointB) != Point:
			raise TypeError()

		x0, y0, z0 = ToCartesian(pointA.Latitude, pointA.Longitude)
		x1, y1, z1 = ToCartesian(pointB.Latitude, pointB.Longitude)

		distance = Distance_LatLongs(pointA.Latitude, pointA.Longitude, pointB.Latitude, pointB.Longitude)

		# distance = math.sqrt(math.pow(x1 - x0, 2) + math.pow(y1 - y0, 2) + math.pow(z1 - z0, 2))

		segment_size = distance / Resolution

		segments = []

		for index in range(Resolution):
			segment_distance = index * segment_size
			x, y, z = Interpolate_Linear_3Points(x0, y0, z0, x1, y1, z1, segment_distance)

			lat, lon = ToGeo(x, y, z)

			segments.append(Point(Latitude = lat, Longitude = lon))

		return segments

	def Modifier_API(self):
		"""
		Modifier that modifies the arrival time based on API data
		"""
		pass

	def Modifier_History(self):
		"""
		Modifies the data based on previous history of the bus
		"""
		pass

	def MOdifier_Traffic(self):
		pass

	def Modifier_UserGPS(self):
		"""
		Modifies the data based on data from user GPS positions
		"""
