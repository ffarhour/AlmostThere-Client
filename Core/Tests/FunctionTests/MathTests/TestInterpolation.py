"""
Tests the Interpolate_Linear and Interpolate_Linear_3Points functions, as
contained in the Core.Functions.Math.Interpolation native library
"""

import unittest

from Core.Functions.Math.Interpolation import Interpolate_Linear, \
    Interpolate_Linear_3Points

from Core import version, licence, copyright

__author__ = "Shorya Raj"
__email__ = "rajshorya@gmail.com"
__version__ = version
__copyright__ = copyright
__licence__ = licence

class Test_Interpolation_Linear(unittest.TestCase):
	"""
	Tests linear interpolation
	"""
	def test_Linear_Interpolate_A(self):
		x0 = 1
		y0 = 1

		x1 = 3
		y1 = 3

		x = 2

		expected = 2
		actual = Interpolate_Linear(x0, y0, x1, y1, x)

		self.assertEqual(actual, expected)

class Test_Interpolation_Linear_3Points(unittest.TestCase):

	def test_Linear_Interpolate_3Points_A(self):
		x0 = 0
		y0 = 0
		z0 = 0

		x1 = 2
		y1 = 2
		z1 = 2

		distance = 1

		expected = (0.5773502691896258, 0.5773502691896258, 0.5773502691896258)

		actual = Interpolate_Linear_3Points(x0, y0, z0, x1, y1, z1, distance)

		self.assertEqual(actual[0], expected[0])
		self.assertEqual(actual[1], expected[1])
		self.assertEqual(actual[2], expected[2])

	def test_Linear_Interpolate_3Points_B(self):
		x0 = 6371.0
		y0 = 0
		z0 = 0

		x1 = 4485.44540790656
		y1 = 2908.1870961928576
		z1 = 10

		distance = 1

		expected = (6370.455981153423, 0.8390680367119765, 0.002885192764284012)

		actual = Interpolate_Linear_3Points(x0, y0, z0, x1, y1, z1, distance)

		self.assertEqual(actual[0], expected[0])
		self.assertEqual(actual[1], expected[1])
		self.assertEqual(actual[2], expected[2])


if __name__ == '__main__':
	unittest.main()
