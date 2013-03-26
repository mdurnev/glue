/*
  Copyright 2013 Mikhail Durnev. Released under the GPLv3
*/

#ifndef PYTHON_HPP
#define PYTHON_HPP

#include <stdarg.h>
#include <python3.2/Python.h>

class PyObj {
public:
    PyObject* pValue;

    PyObj() : pValue(NULL) {
    }

    PyObj(PyObject* pObj) : pValue(pObj) {
    }

    ~PyObj() {
        if (pValue) Py_DECREF(pValue);
    }

    operator int() {
        if (pValue && Py_TYPE(pValue) == &PyLong_Type)
            return PyLong_AsLong(pValue);
        return 0;
    }

    operator double() {
        if (pValue && Py_TYPE(pValue) == &PyFloat_Type)
            return PyFloat_AsDouble(pValue);
        return 0;
    }

    operator const char*() {
        if (pValue && Py_TYPE(pValue) == &PyUnicode_Type) {
            PyObject* pBytes = PyUnicode_AsUTF8String(pValue);

            if (pBytes != NULL) {
                return (const char*)PyBytes_AsString(pBytes);
            }
        }
        return NULL;
    }
};

#endif
