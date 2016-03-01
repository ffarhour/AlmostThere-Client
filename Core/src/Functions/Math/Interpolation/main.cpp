/*
	Mainly present for module initialization
	*/
#include "stdafx.h"

// #include <Cartesian.h>
#include "Interpolation.h"

static PyMethodDef InterpolationMethods[] = {
		{ "Interpolate_Linear", Interpolate_Linear, METH_VARARGS, "Performs a linear interpolation" },
		{ "Interpolate_Linear_3Points", Interpolate_Linear_3Points, METH_VARARGS, "3d point linear interpolation" },
		{ NULL, NULL, 0, NULL }
};

static struct PyModuleDef InterpolationModule = {
	PyModuleDef_HEAD_INIT,
	"Interpolation",
	NULL,
	-1,
	InterpolationMethods
};

PyMODINIT_FUNC PyInit_Interpolation(void){
	PyObject * m;

	static void * INTERPOLATION_API[INTERPOLATION_API_pointers];
	PyObject * Interpolation_C_API_OBJECT;

	m = PyModule_Create(&InterpolationModule);

	if (m == NULL){
		return NULL;
	}

	/*
	if (import_Cartesian() < 0){
	return NULL;
	}*/

	INTERPOLATION_API[Linear_Interpolate_NUM] = (void *)Linear_Interpolate;

	Interpolation_C_API_OBJECT = PyCapsule_New((void *)INTERPOLATION_API, "INTERPOLATION._C_API", NULL);
	if (Interpolation_C_API_OBJECT != NULL){
		PyModule_AddObject(m, "_C_API", Interpolation_C_API_OBJECT);
	}

	return m;
}
