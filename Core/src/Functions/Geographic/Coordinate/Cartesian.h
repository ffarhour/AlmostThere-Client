#ifndef CARTESIAN_H
#define CARTESIAN_H

#ifdef __cplusplus

extern "C" {
#endif

	// Python Functions
	PyObject * ToCartesian(PyObject * self, PyObject * args);
	PyObject * ToGeo(PyObject * self, PyObject * args);

#define _ToCartesian_NUM 0
#define _ToCartesian_RETURN void
#define _ToCartesian_PROTO (double lat, double lon, double cartesian[3])

#define _ToGeo_NUM 1
#define _ToGeo_RETURN void
#define _ToGeo_PROTO (double x, double y, double z, double geo[2])

#define CARTESIAN_API_pointers 2

#ifdef COORDINATE_CARTESIAN_MODULE

	static _ToCartesian_RETURN _ToCartesian _ToCartesian_PROTO;
	static _ToGeo_RETURN _ToGeo _ToGeo_PROTO;

#else

	static void ** CARTESIAN_API;

#define _ToCartesian \
	(*(_ToCartesian_RETURN(*)_ToCartesian_PROTO) CARTESIAN_API[_ToCartesian_NUM])

#define _ToGeo \
	(* (_ToGeo_RETURN(*)_ToGeo_PROTO) CARTESIAN_API[_ToGeo_NUM])

	static int
		import_Cartesian(void)
	{
		CARTESIAN_API = (void **)PyCapsule_Import("CARTESIAN._C_API", 0);
		return (CARTESIAN_API != NULL) ? 0 : -1;
	}

#endif /* COORDINATE_CARTESIAN_MODULE */

#ifdef __cplusplus
}
#endif

#endif /* !defined(CARTESIAN_H) */