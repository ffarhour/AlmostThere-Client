#ifndef INTERPOLATION_H
#define INTERPOLATION_H

#ifdef __cplusplus
extern "C"{
#endif

	// Python Functions
	PyObject * Interpolate_Linear(PyObject * self, PyObject * args);
	PyObject * Interpolate_Linear_3Points(PyObject * self, PyObject * args);

	double * Linear_Interpolate_3Points(double x0, double y0, double z0, double x1, double y1, double z1, double d);

#define Linear_Interpolate_NUM 0
#define Linear_Interpolate_RETURN double
#define Linear_Interpolate_PROTO (double x0, double y0, double x1, double y1, double x)

#define INTERPOLATION_API_pointers 1

#ifdef	INTERPOLATION_INTERPOLATION_MODULE

	static Linear_Interpolate_RETURN Linear_Interpolate Linear_Interpolate_PROTO;

#else

	static void ** INTERPOLATION_API;

#define Linear_Interpolate \
	(* (Linear_Interpolate_RETURN (*) Linear_Interpolate_PROTO ) INTERPOLATION_API[Linear_Interpolate_NUM])

	static int import_Interpolation(void){
		INTERPOLATION_API = (void **)PyCapsule_Import("INTERPOLATION._C_API", 0);
		return (INTERPOLATION_API != NULL) ? 0 : -1;
	}

#endif /* INTERPOLATION_INTERPOLATION_MODULE */

#ifdef __cplusplus
}
#endif

#endif /* !defined(INTERPOLATION_H) */