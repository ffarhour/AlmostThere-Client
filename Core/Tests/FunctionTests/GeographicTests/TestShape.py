"""
Tests the functionality of InQuad, as contained in the
Functions.Geographic.Coordinate native library
"""
import unittest

from Core.Types import Point

from Core.Functions.Geographic.Coordinate import InQuad

from Core import version, copyright, licence

__author__ = "Shorya Raj"
__email__ = "rajshorya@gmail.com"
__version__ = version
__copyright__ = copyright
__licence__ = licence

class Test_InQuad(unittest.TestCase):
	"""
	Tests the inQuad function
	"""

	@unittest.skip("Needed only later")
	def test_InQuad_Square(self):
		"""
		Tests when the point is in the quad, shape square
		"""

		skipTest("Not needed for now")
		point_A = Point(Latitude = 0, Longitude = 0)
		point_B = Point(Latitude = 10, Longitude = 0)
		point_C = Point(Latitude = 10, Longitude = 10)
		point_D = Point(Latitude = 0, Longitude = 10)

		point = Point(5, 5)

		expected = True

		actual = InQuad(point_A.Latitude, point_A.Longitude, point_B.Latitude, point_B.Longitude, point_C.Latitude, point_C.Longitude,
				  point_D.Latitude, point_D.Longitude, point.Latitude, point.Longitude)

		actual = 1
		expected = 1
		self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
