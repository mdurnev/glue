#ifndef SAMPLE_PY
#define SAMPLE_PY
#include "python.hpp"

namespace sample {

PyObject* hello_obj = NULL;

PyObj hello() {
     return PyObj(PyObject_CallFunction(hello_obj, NULL));
}

PyObject* number_obj = NULL;

PyObj number(int n, int m) {
     return PyObj(PyObject_CallFunction(number_obj, "ii" ,n, m));
}

PyObj number(double n, int m) {
     return PyObj(PyObject_CallFunction(number_obj, "fi" ,n, m));
}

PyObj number(char* n, int m) {
     return PyObj(PyObject_CallFunction(number_obj, "si" ,n, m));
}

PyObj number(int n, double m) {
     return PyObj(PyObject_CallFunction(number_obj, "if" ,n, m));
}

PyObj number(double n, double m) {
     return PyObj(PyObject_CallFunction(number_obj, "ff" ,n, m));
}

PyObj number(char* n, double m) {
     return PyObj(PyObject_CallFunction(number_obj, "sf" ,n, m));
}

PyObj number(int n, char* m) {
     return PyObj(PyObject_CallFunction(number_obj, "is" ,n, m));
}

PyObj number(double n, char* m) {
     return PyObj(PyObject_CallFunction(number_obj, "fs" ,n, m));
}

PyObj number(char* n, char* m) {
     return PyObj(PyObject_CallFunction(number_obj, "ss" ,n, m));
}

bool __init__() {
    PyObject* pModule = NULL;
    PyObject* pName = PyUnicode_FromString("sample");

    if (pName == NULL) {
        pModule = NULL;
        return false;
    }
    else {
        pModule = PyImport_Import(pName);
        Py_DECREF(pName);

        hello_obj = PyObject_GetAttrString(pModule, "hello");
        number_obj = PyObject_GetAttrString(pModule, "number");

        Py_DECREF(pModule);
    }
    return true;
}

void __del__() {
    if (hello_obj) Py_DECREF(hello_obj);
    if (number_obj) Py_DECREF(number_obj);
}

}
#endif
