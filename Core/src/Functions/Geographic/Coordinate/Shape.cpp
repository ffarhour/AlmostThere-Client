/*
	Shape.cpp

	Allows for a point to be determined in a shape

	SbSpider rajshorya@gmail.com
	*/

#include "stdafx.h"

#include "Shape.h"
// #include "Distance.h"
// #include "Cartesian.h"
#include <iostream>
static double Degrees_To_Radians(double degree){
	return degree / 180 * Py_MATH_PIl;
}

// Need to move later - currently, unable to get code from Cartesian file
void _ToCartesian(double lat, double lon, double cartesian[3]){
	// double const semi_Major = 6378.1370;
	// double const semi_Minor = 6356.7523;

	double const semi_Major = 6378.1370;
	double const semi_Minor = 6356.7523;
	double e = semi_Minor / semi_Major;
	double const e_squared = 1 - pow(semi_Minor / semi_Major, 2);
	double const e_quart = pow(e_squared, 2);

	lat = Degrees_To_Radians(lat);
	lon = Degrees_To_Radians(lon);

	double const N = pow(semi_Major, 2) / (sqrt(pow(semi_Major, 2) * pow(cos(lat), 2) + pow(semi_Minor, 2) * pow(sin(lat), 2)));

	cartesian[0] = N * cos(lat) * cos(lon);
	cartesian[1] = N * cos(lat) * sin(lon);
	cartesian[2] = (1 - e_squared) * N * sin(lat);

	std::cout << std::endl << "x : " << cartesian[0] << " y : " << cartesian[1] << " z : " << cartesian[2] << std::endl;
}

PyObject * InQuad(PyObject * self, PyObject * args){
	Point cornerA;
	Point cornerB;
	Point cornerC;
	Point cornerD;

	Point point;

	if (!PyArg_ParseTuple(args, "dddddddddd", &cornerA.lat, &cornerA.lon, &cornerB.lat, &cornerB.lon, &cornerC.lat, &cornerC.lon, &cornerD.lat, &cornerD.lon, &point.lat, &point.lon)){
		return NULL;
	}

	bool Is_InQuad = Point_In_Quadrilateral(cornerA, cornerB, cornerC, cornerD, point);

	if (Is_InQuad){
		return Py_True;
	}
	else {
		return Py_False;
	}
}

/*
	Using http://stackoverflow.com/a/16260220
	*/
