"""
This class contains an overarching database type, that should hopefully allow
for wrapping around the database specific implementations. This would allow
for database agnostic development
"""

from Core.Types.Database.Connectors import CassandraConnection, \
    RedisConnection, MongoConnection

from Core import version, licence, copyright

__author__ = "Shorya Raj"
__email__ = "rajshorya@gmail.com"
__version__ = version
__licence__ = licence
__copyright__ = copyright
__status__ = "Prototype"

class DatabaseConnection:

	def __init__(self):
		pass
