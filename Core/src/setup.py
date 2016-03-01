"""
Builds the python extension
"""

raise DeprecationWarning("setup.py in root directory should be used instead")

import os
from distutils.core import setup, Extension
from distutils.command.build import build

# TO move folders
from distutils.dir_util import copy_tree

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
OUTPUT_DIR = os.path.dirname(BASE_DIR)


VERSION_MAJOR = '0'
VERSION_MINOR = '5'

Functions_Geographic_Coordinate_DIR = os.path.join(BASE_DIR, "Functions", "Geographic", "Coordinate")
Functions_Geographic_Coordinate = Extension(
	# Expected Package name
	'Functions.Geographic.Coordinate',
	# Location of the sources. Since they are stored in a directory structure and since this is building all of the files, we
	# need to use the BASE_DIR variable.
	sources = [
		os.path.join(Functions_Geographic_Coordinate_DIR, "Cartesian.cpp"),
		os.path.join(Functions_Geographic_Coordinate_DIR, "Distance.cpp"),
		os.path.join(Functions_Geographic_Coordinate_DIR, "Shape.cpp"),
		os.path.join(Functions_Geographic_Coordinate_DIR, "main.cpp")
		],
	# The version number
	define_macros = [
			('VERSION_MAJOR', VERSION_MAJOR),
			('VERSION_MINOR', VERSION_MINOR)
		]
		)

Functions_Math_Interpolation_DIR = os.path.join(BASE_DIR, "Functions", "Math", "Interpolation")
Functions_Math_Interpolation = Extension(
		'Functions.Math.Interpolation',
		sources = [
		os.path.join(Functions_Math_Interpolation_DIR, "Interpolation.cpp"),
		os.path.join(Functions_Math_Interpolation_DIR, "main.cpp")
			],
	define_macros = [
			('VERSION_MAJOR', VERSION_MAJOR),
			('VERSION_MINOR', VERSION_MINOR)
		]
		)


class Copy_Package(build):
	def run(self):
		build.run(self)

		build_listing = os.listdir(os.path.join(BASE_DIR, 'build'))
		chosen_listing = None

		for listing in build_listing:
			if listing.find('lib') != -1:
				chosen_listing = listing

		copy_tree(os.path.join(BASE_DIR, 'build', chosen_listing), OUTPUT_DIR)



setup (
		# The whole of this in its entirety is Core_Native builds
	name = "Core_Native",
	# Overall version is the same as CORE
	version = VERSION_MAJOR + '.' + VERSION_MINOR,
	description = "Native code for the CORE componenet",
	ext_modules = [
		Functions_Geographic_Coordinate,
		Functions_Math_Interpolation
		],
	cmdclass= dict(build = Copy_Package)
		)
