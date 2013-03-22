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

    PyObj() : pValue(NULL) {}

    PyObj(PyObject* pObj) : pValue(pObj) {}

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

    operator char*() {
        if (pValue && Py_TYPE(pValue) == &PyUnicode_Type) {
            //wchar_t* buf = new wchar_t[4096];
            //Py_ssize_t sz = PyUnicode_AsWideChar(pValue, buf, 4096);
            return _PyUnicode_AsString(pValue);
        }
        return NULL;
    }
};

#endif
