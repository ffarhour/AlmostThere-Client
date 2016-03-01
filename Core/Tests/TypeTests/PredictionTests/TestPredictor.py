"""
Tests the functionality of the module Core.Types.Prediction.Predictor.

Tests the Value settting, calculation, section interpolation and
Base_Modifier
"""
# The base testing module
import unittest

# Insyt modules
from Core.Types import Point
from Core.Functions.Geographic.Coordinate import Distance_LatLongs

# The module to test
from Core.Types.Prediction import Predictor

from Core import version, copyright, licence

__author__ = "Shorya Raj"
__email__ = "rajshorya@gmail.com"
__version__ = version
__copyright__ = copyright
__licence__ = licence

class Test_Predictor_Setters(unittest.TestCase):
	"""
	Tests the setters in Core.Types.Prediction.Predictor
	"""

	def setUp(self):
		self.predictor = Predictor()
		self.point = Point()

	def test_SetCurrentPosition(self):
		self.predictor.SetCurrentPosition(self.point)

		self.assertEqual(self.predictor.currentPosition, self.point)

	def test_SetCurrentPosition_UpdatePrevopisPositions(self):
		self.predictor.SetCurrentPosition(self.point)

		point = Point(Latitude = 10, Longitude = 10)
		self.predictor.SetCurrentPosition(point)

		self.assertEqual(self.predictor.previousPositions[len(self.predictor.previousPositions) - 1], self.point)

		self.predictor.SetCurrentPosition(Point(Latitude = 20, Longitude = 20))

		self.assertEqual(self.predictor.previousPositions[len(self.predictor.previousPositions) - 1], point)


	def test_SetDestination(self):
		self.predictor.SetDestination(self.point)

		self.assertEqual(self.predictor.destination, self.point)

	def test_SetPath(self):
		points = []

		for x in range(10):
			points.append(Point(Latitude = x, Longitude = x))

		self.predictor.SetPath(points)

		self.assertEqual(self.predictor.path, points)

class Test_Predictor_Calculate(unittest.TestCase):
	"""
	Tests the calculate function
	"""
	def setUp(self):
		self.predictor = Predictor()

	def test_Basic_Calculate(self):
		"""
		A basic test of the calculate function in Predictor
		"""
		speed = 10

		pointA = Point(Latitude = 0, Longitude = 0)
		pointB = Point(Latitude = 10, Longitude = 10)

		# We are between A and B
		currentPosition = Point(Latitude = 5, Longitude = 5)

		distance = Distance_LatLongs(currentPosition.Latitude, currentPosition.Longitude, pointB.Latitude, pointB.Longitude)

		expected = 78.27790829048027;
		# expected = 1568.520556798576 / speed / 2;

		self.predictor.SetDestination(pointB)

		path = []
		path.append(pointA)
		path.append(pointB)

		self.predictor.SetPath(path)

		# MidPoint
		self.predictor.SetCurrentPosition(Point(Latitude = 5, Longitude = 5))

		actual = self.predictor.Calculate(average_speed = speed)

		self.assertEqual(actual, expected)

	def test_Complex_Calculate(self):
		"""
		A far more comprehensive test of the Calculate function
		"""
		path = []
		for x in range(100):
			path.append(Point(DeviceID = 1, Latitude = x, Longitude = x))

		currentPosition = Point(Latitude = 0.5, Longitude = 0.5)
		destination = Point(Latitude = 50, Longitude = 50)

		self.predictor.SetPath(path)
		self.predictor.SetCurrentPosition(currentPosition)
		self.predictor.SetDestination(destination)

		expected = round(1440.0024195697736, 11)
		actual = round(self.predictor.Calculate(5), 11)

		self.assertEqual(actual, expected)



class Test_Predictor_InterpolateSection(unittest.TestCase):

	def setUp(self):
		self.predictor = Predictor()

	@unittest.skip("Precision is closer now, but varies")
	def test_Section(self):
		"""
		Basic section formation, low resolution
		"""
		pointA = Point(Latitude = 0, Longitude = 0)
		pointB = Point(Latitude = 10,  Longitude = 10)

		resolution = 10

		sections = self.predictor.InterpolateSection(pointA, pointB, resolution)

		# for x in range(len(sections)):
		#	print(sections[x])

		self.assertEqual(len(sections), 10)

		# Current accuracy is two within one digit
		for x in range(len(sections)):
			#self.assertEqual(round(sections[x].Latitude, 1), x)
			# self.assertEqual(round(sections[x].Longitude, 1), x)
			self.assertAlmostEqual(sections[x].Latitude, x, 1)
			self.assertAlmostEqual(sections[x].Longitude, x, 1)


class Test_Predictor_Base_Modifier(unittest.TestCase):
	"""
	Tests the Modifier_Base function
	"""

	def setUp(self):
		self.predictor = Predictor()

	def test_TwoPoint_CurrentHalfway(self):
		"""
		Tests the time calculation for two points, with the object halfway in between first two
		"""
		speed = 10

		pointA = Point(Latitude = 0, Longitude = 0)
		pointB = Point(Latitude = 10, Longitude = 10)

		# We are between A and B
		currentPosition = Point(Latitude = 5, Longitude = 5)

		distance = Distance_LatLongs(currentPosition.Latitude, currentPosition.Longitude, pointB.Latitude, pointB.Longitude)

		expected = distance / speed;

		self.predictor.SetDestination(pointB)

		path = []
		path.append(pointA)
		path.append(pointB)

		self.predictor.SetPath(path)

		# MidPoint
		self.predictor.SetCurrentPosition(Point(Latitude = 5, Longitude = 5))

		actual = self.predictor.Modifier_Base(average_speed = speed)

		self.assertEqual(actual, expected)

	def test_FourPoint_CurrentHalfway(self):
		"""
		Tests the time calculation for four points, with the object halfway in between first two
		"""
		speed = 10

		pointA = Point(Latitude = 0, Longitude = 0)
		pointB = Point(Latitude = 10, Longitude = 10)
		pointC = Point(Latitude = 20, Longitude = 20)
		pointD = Point(Latitude = 30, Longitude = 30)

		# We are between A and B
		currentPosition = Point(Latitude = 5, Longitude = 5)

		distance = Distance_LatLongs(currentPosition.Latitude, currentPosition.Longitude, pointB.Latitude, pointB.Longitude)

		distance += Distance_LatLongs(pointB.Latitude, pointB.Longitude, pointC.Latitude, pointC.Longitude)
		distance += Distance_LatLongs(pointC.Latitude, pointC.Longitude, pointD.Latitude, pointD.Longitude)

		expected = distance / speed;

		expected = round(expected, 13)

		self.predictor.SetDestination(pointB)

		path = []
		path.append(pointA)
		path.append(pointB)
		path.append(pointC)
		path.append(pointD)

		self.predictor.SetPath(path)

		# MidPoint
		self.predictor.SetCurrentPosition(currentPosition)

		actual = self.predictor.Modifier_Base(average_speed = speed)

		self.assertEqual(actual, expected)


if __name__ == '__main__':
	unittest.main()
