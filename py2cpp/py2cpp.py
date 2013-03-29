#!/usr/bin/env python3

# Copyright 2013 Mikhail Durnev. Released under the GPLv3

import inspect
import sys
import getopt
import os
import errno

usage = """Usage: py2cpp <python module name>
"""

#==============================================================================
# PyObject_CallFunction() requires a format string where 
# parameter types are coded.
# This variable helps do type encoding
#==============================================================================
formats = {"int"    : "i",
           "double" : "f",
           "const char*"  : "s" }

#==============================================================================
# Retrieves a list of function parameters (arguments)
# Variable parameter list and keywords parameters are ignored
#==============================================================================
def get_argspec(func):
    arg_spec = inspect.getargspec(func)
    return arg_spec.args


#==============================================================================
# Generates all combinations of function parameter types
# E.g. 'def func(x, y):' is translated in
# 'PyObj func(int x, int y) {'
# 'PyObj func(double x, int y) {'
# 'PyObj func(char* x, int y) {'
# 'PyObj func(int x, double y) {'
# 'PyObj func(double x, double y) {'
# 'PyObj func(char* x, double y) {'
# 'PyObj func(int x, char* y) {'
# 'PyObj func(double x, char* y) {'
# 'PyObj func(char* x, char* y) {'
#==============================================================================
def types(n):
    supported = ["int", "double", "const char*"]
    result = [[supported[0] for x in range(n)]]

    idx = [0 for x in range(n)]
    num = len(supported) - 1

    while idx != [num for x in range(n)]:
        for i in range(n):
            idx[i] += 1
            if idx[i] > num:
                idx[i] = 0
            else:
                break
        result.append([supported[x] for x in idx])
    
    return result


#==============================================================================
# Generates all C++ polymorphic function definitions
# for the python function
#==============================================================================
def definitions(func_obj, func_name, is_method = False, is_init = False):
    args = get_argspec(func_obj)

    # remove self for class methods
    if is_method and len(args) > 0:
        args = args[1:]

    type_list = types(len(args))
    for ts in type_list:
        format = ""
        arguments = ""

        if is_method:
            if is_init:
                print("\n    %s(" % func_name, end = '')
            else:
                print("\n    PyObj %s(" % func_name, end = '')
        else:
            print("\nPyObj %s(" % func_name, end = '')

        # generate C++ function parameter list
        for a,t in zip(args, ts):
            global formats
            format += formats[t]

            if a != args[-1]:
                arguments += a + ", "
                print(t, a, end = ", ")
            else:
                arguments += a
                print(t, a, end = '')

        # generate C++ function body
        if format == "":
            format = "NULL"
        else:
            format = "(char*)\"" + format + "\""
            arguments = " ," + arguments

        print(") {")

        if is_method:
            if is_init:
                print('        object = PyObject_CallFunction(class_obj, %s%s);' % (format, arguments))
                print('        if (object == NULL) throw PyExcept(PyErr_Occurred());')
            else:
                print('        PyObj res = PyObj(PyObject_CallMethod(object, (char*)"%s", %s%s));' % (func_name, format, arguments))
                print('        if (res.type() == NULL) throw PyExcept(PyErr_Occurred());')
                print('        return res;')
            print("    }")
        else:
            print('    PyObj res = PyObj(PyObject_CallFunction(%s_obj, %s%s));' % (func_name, format, arguments))
            print('    if (res.type() == NULL) throw PyExcept(PyErr_Occurred());')
            print('    return res;')
            print("}")


#==============================================================================
# Generates class definition
#==============================================================================
def define_class(class_obj, class_name):
    print('\nclass %s {' % class_name)
    print('    static PyObject* class_obj;\n'
          '    PyObject* object;\n\n'
          'public:')

    # destructor
    print('    ~%s() {' % class_name)
    print('        Py_XDECREF(object);\n'
          '    }\n')

    class_symbols = dir(class_obj)

    for symbol in class_symbols:
        member = getattr(class_obj, symbol)

        if symbol == "__init__":
            definitions(member, class_name, True, True)
        elif inspect.isfunction(member):
            definitions(member, symbol, True)

    print('\n    friend bool __init__();\n'
          '    friend void __del__();')
    print('}; // class %s\n' % class_name)
    print('PyObject* %s::class_obj = NULL;' % class_name)


#==============================================================================
#                          E N T R Y   P O I N T
#==============================================================================
def main():
    # get command line options and arguments
    try:
        opts,args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    for o, a in opts:
        if o in ("-h", "--help"):
            global usage
            print(usage)
            sys.exit(0)

    # get module name
    module_name = args[0]

    # load the module
    module = __import__(module_name)

    functions = []
    classes = []

    print("#ifndef %s_PY" % module_name.upper())
    print("#define %s_PY" % module_name.upper())
    print('\n#include "python.hpp"')
    print("\nnamespace %s {\n" % module_name) # begin namespace

    module_symbols = dir(module)

    # get all classes and functions
    for symbol in module_symbols:
        obj = getattr(module, symbol)

        # check if it is a function
        if inspect.isfunction(obj):
            print("\nPyObject* %s_obj = NULL;" % symbol)
            functions.append(symbol)

            definitions(obj, symbol)

        # check if it is a class
        if inspect.isclass(obj):
            classes.append(symbol)

            define_class(obj, symbol)

    print("\nvoid __del__() {")

    for fn in functions:
         print("    Py_CLEAR(%s_obj);" % fn)

    for cl in classes:
         print("    Py_CLEAR(%s::class_obj);" % cl)

    print("}\n")
    print("bool __init__() {\n"
          "    PyObject* pModule = NULL;")
    print('    PyObject* pName = PyUnicode_FromString("%s");' % module_name)
    print("\n"
          "    if (pName == NULL) {\n"
          "        return false;\n"
          "    }\n"
          "    else {\n"
          "        pModule = PyImport_Import(pName);\n"
          "        Py_DECREF(pName);\n\n"
          "        if (pModule == NULL) {\n"
          "            return false;\n"
          "        }\n")

    for fn in functions:
         print('        %s_obj = PyObject_GetAttrString(pModule, "%s");' % (fn, fn))

    for cl in classes:
         print('        %s::class_obj = PyObject_GetAttrString(pModule, "%s");' % (cl, cl))

    print("\n"
          "        Py_DECREF(pModule);\n\n"
          "        if (false")

    for fn in functions:
        print('            || %s_obj == NULL' % fn)

    for cl in classes:
        print('            || %s::class_obj == NULL' % cl)

    print("           ) {\n"
          "            __del__();\n"
          "            return false;\n"
          "        }\n"
          "    }\n"
          "    return true;\n"
          "}")

    print("\n} // namespace %s" % module_name) # end namespace
    print("#endif // %s_PY" % module_name.upper())




if __name__ == "__main__":
    main()