static bool Point_In_Quadrilateral(Point cornerA, Point cornerB, Point cornerC, Point cornerD, Point point){
	// Area of quadrilateral - http://en.wikipedia.org/wiki/Brahmagupta's_formula
	struct Point_Cart{
		double x;
		double y;
		double z;
	};

	// The points.
	Point_Cart A, B, C, D, point_c;

	double A_TEMP[3];
	_ToCartesian(cornerA.lat, cornerA.lon, A_TEMP);
	A.x = A_TEMP[0];
	A.y = A_TEMP[1];
	A.z = A_TEMP[2];

	double B_TEMP[3];
	_ToCartesian(cornerB.lat, cornerB.lon, B_TEMP);
	B.x = B_TEMP[0];
	B.y = B_TEMP[1];
	B.z = B_TEMP[2];

	double C_TEMP[3];
	_ToCartesian(cornerC.lat, cornerC.lon, C_TEMP);
	C.x = C_TEMP[0];
	C.y = C_TEMP[1];
	C.z = C_TEMP[2];

	double D_TEMP[3];
	_ToCartesian(cornerD.lat, cornerD.lon, D_TEMP);
	D.x = D_TEMP[0];
	D.y = D_TEMP[1];
	D.z = D_TEMP[2];

	double POINT_TEMP[3];
	_ToCartesian(point.lat, point.lon, POINT_TEMP);
	point_c.x = POINT_TEMP[0];
	point_c.y = POINT_TEMP[1];
	point_c.z = POINT_TEMP[2];

	// Shouldn't be used beyond this
	// delete[] A_TEMP, B_TEMP, C_TEMP, D_TEMP, POINT_TEMP;

	/*
		Total area of quad calculated from here
		*/

	// The distances, as compared to the points.
	double a, b, c, d;

	a = sqrt(pow(B.x - A.x, 2) + pow(B.y - A.y, 2) + pow(B.z - A.z, 2));
	b = sqrt(pow(C.x - B.x, 2) + pow(C.y - B.y, 2) + pow(C.z - B.z, 2));
	c = sqrt(pow(D.x - C.x, 2) + pow(D.y - C.y, 2) + pow(D.z - C.z, 2));
	d = sqrt(pow(A.x - D.x, 2) + pow(A.y - D.y, 2) + pow(A.z - D.z, 2));

	double s = (a + b + c + d) / 2;

	std::cout << "a : " << a << " b : " << b << " c : " << c << " d : " << d << std::endl;

	// Angle between AB and DA
	double vecAB[3];
	vecAB[0] = B.x - A.x;
	vecAB[1] = B.y - A.y;
	vecAB[2] = B.z - A.z;

	double vecAD[3];
	vecAD[0] = D.x - A.x;
	vecAD[1] = D.y - A.y;
	vecAD[2] = D.z - A.z;

	// Using dotproduct calculation
	double dot_AB_AD = vecAB[0] * vecAD[0] + vecAB[1] * vecAD[1] + vecAB[2] * vecAD[2];

	// a is distance AB, d is distance AD
	double theta_A = acos(dot_AB_AD / (a * d));

	// Angle between CB and CD
	double vecCB[3];
	vecCB[0] = B.x - C.x;
	vecCB[1] = B.y - C.y;
	vecCB[2] = B.z - C.z;

	double vecCD[3];
	vecCD[0] = D.x - C.x;
	vecCD[1] = D.y - C.y;
	vecCD[2] = D.z - C.z;

	double dot_CB_CD = vecCB[0] * vecCD[0] + vecCB[1] * vecCD[1] + vecCB[2] * vecCD[2];

	double theta_C = acos(dot_CB_CD / (b * c));

	double theta = (theta_A + theta_C) / 2;

	// double area = sqrt((s - a) * (s - b) * (s - c) * (s - d) - a*b*c*d*pow(cos(theta), 2));
	double area = sqrt((s - a) * (s - b) * (s - c) * (s - d));

	/*
		Four triangles calculated here

		Area calculated using http://www.mathopenref.com/heronsformula.html
		*/

	// Distance from point to letter
	double point_to_A = sqrt(pow(point_c.x - A.x, 2) + pow(point_c.y - A.y, 2) + pow(point_c.z - A.z, 2));
	double point_to_B = sqrt(pow(point_c.x - B.x, 2) + pow(point_c.y - B.y, 2) + pow(point_c.z - B.z, 2));
	double point_to_C = sqrt(pow(point_c.x - C.x, 2) + pow(point_c.y - C.y, 2) + pow(point_c.z - C.z, 2));
	double point_to_D = sqrt(pow(point_c.x - D.x, 2) + pow(point_c.y - D.y, 2) + pow(point_c.z - D.z, 2));

	// Perimeter ABPOINT
	double p_triA = (point_to_A + a + point_to_B) / 2;

	// Area of triangle a
	double area_tri_A = sqrt(p_triA * (p_triA - point_to_A) * (p_triA - a) * (p_triA - point_to_B));

	std::cout << "Triangle A Area : " << area_tri_A << std::endl;

	// PERIMAETERS BCPOINT
	double p_triB = (point_to_B + b + point_to_C) / 2;

	// Area of triangle b
	double area_tri_B = sqrt(p_triB * (p_triB - point_to_B) * (p_triB - b) * (p_triB - point_to_C));

	std::cout << "Triangle B Area : " << area_tri_B << std::endl;

	// Perimeter CDPoint
	double p_triC = (point_to_C + c + point_to_D) / 2;

	// Area of triangle C
	double area_tri_C = sqrt(p_triC * (p_triC - point_to_C) * (p_triC - c) * (p_triC - point_to_D));

	std::cout << "Triangle C Area : " << area_tri_C << std::endl;

	// Perimeter of DAPoint
	double p_triD = (point_to_D + d + point_to_A) / 2;

	// Area of triangle D
	double area_tri_D = sqrt(p_triD * (p_triD - point_to_D) * (p_triD - d) * (p_triD - point_to_A));

	std::cout << "Triangle D Area : " << area_tri_D << std::endl;

	// Sum of areas of all triangles
	double area_of_triangles = area_tri_A + area_tri_B + area_tri_C + area_tri_D;

	std::cout << std::endl << "Area : " << area << std::endl;
	std::cout << "ARea of triangles : " << area_of_triangles << std::endl;

	if (area >= area_of_triangles){
		return true;
	}
	else {
		return false;
	}
}