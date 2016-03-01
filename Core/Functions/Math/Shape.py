"""
Shape functions
"""

import math


from Core.Types import Point

from Core.Functions.Geographic.Coordinate import ToGeo, ToCartesian

__author__ = "Shorya Raj"
__email__ = "rajshorya@gmail.com"

def Point_In_Polygon(point_to_check, points):
	"""
	Determines if a point is within a polygon.

	The algorithm used is ray casting.

	point_to_check is the point to check (tuple)
	points are the points that make the polygon
	"""

	# First check the values of the inputs
	if type(point_to_check) is Point:
		# Then convert to x, y ,z
		point_to_check = (point_to_check.Latitude, point_to_check.Longitude)
	elif type(point_to_check) is tuple:
		# If it is a tuple, then ignore and go on
		pass
	else:
		# Then error
		raise TypeError("Input is not useable")


	if type(points) is not list:
		raise TypeError("Polygon points are not list")
	else:
		# Check if the inputs are lat long points
		for i in range(0, len(points)):
			if type(points[i]) is Point:
				# Try and convert
				# Super advanced conversion
				points[i] = (points[i].Latitude, points[i].Longitude)
			elif type(points[i]) is not tuple:
				# THen can not use
				raise TypeError("Polygon point type is not tuple or Core.Point")

	# Now, for calculation, we need last point in polygon to be the same as the
	# first point
	if points[0] != points[-1]:
		points.append(points[0])

	# We use the raycasting algorithm

	counter = 0

	xinters = 0

	p1 = points[0]
	p2 = 0

	N = len(points)
	for x in range(1, N):
		p2 = points[ x % N]

		if point_to_check[1] > min(p1[1], p2[1]):
			if point_to_check[1] <= max(p1[1], p2[1]):
				if point_to_check[0] <= max(p1[0], p2[0]):
					if p1[1] != p2[1]:
						xinters = (point_to_check[1] - p1[1]) * (p2[0] - p1[0])
						xinters /= ( p2[1] - p1[1])
						xinters += p1[0]

						if p1[0] == p2[0] or point_to_check[0] <= xinters:
							counter += 1

		p1 = p2

	if counter % 2 == 0:
		return False
	else:
		return True


def Polygon_Centroid(points):
	"""
	Returns the centroid of the polygon
	http://stackoverflow.com/questions/19766485/how-to-calculate-centroid-of-polygon-in-c
	"""

	# Check for types
	if type(points) is not list:
		raise TypeError("Expected a list")
	else:
		for i in range(0, len(points)):

			if type(points[i]) is Point:
				# Convert to cartesian
				x, y, z = ToCartesian(points[i].Latitude, points[i].Longitude)
				points[i] = (x, y, z)
			elif type(points[i]) is not tuple:
				raise TypeError("Point is not Core.Types.Point or tuple")

	if points[0] != points[-1]:
		points.append(points[0])

	a = 0.0
	i1 = 1

	n = len(points)

	for i in range(0, n - 1):
		a += points[i][0] * points[i1][1] - points[i1][0] * points[i][1]
		i1 += 1

	a *= 0.5

	cx = cy = 0.0

	i1 = 1
	for i in range(0, n - 1):
		cx += (points[i][0] + points[i1][0]) * (points[i][0] * points[i1][1] - \
										points[i1][0] * points[i][1])
		cy += (points[i][1] + points[i1][1]) * (points[i][0] * points[i1][1] - \
										points[i1][0] * points[i][1])

		i1 += 1


	cx /= (6 * a)
	cy /= (6 * a)

	return (cx, cy)
