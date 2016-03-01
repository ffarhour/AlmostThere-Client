"""
.. module::Query
.. moduleauthor:: Spider rajshorya@gmail.com

Query is query definition that allows Godfather to operate on Sentinel data.
It is structured so that the Query object is created in Godfather, pickled
and sent, then unpickled on the Sentinel side. Then, Sentinel goes through
and figures out what to do based on the data in the Query. This allows for a
standardised messaging module between the two.
"""

from enum import Enum, unique
#import cPickle as pickle
import pickle

from Core import version, licence, copyright

__author__ = "Shorya Raj"
__email__ = "rajshorya@gmail.com"
__version__ = version
__licence__ = licence
__copyright__ = copyright
__status__ = "Development"


@unique
class Urgency(Enum):
	"""
	An :class:`enum.Enum` that specifies the urgency of the task to be performed.
	Options are:

	* ``Urgency.Urgent`` - Urgent task
	* ``Urgency.Normal`` - Normal task
	"""
	Urgent = 1
	Normal = 2

@unique
class Action(Enum):
	"""
	The action to perform

	* ``Action.Calculate`` - Performs calculations
	* ``Action.Read`` - Read from database
	"""
	Calculate = 1
	Read = 2

class PointFilter:
	"""
	Used in conjunction with `Action.Read`

	This allows the points returend by the Action.Read query to be filtered according to a
	filter.

	The above options are made optional. The reason for this is that they can be changed later.


	The following values are present, to allow the decision on action be made

	* FilterBy [Something] variables. Determines what is to be filtered by, non-exclusive

		* ``FilterByDeviceID``
		* ``FilterByLatitude``
		* ``FilterByLongitude``
		* ``FilterByDateTime``

	* Range [Something] Variables. Determines that a range is to be returned for this specificaication. Non-Exclusive

		* ``RangeDeviceID``
		* ``RangeLatitude``
		* ``RangeLongitude``
		* ``RangeDateTime``

	* [Something] filter variables. When only one thing is to be filtered, this specifies with what to search. Non-Exclusive

		* ``DeviceIDFilter``
		* ``LatitudeFilter``
		* ``LongitudeFilter``
		* ``DateTimeFilter``

	* [Something] Range min and max variables. When Range[Something] is specified, these specifiy the min and max of the thing to be returned. Non-exclusive

		* DeviceID

			* ``DeviceIDRange_Min`` The Min of range of DeviceID's to search
			* ``DeviceIDRange_Max`` The max of range of DeviceID's to search

		* Latitude

			* ``LatitudeRange_Min`` The Min of range of Latitude to search
			* ``LatitudeRange_Max`` The Max of range of Latitude to search

		* Longitude

			* ``LongitudeRange_Min`` The Min of range of Longitude to search
			* ``LongitudeRange_Max`` The Max of range of Longitude to search

		* DateTime

			* ``DateTimeRange_Min`` The Min of range of DateTime to search
			* ``DateTimeRange_Max`` The Max of range of DateTime to search


	"""

	def __init__(self):

		self.FilterByDeviceID = False
		self.FilterByLatitude = False
		self.FilterByLongitude = False
		self.FilterByDateTime = False

		self.RangeDeviceID = False
		self.RangeLatitude = False
		self.RangeLongitude = False
		self.RangeDateTime = False


		self.DeviceIDRange_Min = None
		self.DeviceIDRange_Max = None

		self.LatitudeRange_Min = None
		self.LatitudeRange_Max = None

		self.LongitudeRange_Min = None
		self.LongitudeRange_Max = None

		self.DateTimeRange_Min = None
		self.DateTimeRange_Max = None

		self.DeviceIDFilter = None
		self.LatitudeFilter = None
		self.LongitudeFilter = None
		self.DateTimeFilter = None

	def FilterBySingleParameter(self, DeviceID = None, Latitude = None, Longitude = None, DateTime = None):
		"""
		Allows for filtering to happen using a single variable.

		:arg int DeviceID: The DeviceID to filter by
		:arg float Latitude: The Latitude to filter by
		:arg float Longitude: The Longitude to filter by
		:arg datetime.datetime: The DateTime to filter by
		:raises: Exception

		The defaults for the parameter are type ``None``. This is to allow flexibility. However, if all are None, then exception
		is thrown. The reason for this is that we want an explicity call to be made to return all points.

		This function will change the neccesary components (i.e. FilterBy booleans) so that type can be determined
		"""
		if DeviceID == None:
			if Latitude == None:
				if Longitude == None:
					if DateTime == None:
						raise Exception("No Parameter specified")

		if DeviceID != None:
			# Then use DeviceID to search by, after checking
			if Latitude != None or Longitude != None or DateTime != None:
				# Then too many parameters specified
				raise Exception("Too many parameters specified")
			else:
				# Otherwise, carry on

				# Change filterby
				self.FilterByDeviceID = True

				# The DeviceID to filter by
				self.DeviceIDFilter = DeviceID

		elif Latitude != None:
			# Check for others
			if Longitude != None or DateTime != None:
				# Don't need to check for datetime as done above
				raise Exception("Too many parameters specified")
			else:
				self.FilterByLatitude = True
				self.LatitudeFilter = Latitude

		elif Longitude != None:
			# Check for DateTime
			if DateTime != None:
				raise Exception("Too many parameters specified")
			else:
				self.FilterByLongitude = True
				self.LongitudeFilter = Longitude

		elif DateTime != None:
			self.FilterByDateTime = True
			self.DateTimeFilter = DateTime

	def FilterRange_DeviceID(self, DeviceID_Min, DeviceID_Max):
		"""
		Filters the range of DeviceID's from the specified Min to the specified max

		:arg int DeviceID_Min: The minimum DeviceID to retrieve
		:arg int DeviceID_Max: The maximum DeviceID to retrieve
		"""

		if DeviceID_Max < DeviceID_Min:
			raise Exception("Maximum lower than minimum")

		self.RangeDeviceID = True

		self.DeviceIDRange_Min = DeviceID_Min
		self.DeviceIDRange_Max = DeviceID_Max

	def FilterRange_Latitude(self, Latitude_Min, Latitude_Max):
		"""
		Filters the range of Latitude frmo the specified Min to the specified Max

		:arg float Latitude_Min: The minimum Latitude to retrive
		:arg float Latitude_Max: THe maximum Latitude to retreive
		"""
		if Latitude_Max < Latitude_Min:
			raise Exception("Maximum lower than minimum")

		self.RangeLatitude = True

		self.LatitudeRange_Min = Latitude_Min
		self.LatitudeRange_Max = Latitude_Max

	def FilterRange_Longitude(self, Longitude_Min, Longitude_Max):
		"""
		Filters the range of Longitude from the specified Min to the specified Max

		:arg float Longitude_Min: The minimum Longitude to retrieve
		:arg flaot Longitude_Max: The maximum Longitude to retrieve
		"""

		if Longitude_Max < Longitude_Min:
			raise Exception("Maximum lower than minimum")

		self.RangeLongitude = True

		self.LongitudeRange_Min = Longitude_Min
		self.LongitudeRange_Max = Longitude_Max

	def FilterRange_DateTime(self, DateTime_Min, DateTime_Max):
		"""
		Filters the range of DateTime from the specified Min tot he specified Max

		:arg datetime.datetime DateTime_Min: THe minimum DateTime to retreive
		:arg datetime.datetime DateTime_Max: The maximum DateTime to rertreive
		"""

		if DateTime_Max < DateTime_Min:
			raise Exception("Maximum lower than minimum")

		self.RangeDateTime = True

		self.DateTimeRange_Min = DateTime_Min
		self.DateTimeRange_Max = DateTime_Max

	def __eq__(self, other):
		if isinstance(other, PointFilter) == False:
			return False

		if self.FilterByDeviceID == other.FilterByDeviceID:
			if self.FilterByLatitude == other.FilterByLatitude:
				if self.FilterByLongitude == other.FilterByLongitude:
					if self.FilterByDateTime == other.FilterByDateTime:
						if self.RangeDeviceID == other.RangeDeviceID:
							if self.RangeLatitude == other.RangeLatitude:
								if self.RangeLongitude == other.RangeLongitude:
									if self.RangeDateTime == other.RangeDateTime:
										if self.DeviceIDRange_Min == other.DeviceIDRange_Min:
											if self.DeviceIDRange_Max == other.DeviceIDRange_Max:
												if self.LatitudeRange_Min == other.LatitudeRange_Min:
													if self.LatitudeRange_Max == other.LatitudeRange_Max:
														if self.LongitudeRange_Min == other.LongitudeRange_Min:
															if self.LongitudeRange_Max == other.LongitudeRange_Max:
																if self.DateTimeRange_Min == other.DateTimeRange_Min:
																	if self.DateTimeRange_Max == other.DateTimeRange_Max:
																		if self.DeviceIDFilter == other.DeviceIDFilter:
																			if self.LatitudeFilter == other.LatitudeFilter:
																				if self.LongitudeFilter == other.LongitudeFilter:
																					if self.DateTimeFilter == other.DateTimeFilter:
																						return True
		else:
			return False

	def __nq__(self, other):
		if isinstance(other, PointFilter) == False:
			return True

		if self.FilterByDeviceID == other.FilterByDeviceID:
			if self.FilterByLatitude == other.FilterByLatitude:
				if self.FilterByLongitude == other.FilterByLongitude:
					if self.FilterByDateTime == other.FilterByDateTime:
						if self.RangeDeviceID == other.RangeDeviceID:
							if self.RangeLatitude == other.RangeLatitude:
								if self.RangeLongitude == other.RangeLongitude:
									if self.RangeDateTime == other.RangeDateTime:
										if self.DeviceIDRange_Min == other.DeviceIDRange_Min:
											if self.DeviceIDRange_Max == other.DeviceIDRange_Max:
												if self.LatitudeRange_Min == other.LatitudeRange_Min:
													if self.LatitudeRange_Max == other.LatitudeRange_Max:
														if self.LongitudeRange_Min == other.LongitudeRange_Min:
															if self.LongitudeRange_Max == other.LongitudeRange_Max:
																if self.DateTimeRange_Min == other.DateTimeRange_Min:
																	if self.DateTimeRange_Max == other.DateTimeRange_Max:
																		if self.DeviceIDFilter == other.DeviceIDFilter:
																			if self.LatitudeFilter == other.LatitudeFilter:
																				if self.LongitudeFilter == other.LongitudeFilter:
																					if self.DateTimeFilter == other.DateTimeFilter:
																						return False
		return True



class Query:
	"""
	The Query class that will allow a common interface between Sentinel and Godfather.

	This contains a number of variables to facilitate the determination of function type.
	"""

	def __init__(self, urgency = Urgency.Normal, action = Action.Read):
		self.urgency = urgency
		self.Action = action

		self.PointFilter = PointFilter()


	def Pickle(self):
		"""
		Prepares the query for sending, by pickling it

		:returns: The pickled object
		"""
		return pickle.dumps(self)



	def unPickle(pickledData):
		"""
		unPicles the data, using the pickled data

		:arg pickledData: The pickled data
		:returns: The :class:`Core.Types.Query.Query` craeted from the pickled data
		"""
		query = pickle.loads(pickledData)
		return query

	def __eq__(self, other):
		if isinstance(other, Query) == False:
			return False

		if self.urgency == other.urgency:
			if self.Action == other.Action:
				if self.PointFilter == other.PointFilter:
					return True

		else:
			return False


	def __nq__(self, other):
		if isinstance(other, Query) == False:
			return True

		if self.urgency == other.urgency:
			if self.Action == other.Action:
				if self.PointFilter == other.PointFilter:
					return False

		return False
