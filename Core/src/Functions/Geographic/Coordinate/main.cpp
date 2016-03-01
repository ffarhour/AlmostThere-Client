/*
	Main.cpp

	SbSpider rajshorya@gmail.com

	Version: 0.1

	Functions.Geographic.Coordinate contains the functions to operate on coordinates.
	*/

#include "stdafx.h"

#include "Distance.h"
#include "Cartesian.h"
#include "Shape.h"

#include <math.h>

static PyMethodDef CoordinateMethods[] = {
		{ "Angle_LatLongs_And_Vertical", Angle_LatLongs_And_Vertical, METH_VARARGS, "Calculates the angle between two Latitude and Longitude points" },
		{ "Distance_LatLongs", Distance_LatLongs, METH_VARARGS, "Calculates the distance between two Latitude and Longitude points" },
		{ "ToCartesian", ToCartesian, METH_VARARGS, "Converts the input latitude and longitude into relevant xyz coordinates" },
		{ "ToGeo", ToGeo, METH_VARARGS, "Converts cartesian coordinates into geographic ones" },
		{ "InQuad", InQuad, METH_VARARGS, "Determins if a point is within the a set of four points forming a quadrilateral" },
		{ NULL, NULL, 0, NULL }
};

static struct PyModuleDef CoordinateModule = {
	PyModuleDef_HEAD_INIT,
	"Coordinate",
	NULL,
	-1,
	CoordinateMethods
};

PyMODINIT_FUNC PyInit_Coordinate(void){
	PyObject * m;

	// For distance module
	static void * DISTANCE_API[DISTANCE_API_pointers];
	PyObject * Distance_C_API_OBJECT;

	// For cartesian module
	static void * CARTESIAN_API[CARTESIAN_API_pointers];
	PyObject * Cartesian_C_API_OBJECT;

	m = PyModule_Create(&CoordinateModule);
	if (m == NULL){
		return NULL;
	}

	// Distance module init
	DISTANCE_API[Calculate_Angle_Between_LatLongs_And_Vertical_NUM] = (void *)Calculate_Angle_Between_LatLongs_And_Vertical;
	DISTANCE_API[Calculate_Distance_Between_LatLongs_NUM] = (void *)Calculate_Distance_Between_LatLongs;
	DISTANCE_API[Degrees_To_Radians_NUM] = (void *)Degrees_To_Radians;

	Distance_C_API_OBJECT = PyCapsule_New((void *)DISTANCE_API, "DISTANCE._C_API", NULL);
	if (Distance_C_API_OBJECT != NULL){
		PyModule_AddObject(m, "_C_API", Distance_C_API_OBJECT);
	}

	CARTESIAN_API[_ToCartesian_NUM] = (void *)_ToCartesian;
	CARTESIAN_API[_ToGeo_NUM] = (void *)_ToGeo;

	Cartesian_C_API_OBJECT = PyCapsule_New((void *)CARTESIAN_API, "CARTESIAN._C_API", NULL);
	if (Cartesian_C_API_OBJECT != NULL){
		PyModule_AddObject(m, "_C_API", Cartesian_C_API_OBJECT);
	}

	return m;
}