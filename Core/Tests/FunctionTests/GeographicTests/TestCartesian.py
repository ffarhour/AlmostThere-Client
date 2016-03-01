"""
Tests the functionality of the functions ToCartesian and ToGeo, as contained
in the Functions.Geographic.Coordinate native library. The native sources
for these are under source/Functions/Geographic/Coordinate/Cartesian.cpp
"""
import unittest

from Core.Functions.Geographic.Coordinate import ToGeo, ToCartesian

from Core import version, copyright, licence

__author__ = "Shorya Raj"
__email__ = "rajshorya@gmail.com"
__version__ = version
__copyright__ = copyright
__licence__ = licence

class Test_ToCartesian(unittest.TestCase):
	"""
	Tests ToCartesian
	"""
	def test_AllZero(self):
		lat = 0
		lon = 0

		expectedx = 6378.137
		expectedy = 0
		expectedz = 0

		results = ToCartesian(lat, lon)

		actualx, actualy, actualz = results

		self.assertEquals(actualx, expectedx)
		self.assertEquals(actualy, expectedy)
		self.assertEquals(actualz, expectedz)

	def test_1010(self):
		lat = 10
		lon = 10

		expectedx = 6186.437066445539
		expectedy = 1090.835769269275
		expectedz = 1100.248542878017



		results = ToCartesian(lat, lon)

		actualx, actualy, actualz = results

		self.assertEquals(actualx, expectedx)
		self.assertEquals(actualy, expectedy)
		self.assertEquals(actualz, expectedz)



class Test_ToGeo(unittest.TestCase):

	def test_GEO_A(self):
		"""
		with x = 6371
			y = 0
			z = 0
		"""
		x = 6371
		y = 0
		z = 0

		expectedLat = 0
		expectedLong = 0

		results = ToGeo(x, y, z)

		actuallat = results[1]
		actuallon = results[0]

		self.assertEqual(actuallat, expectedLat)
		self.assertEqual(actuallon, expectedLong)

	def test_GEO_B(self):

		x = 6186.437066445538
		y = 1090.835769269275
		z = 1100.2485428780165

		expectedLat = 10
		expectedLong = 10

		actuallat, actuallong = ToGeo(x, y, z)

		self.assertEqual(round(actuallat, 2), expectedLat)
		self.assertEqual(actuallong, expectedLong)


if __name__ == '__main__':
	unittest.main()
