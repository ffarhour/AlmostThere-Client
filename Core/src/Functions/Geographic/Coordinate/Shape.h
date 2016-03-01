#ifndef SHAPE_H
#define SHAPE_H

#ifdef __cplusplus

extern "C" {
#endif

	struct Point{
		double lat;
		double lon;
	};

	PyObject * InQuad(PyObject * self, PyObject * args);

	static bool Point_In_Quadrilateral(Point cornerA, Point cornerB, Point cornerC, Point cornerD, Point point);

#ifdef __cplusplus
}
#endif

#endif /* !(defined(SHAPE_H)) */