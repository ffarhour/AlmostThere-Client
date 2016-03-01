#ifndef DISTANCE_H
#define DISTANCE_H

#ifdef __cplusplus

extern "C" {
#endif

	/* Header file for Distance */

	// Python Functions
	PyObject * Distance_LatLongs(PyObject * self, PyObject * args);
	PyObject * Angle_LatLongs_And_Vertical(PyObject * self, PyObject * args);

	/* C API functions */

	/*
		Functions:
		Calculate_Distance_Between_LatLongs
		Degrees_To_Radians
		Calculate_Angle_Between_LatLongs_And_Vertical
		*/

#define Calculate_Distance_Between_LatLongs_NUM 0
#define Calculate_Distance_Between_LatLongs_RETURN double
#define Calculate_Distance_Between_LatLongs_PROTO (double lat1, double long1, double lat2, double long2)

#define Degrees_To_Radians_NUM 1
#define Degrees_To_Radians_RETURN double
#define Degrees_To_Radians_PROTO (double degree)

#define Calculate_Angle_Between_LatLongs_And_Vertical_NUM 2
#define Calculate_Angle_Between_LatLongs_And_Vertical_RETURN double
#define Calculate_Angle_Between_LatLongs_And_Vertical_PROTO (double lat1, double long1, double lat2, double long2)

	/* Total number of C API pointers */
#define DISTANCE_API_pointers 3

#ifdef COORDINATE_DISTANCE_MODULE
	/* This section is used when compiling spammodule.c */

	static Calculate_Distance_Between_LatLongs_RETURN Calculate_Distance_Between_LatLongs Calculate_Distance_Between_LatLongs_PROTO;
	static Degrees_To_Radians_RETURN Degrees_To_Radians Degrees_To_Radians_PROTO;
	static Calculate_Angle_Between_LatLongs_And_Vertical_RETURN Calculate_Angle_Between_LatLongs_And_Vertical Calculate_Angle_Between_LatLongs_And_Vertical_PROTO;

#else
	/* This section is used in modules that use spammodule's API */

	static void **DISTANCE_API;

#define Calculate_Distance_Between_LatLongs \
 (*(Calculate_Distance_Between_LatLongs_RETURN (*)Calculate_Distance_Between_LatLongs_PROTO) DISTANCE_API[Calculate_Distance_Between_LatLongs_NUM])

#define Degrees_To_Radians \
 (*(Degrees_To_Radians_RETURN (*)Degrees_To_Radians_PROTO) DISTANCE_API[Degrees_To_Radians_NUM])

#define Calculate_Angle_Between_LatLongs_And_Vertical \
 (*(Calculate_Angle_Between_LatLongs_And_Vertical_RETURN (*)Calculate_Angle_Between_LatLongs_And_Vertical_PROTO) DISTANCE_API[Calculate_Angle_Between_LatLongs_And_Vertical_NUM])

	/* Return -1 on error, 0 on success.
	* PyCapsule_Import will set an exception if there's an error.
	*/
	static int
		import_Distance(void)
	{
		DISTANCE_API = (void **)PyCapsule_Import("DISTANCE._C_API", 0);
		return (DISTANCE_API != NULL) ? 0 : -1;
	}

#endif /* COORDINATE_DISTANCE_MODULE */

#ifdef __cplusplus
}
#endif

#endif /* !defined(DISTANCE_H) */