"""
An area specification
"""

# import cPickle as pickle
import pickle


from Core.Types import Point


from Core import version, licence, copyright
__author__ = "Shorya Raj"
__email__ = "rajshorya@gmail.com"
__version__ = version
__licence__ = licence
__copyright__ = copyright

class Area:
	"""
	A number of points combining to make an area
	"""

	def __init__(self):
		self.points = []

	def SetArea(self, area):
		self.points = area

	def AddPoint(self, point):
		if type(point) == Point:
			self.points.append(point)
		else:
			raise TypeError("input point is not of type Point")

	def __eq__(self, other):
		if self.points == other.points:
			return True
		else:
			return False

	def __nq__(self, other):
		if self.points != other.points:
			return False
		else:
			return True

	def __str__(self, other):
		for point in self.points:
			print(str(point))

	def Pickle(self):
		return pickle.dumps(self)

	def unPickle(self, data):
		area = pickle.loads(data)

		if type(area) == Area:
			return area
		else:
			raise TypeError("Failed to unPickle")
