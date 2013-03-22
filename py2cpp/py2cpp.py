#!/usr/bin/env python3

import inspect

def get_argspec(func):
    arg_spec = inspect.getargspec(func)
    arg_list = arg_spec.args
    #if arg_spec.varargs != None:
    #    arg_list.append("...")
    return arg_list


def types(n):
    supported = ["int", "double", "char*"]
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


formats = {"int"    : "i",
           "double" : "f",
           "char*"  : "s" }


def main():
    # get module name
    module_name = input()

    # load the module
    module = __import__(module_name)

    functions = []

    print("#ifndef %s_PY" % module_name.upper())
    print("#define %s_PY" % module_name.upper())
    print("#include \"python.hpp\"")
    print("\nnamespace %s {" % module_name) # begin namespace

    module_symbols = dir(module)

    # get all classes and functions
    for symbol in module_symbols:
        obj = getattr(module, symbol)

        if inspect.isfunction(obj):
            print("\nPyObject* %s_obj = NULL;" % symbol)
            functions.append(symbol)

            # get number of arguments
            args = get_argspec(obj)

            type_list = types(len(args))
            for ts in type_list:
                format = ""
                arguments = ""
                print("\nPyObj %s(" % symbol, end = '')

                for a,t in zip(args, ts):
                    global formats
                    format += formats[t]

                    if a != args[-1]:
                        arguments += a + ", "
                        print(t, a, end = ", ")
                    else:
                        arguments += a
                        print(t, a, end = '')

                if format == "":
                    format = "NULL"
                else:
                    format = "\"" + format + "\""
                    arguments = " ," + arguments

                print(") {")
                #print('    return call_python(%s_obj, %s%s);' % (symbol, format, arguments))
                print('     return PyObj(PyObject_CallFunction(%s_obj, %s%s));' % (symbol, format, arguments))
                print("}")


        if inspect.isclass(obj):
            # get methods
            class_symbols = dir(obj)

            for sym in class_symbols:
                m = getattr(obj, sym)

                if inspect.isfunction(m):
                    # get number of arguments
                    #print("%s.%s(%s)" % (symbol, sym, str(get_argspec(m))[1:-1]))
                    pass

    print("\nbool __init__() {")
    print("    PyObject* pModule = NULL;")
    print('    PyObject* pName = PyUnicode_FromString("%s");' % module_name)
    print("""
    if (pName == NULL) {
        pModule = NULL;
        return false;
    }
    else {
        pModule = PyImport_Import(pName);
        Py_DECREF(pName);
""")

    for fn in functions:
         print('        %s_obj = PyObject_GetAttrString(pModule, "%s");' % (fn, fn))

    print("""
        Py_DECREF(pModule);
    }
    return true;
}

void __del__() {""")

    for fn in functions:
         print("    if (%s_obj) Py_DECREF(%s_obj);" % (fn,fn))

    print("}")


    print("\n}") # end namespace
    print("#endif")




if __name__ == "__main__":
    main()
