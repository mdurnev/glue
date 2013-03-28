/*
  Copyright 2013 Mikhail Durnev. Released under the GPLv3
*/

#ifndef PYTHON_HPP
#define PYTHON_HPP

#include <python3.2/Python.h>


// Python exceptions to be used with try-catch
class PyExcept {
protected:
    PyObject* pExcType;

public:
    PyExcept(PyObject* pType, bool warn = true) {
        pExcType = pType;

        if (pExcType != NULL) {

            if (warn) {
                PyErr_Print();
            }

            PyErr_Clear();
        }
    }

    bool matches(PyObject* exc) {
        return (bool)PyErr_GivenExceptionMatches(pExcType, exc);
    }
};


// PyObject wrapper to provide type casting
class PyObj {
public:
    PyObject* pValue;
    PyObject* pBytes;

    PyObj() : pValue(NULL), pBytes(NULL) {
    }

    PyObj(PyObject* pObj) : pValue(pObj), pBytes(NULL) {
    }

    ~PyObj() {
        Py_XDECREF(pBytes);
        Py_XDECREF(pValue);
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
            Py_CLEAR(pBytes);
            pBytes = PyUnicode_AsUTF8String(pValue);

            if (pBytes != NULL) {
                return (const char*)PyBytes_AsString(pBytes);
            }
        }
        return NULL;
    }
};

#endif
