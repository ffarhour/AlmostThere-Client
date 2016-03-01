"""
Function list:

Coordinate:
	- Distance_LatLongs(lat1, long1, lat2, long2)
		Calculates the great-circle distance between two sets of geographic points
	- Angle_LatLongs_And_Vertical(lat1, long1, lat2, long2)
		Calculates the angle between the line formed by two points and the vertical

	- ToCartesian(lat, lon)
		Returns the xyz coordiantes of a point based on the lat lon point
	- ToGeo (x, y, z)
		Retusn the geographic coordinates of a point based on the cartesian coordinates

	- InQuad(lat1, lon1, lat2, lon2, lat3, lon3, lat4, lon4, point_lat, point_lon)
		The first four sets of lat lon points form the quad, and then run a test to determine
		if point_lat point_lon fall inside of the formed quad

"""
from Core import version, licence, copyright

__author__ = "Shorya Raj"
__email__ = "rajshorya@gmail.com"
__version__ = version
__licence__ = licence
__copyright__  = copyright

__summary__ = "Module relating to the Geographic Functions"
