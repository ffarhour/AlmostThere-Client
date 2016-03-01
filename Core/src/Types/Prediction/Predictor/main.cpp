/*
	Main.cpp

	Handles anything to do with module initialization and such.
	*/

#include "stdafx.h"

typedef struct {
	PyObject_HEAD
		/* Type-specific fields go here. */
} Predictor_Predictor_Object;

static PyTypeObject Predictor_Predictor_Type = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"Predictor.Predictor",             /* tp_name */
	sizeof(Predictor_Predictor_Object), /* tp_basicsize */
	0,                         /* tp_itemsize */
	0,                         /* tp_dealloc */
	0,                         /* tp_print */
	0,                         /* tp_getattr */
	0,                         /* tp_setattr */
	0,                         /* tp_reserved */
	0,                         /* tp_repr */
	0,                         /* tp_as_number */
	0,                         /* tp_as_sequence */
	0,                         /* tp_as_mapping */
	0,                         /* tp_hash  */
	0,                         /* tp_call */
	0,                         /* tp_str */
	0,                         /* tp_getattro */
	0,                         /* tp_setattro */
	0,                         /* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,        /* tp_flags */
	"Predictor Objects",           /* tp_doc */
};

static PyModuleDef PredictorModule = {
	PyModuleDef_HEAD_INIT,
	"Predictor",
	"The Predictor module, containing code for the prediction of arrival time.",
	-1,
	NULL, NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC
PyInit__Predictor(void)
{
	PyObject* m;

	Predictor_Predictor_Type.tp_new = PyType_GenericNew;
	if (PyType_Ready(&Predictor_Predictor_Type) < 0)
		return NULL;

	m = PyModule_Create(&PredictorModule);
	if (m == NULL)
		return NULL;

	Py_INCREF(&Predictor_Predictor_Type);
	PyModule_AddObject(m, "Predictor", (PyObject *)&Predictor_Predictor_Type);
	return m;
}