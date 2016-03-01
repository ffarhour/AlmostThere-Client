#pragma once

#ifndef STDAFX_H
#define STDAFX_H

#ifdef _DEBUG
#define DEBUG_WAS_DEFINED
#undef _DEBUG
#endif

#include <Python.h>

#ifdef DEBUG_WAS_DEFINED
#define _DEBUG 1
#undef DEBUG_WAS_DEFINED
#endif

#include <math.h>

#endif