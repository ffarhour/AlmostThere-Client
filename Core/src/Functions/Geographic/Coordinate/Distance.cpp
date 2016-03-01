/*
	Distance.cpp

	SbSpider rajshorya@gmail.com

	Functions based on distance
	*/

#include "stdafx.h"

#define COORDINATE_DISTANCE_MODULE
#include "Distance.h"

PyObject * Distance_LatLongs(PyObject * self, PyObject * args){
	double lat1;
	double long1;

	double lat2;
	double long2;

	if (!PyArg_ParseTuple(args, "dddd", &lat1, &long1, &lat2, &long2)){
		return NULL;
	}

	double distance = Calculate_Distance_Between_LatLongs(lat1, long1, lat2, long2);

	return PyFloat_FromDouble(distance);
}

PyObject * Angle_LatLongs_And_Vertical(PyObject * self, PyObject * args){
	double lat1;
	double long1;

	double lat2;
	double long2;

	if (!PyArg_ParseTuple(args, "dddd", &lat1, &long1, &lat2, &long2)){
		return NULL;
	}

	double angle = Calculate_Angle_Between_LatLongs_And_Vertical(lat1, long1, lat2, long2);

	return PyFloat_FromDouble(angle);
}

static double Calculate_Distance_Between_LatLongs(double lat1, double long1, double lat2, double long2){
	// Great Circle Distance http://en.wikipedia.org/wiki/Great-circle_distance

	double Radius = 6371;

	lat1 = Degrees_To_Radians(lat1);
	lat2 = Degrees_To_Radians(lat2);

	long1 = Degrees_To_Radians(long1);
	long2 = Degrees_To_Radians(long2);

	double deltaLat = abs(lat2 - lat1);
	double deltaLong = abs(long2 - long1);

	//// Chord Length formula
	//double deltaX = cos(lat2) * cos(long2) - cos(lat1) * cos(long1);
	//double deltaY = cos(lat2) * sin(long2) - cos(lat1) * sin(long1);
	//double deltaZ = sin(lat2) - sin(lat1);

	//double C = sqrt(pow(deltaX, 2) + pow(deltaY, 2) + pow(deltaZ, 2));

	//double CA = 2 * asin(C / 2);

	double CA = pow(cos(lat2) * sin(deltaLong), 2);
	CA += pow(cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(deltaLong), 2);
	CA = sqrt(CA);
	CA = atan2(CA, (sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(deltaLong)));

	// Vincinty Formula

	double d = Radius * CA;

	return d;
}

static double Degrees_To_Radians(double degree){
	return degree / 180 * Py_MATH_PIl;
}

static double Calculate_Angle_Between_LatLongs_And_Vertical(double lat1, double long1, double lat2, double long2){
	/*
		Calculates the angle between the vertical and the line formed by two points, using the dot product formulae

		i.e. A . B = |A||B| cos(theta)
		*/

	// First, two vectors - one that goes from lat1 long1 to lat2 long2, and the other that goes from lat1 long1 to lat3 long1 (i.e. y unit vector)
	double vec1[2];
	double vec2[2];

	// Fill in values
	vec1[0] = long2 - long1;
	vec1[1] = lat2 - lat1;

	double lat3 = lat1 + 1;

	vec2[0] = long1 - long1;
	vec2[1] = lat3 - lat1;

	double dotProduct = vec1[0] * vec2[0] + vec1[1] * vec2[1];

	double magnitudeVec1 = sqrt(pow(vec1[0], 2) + pow(vec1[1], 2));
	double magnitudeVec2 = sqrt(pow(vec2[0], 2) + pow(vec2[1], 2));

	double arccos = dotProduct / (magnitudeVec1 * magnitudeVec2);

	double angle_RAD = acos(arccos);

	double Angle = angle_RAD / Py_MATH_PIl * 180;

	return Angle;
}