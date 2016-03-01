from setuptools import setup, find_packages
from distutils.core import setup, Extension
from distutils.dir_util import copy_tree
from distutils.command.build import build
import os

# Needs to match Core.version
version ="0.7"

# Needs to be similar to that of version
VERSION_MAJOR = "0"
VERSION_MINOR = "7"

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
OUTPUT_DIR = BASE_DIR


with open('requirements.txt') as f:
	required = f.read().splitlines()


# Functions.Geographic.Coordinate module
Functions_Geographic_Coordinate_DIR = os.path.join(BASE_DIR, "src", "Functions", "Geographic", "Coordinate")
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

Functions_Math_Interpolation_DIR = os.path.join(BASE_DIR, "src", "Functions", "Math", "Interpolation")
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



setup(
	name = "AlmostThere Core",
	version = version,
	packages = find_packages(),
	install_requires = required,

	author = "Shorya Raj, Farmehr Farhour",
	author_email = "rajshorya@gmail.com, ffarhour@gmail.com",

	test_suite = "Tests",
	tests_require = [required],

    ext_modules = [
		Functions_Geographic_Coordinate,
		Functions_Math_Interpolation
		],
	cmdclass= dict(build = Copy_Package),

    url = "www.almostthere.kiwi",
    license = "All rights reserved by Insyt",

    description = "The core package for the AlmostThere project",

    long_description = """
    This package contains the code for the operation of the AlmostThere project.
    It contains the neccessary code that is needed to operate the parts of the
    system, along with any definitions (such as the Core.Types.Point definition)
    that should be same across different parts of the system (for example,
    they should be exactly the same betweeen Sentinel, Godfather and our
    websites).
    """,
)
