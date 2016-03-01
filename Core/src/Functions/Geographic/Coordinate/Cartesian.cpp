/*
	Cartesian.cpp
	Allows for the conversion of latitude and longitude points into cartesian coordinates

	Spider rajshorya@gmail.com
	*/

#include "stdafx.h"

#define COORDINATE_CARTESIAN_MODULE
#include "Cartesian.h"

#include <iostream>
using namespace std;

double const semi_Major = 6378.1370;
double const semi_Minor = 6356.7523;
double e = semi_Minor / semi_Major;
double const e_squared = 1 - pow(semi_Minor, 2) / pow(semi_Major, 2);
double const e_quart = pow(e_squared, 2);

static double Degrees_To_Radians(double degree){
	return degree / 180 * Py_MATH_PIl;
}

/*
	Using http://stackoverflow.com/questions/1185408/converting-from-longitude-latitude-to-cartesian-coordinates

	http://www.iag-aig.org/attach/989c8e501d9c5b5e2736955baf2632f5/V60N2_5FT.pdf
	*/
PyObject * ToCartesian(PyObject * self, PyObject * args){
	double lat1;
	double long1;

	if (!PyArg_ParseTuple(args, "dd", &lat1, &long1)){
		return NULL;
	}

	double cartesian[3];
	_ToCartesian(lat1, long1, cartesian);

	return Py_BuildValue("ddd", cartesian[0], cartesian[1], cartesian[2]);
}

static void _ToCartesian(double lat, double lon, double cartesian[3]){
	// double const semi_Major = 6378.1370;
	// double const semi_Minor = 6356.7523;

	lat = Degrees_To_Radians(lat);
	lon = Degrees_To_Radians(lon);

	// double const N = pow(semi_Major, 2) / (sqrt(pow(semi_Major, 2) * pow(cos(lat), 2) + pow(semi_Minor, 2) * pow(sin(lat), 2)));
	double const N = semi_Major / sqrt(1 - e_squared * pow(sin(lat), 2));

	cartesian[0] = N * cos(lat) * cos(lon);
	cartesian[1] = N * cos(lat) * sin(lon);
	cartesian[2] = (1 - e_squared) * N * sin(lat);
}

// http://stackoverflow.com/questions/1185408/converting-from-longitude-latitude-to-cartesian-coordinates
//
// http://www.iag-aig.org/attach/989c8e501d9c5b5e2736955baf2632f5/V60N2_5FT.pdf
PyObject * ToGeo(PyObject * self, PyObject * args){
	double x;
	double y;
	double z;

	if (!PyArg_ParseTuple(args, "ddd", &x, &y, &z)){
		return NULL;
	}

	double geo[2];

	_ToGeo(x, y, z, geo);

	return Py_BuildValue("dd", geo[0], geo[1]);
}

static void _ToGeo(double x, double y, double z, double geo[2]){
	// double const Radius = 6371;

	// Latitude
	// http://en.wikipedia.org/wiki/Geodetic_datum (bowring)

	// The value calculated

	double k = 0;

	// The one used in the iteration
	double k_prev = NULL;

	const double p = sqrt(pow(x, 2) + pow(y, 2));

	do{
		k_prev = k;

		double c = pow((pow(p, 2) + (1 - e_squared) * pow(z, 2) * pow(k_prev, 2)), 1.5);
		c /= (semi_Major * e_squared);

		k = (c + (1 - e_squared) * pow(z, 2) * pow(k_prev, 3)) / (c - pow(p, 2));
	} while (k_prev - k > 0.00000000000001);

	double latitude = atan2(k * z, p);

	// Ferrari's solution - good but not accurate enough
	/*
	double p = sqrt(pow(x, 2) + pow(y, 2));
	double l = ((1 - e_squared) * pow(z, 2)) / pow(semi_Major, 2);
	double rho = ((pow(p, 2) / pow(semi_Major, 2)) + l - e_quart) / 6;
	double s = (e_quart * l * pow(p, 2)) / (4 * pow(semi_Major, 2));
	double t = pow((pow(rho, 3) + s + sqrt(s * (s + 2 * pow(rho, 3)))), 1 / 3);
	double u = rho + t + (pow(rho, 2) / t);
	double v = sqrt(pow(u, 2) + e_quart * l);
	double w = (e_squared * (u + v - l)) / (2 * v);
	double k = 1 + (e_squared * (sqrt(u + v + pow(w, 2)) + w)) / (u + v);
	double latitude = atan2(k * z, p); */

	// Iteration
	/*
	double p = sqrt(pow(x, 2) + pow(y, 2));

	double k_prev = 0;
	double k = pow((1 - e_squared), -1);

	while (abs(k - k_prev) > 0.000000001){
	k_prev = k;

	double c = pow((pow(p, 2) + (1 - e_squared) * pow(z, 2) * pow(k_prev, 2)), 3 / 2) / (semi_Major * e_squared);

	k = 1 + (pow(p, 2) + (1 - e_squared) * pow(z, 2) * pow(k_prev, 3)) / (c - pow(p, 2));
	}

	std::cout << "K : " << k;
	double latitude = atan2((abs(k) * z), p);
	std::cout << "Lat " << latitude << std::endl; */

	/*
	// Fast Bowring http://www.iag-aig.org/attach/989c8e501d9c5b5e2736955baf2632f5/V60N2_5FT.pdf
	double e_ = sqrt(1 - e_squared);
	double c = semi_Major * e_squared;
	double z_ = e_ * z;
	double pg = sqrt(pow(x, 2) + pow(y, 2));

	double T_prev = 0;
	double T_current = (z / e_ * pg);

	// Newton iteration
	while (abs(T_current - T_prev) > 0.1){
	T_prev = T_current;

	double C = 1 / (sqrt(1 + T_prev));
	double S = C * T_prev;

	double num = z_ + c * pow(S, 3);
	double den = pg - c * pow(C, 3);

	T_current = num / den;
	}

	double latitude = atan2(T_current, e_); */

	/* Trying to use Fukushima, but error in t
	double c = semi_Major * e_squared;
	double z_ = (semi_Minor / semi_Major) * z;
	double v = 2 * (z_ + c);
	double u = 2 * (z_ - c);
	double pg = sqrt(pow(x, 2) + pow(y, 2));

	double t = (pg - c + z_) / (pg - c + 2 * z_);

	double latitude = atan2(semi_Major * (1 - pow(t, 2)), 2 * semi_Minor * t); */

	geo[0] = (latitude / Py_MATH_PIl) * 180;

	// std::cout << "X : " << x << "Y : " << y << "Z : " << z;

	// Longitude, Vanicek and Krakiwsky (1982)
	geo[1] = (2 * atan2(y, (x + sqrt(pow(x, 2) + pow(y, 2))))) / Py_MATH_PIl * 180;
}