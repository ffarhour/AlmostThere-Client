/*
	Interpolation.cpp

	Spider rajshorya@gmail.com
	*/

#include "stdafx.h"

#define INTERPOLATION_INTERPOLATION_MODULE
#include "Interpolation.h"

// #include <Cartesian.h>

PyObject * Interpolate_Linear(PyObject * self, PyObject  * args){
	double x0;
	double y0;

	double x1;
	double y1;

	double x;

	if (!PyArg_ParseTuple(args, "ddddd", &x0, &y0, &x1, &y1, &x)){
		return NULL;
	}

	double y = Linear_Interpolate(x0, y0, x1, y1, x);

	return PyFloat_FromDouble(y);
}

double Linear_Interpolate(double x0, double y0, double x1, double y1, double x){
	double y = y0 + (y1 - y0) * ((x - x0) / (x1 - x0));

	return y;
}

PyObject * Interpolate_Linear_3Points(PyObject * self, PyObject * args){
	double x0;
	double y0;
	double z0;

	double x1;
	double y1;
	double z1;

	double d;

	if (!PyArg_ParseTuple(args, "ddddddd", &x0, &y0, &z0, &x1, &y1, &z1, &d)){
		return NULL;
	}

	double * result;
	result = Linear_Interpolate_3Points(x0, y0, z0, x1, y1, z1, d);

	return Py_BuildValue("ddd", result[0], result[1], result[2]);
}

// http://math.stackexchange.com/questions/105400/linear-interpolation-in-3-dimensions
double * Linear_Interpolate_3Points(double x0, double y0, double z0, double x1, double y1, double z1, double d){
	double result[3];

	double v[3];
	v[0] = x1 - x0;
	v[1] = y1 - y0;
	v[2] = z1 - z0;

	double magnitude = sqrt(pow(v[0], 2) + pow(v[1], 2) + pow(v[2], 2));

	result[0] = x0 + (d / magnitude) * v[0];
	result[1] = y0 + (d / magnitude) * v[1];
	result[2] = z0 + (d / magnitude) * v[2];

	return result;
}
