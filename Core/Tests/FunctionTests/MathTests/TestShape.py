"""
Tests the Core.Functions.Math.Shape package
"""

import unittest
import math

# Insyt
from Core.Types import Point

# Module to test
from Core.Functions.Math.Shape import Point_In_Polygon, Polygon_Centroid

# Meta
from Core import version, licence, copyright

__author__ = "Shorya Raj"
__email__ = "rajshorya@gmail.com"
__version__ = version
__licence__ = licence
__copyright__ = copyright

class Test_Point_In_Polygon(unittest.TestCase):
	"""
	Tests the Point_In_Polygon package against a number of scenarios
	"""

	def Test_SimpleCase_4Points_True(self):
		"""
		Tests a simple case, where polygon is four points, and the point is
		inside
		"""


		# Point to check
		point = (0.5, 0.5)


		# Points for polygon
		points = []
		points.append((0, 0))
		points.append((0, 1))
		points.append((1, 1))
		points.append((1, 0))

		expected = True
		actual = Point_In_Polygon(point, points)

		self.assertEquals(expected, actual)

	def Test_Simple_Case_4Point_False(self):
		"""
		Tests a simple four sided polygon, where the case is false
		"""
		point = (10, 10)

		points = []
		points.append((0, 0))
		points.append((0, 0))
		points.append((0, 0))
		points.append((0, 0))

		expected = False
		actual = Point_In_Polygon(point, points)

		self.assertEquals(expected, actual)

	def Test_3Point_True(self):
		"""
		Tests triangle shape, where case if true
		"""

		point = (0.5, 0.5)

		points = []
		points.append((0, 0))
		points.append((0.5, 1))
		points.append((1, 0))

		expected = True
		actual = Point_In_Polygon(point, points)

		self.assertEquals(expected, actual)

	def Test_5Point_True(self):
		"""
		Tests pentagon
		"""

		point = (0, 1)

		points = []
		points.append((-0.5, 0))
		points.append((-1, 1))
		points.append((0, 2))
		points.append((1, 1))
		points.append((0.5, 0))

		expected = True
		actual = Point_In_Polygon(point, points)

		self.assertEquals(expected, actual)

	def Test_4CorePoint_True(self):
		"""
		Tests if 4 core points can be used to resolve if the point is in
		centre
		"""

		point = Point(Latitude = 0.5, Longitude = 0.5)

		points = []
		points.append(Point(Latitude = 0, Longitude = 0))
		points.append(Point(Latitude = 1, Longitude = 0))
		points.append(Point(Latitude = 1, Longitude = 1))
		points.append(Point(Latitude = 0, Longitude = 1))

		expected = True
		actual = Point_In_Polygon(point, points)

		self.assertEquals(expected, actual)


class Test_Polygon_Centroid(unittest.TestCase):
	"""
	Tests the Polygon_Centroid package against a number of scenarious
	"""

	def Test_SimpleClose_4Points(self):
		"""
		Tests a simple use case, with 4 points
		"""
		points = []

		# Input must be a list of tuples
		points.append((0, 0))
		points.append((1, 0))
		points.append((1, 1))
		points.append((0, 1))

		midpoint_expected = (0.5, 0.5)
		midpoint_actual = Polygon_Centroid(points)

		self.assertEquals(midpoint_expected, midpoint_actual)
