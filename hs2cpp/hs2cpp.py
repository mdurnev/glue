#!/usr/bin/env python3

# Copyright 2013 Mikhail Durnev. Released under the GPLv3

import sys
import getopt
import os
import errno
import re

usage = """Usage: hs2cpp <Haskell file name>
"""

# Haskell type : [Haskell CType, C type, conversion function]
type_hs2cpp = {"Int" : ["CInt", "int", "fromIntegral"],
               "Float" : ["CFloat", "float", "realToFrac"],
               "Double" : ["CDouble", "double", "realToFrac"]
}

#==============================================================================
#                          E N T R Y   P O I N T
#==============================================================================
def main():
    global usage
    global type_hs2cpp

    # get command line options and arguments
    try:
        opts,args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    for o, a in opts:
        if o in ("-h", "--help"):
            print(usage)
            sys.exit(0)

    # get file name
    try:
        file_name = args[0]
    except IndexError:
        print(usage)
        sys.exit(2)

    # output file names
    hs_file_name = file_name + ".conv.hs"
    hpp_file_name = file_name + ".hpp"

    # read the file
    file = open(file_name, 'r')
    if file == None:
        print("Cannot open %s" % file_name)
        sys.exit(1)
    hs_program = file.readlines()
    file.close()

    # additional lines for C export
    hs_program_tail = []

    # Haskell module name
    hs_module_name = "N/D"
    hs_module_coded = "N/D"

    # Haskell module name translated to function prefix
    module_name = "N/D"

    # Exported Haskell functions
    exported_funcs = []

    for line in hs_program:
        # get module name
        m = re.match(r"\s*module\s*(\S+)\s*where\s*\Z", line)
        if m != None:
            hs_module_name = m.group(1)
            hs_module_coded = hs_module_name.replace("Z", "%").replace("z", "*")
            hs_module_coded = hs_module_coded.replace(".", "zi").replace("_", "zu")
            hs_module_coded = hs_module_coded.replace("%", "ZZ").replace("*", "zz")
            module_name = hs_module_coded[:1].lower() + hs_module_coded[1:]
            continue

        # find functions
        m = re.match(r"\s*(\S+)\s*::\s*([\S \t]+)", line)
        if m != None:
            func_name = m.group(1)

            # get function type as a list of types T1->T2->T3->...
            func_type = re.split(r"\s*(?:->){1}\s*", m.group(2).rstrip(" \t"))
            if func_type != None and func_type != []:

                # verify that all types can be converted to corresponding C types
                hs_ctypes = []
                ctypes = []
                convs = []

                for type in func_type:
                    try:
                        hsct,ct,conv = type_hs2cpp[type]
                        hs_ctypes.append(hsct)
                        ctypes.append(ct)
                        convs.append(conv)
                    except KeyError:
                        pass

                if len(func_type) == len(hs_ctypes):
                    # Exported function type
                    ln = "\n%s_%s :: " % (module_name, func_name)
                    for i in range(len(hs_ctypes)):
                        endl = " -> " if i != len(hs_ctypes) - 1 else "\n"
                        ln += hs_ctypes[i] + endl
                    hs_program_tail.append(ln)

                    # Exported function definition
                    ln = "%s_%s " % (module_name, func_name)
                    for i in range(len(convs) - 1):
                        ln += "x%s " % str(i)
                    ln += "= %s ( %s " % (convs[-1], func_name)
                    for i in range(len(convs) - 1):
                        ln += "(%s x%s) " % (convs[i], str(i))
                    ln += ")\n"
                    hs_program_tail.append(ln)

                    # Export command
                    ln = "foreign export ccall %s_%s :: " % (module_name, func_name)
                    for i in range(len(hs_ctypes)):
                        endl = " -> " if i != len(hs_ctypes) - 1 else "\n"
                        ln += hs_ctypes[i] + endl
                    hs_program_tail.append(ln)

                    exported_funcs.append(("%s_%s" % (module_name, func_name), func_name, ctypes))


    # New Haskell program with C export definitions
    file = open(hs_file_name, 'w')
    if file == None:
        print("Cannot open %s" % hs_file_name)
        sys.exit(1)

    file.write("module %s where\n\n" % hs_module_name)
    file.write("\nimport Foreign.C.Types\n\n")

    for line in hs_program:
        m = re.match(r"\s*module\s*(\S+)\s*where\s*\Z", line)
        if m == None:
            file.write(line)

    file.write("\n\n")

    for line in hs_program_tail:
        file.write(line)

    file.close()


    # C++ wrapper
    file = open(hpp_file_name, 'w')
    if file == None:
        print("Cannot open %s" % hs_file_name)
        sys.exit(1)

    file.write("#ifndef %s_H\n" % module_name.upper())
    file.write("#define %s_H\n\n" % module_name.upper())

    file.write('#include "%s"\n\n' % (hs_file_name[:-3] + "_stub.h"))

    file.write('extern "C" void __stginit_%s(void);\n\n' % hs_module_coded)

    file.write("namespace %s {\n\n" % module_name)

    file.write("void __init__(int argc, char** argv) {\n"
               "    hs_init(&argc, &argv);\n"
               "    hs_add_root(__stginit_%s);\n}\n\n" % hs_module_coded)

    file.write("void __del__() {\n"
               "    hs_exit();\n}\n\n")

    for f in exported_funcs:
        c_name, cpp_name, types = f
        file.write("%s %s(" % (types[-1], cpp_name))
        for x in range(len(types) - 1):
            file.write("%s x%d%s" % (types[x], x, ", " if x < len(types) - 2 else ""))
        file.write(") {\n")

        file.write("    return %s(" % c_name)
        for x in range(len(types) - 1):
            file.write("x%d%s" % (x, ", " if x < len(types) - 2 else ""))
        file.write(");\n}\n\n")

    file.write("} // namespace\n\n")
    file.write("#endif\n")

    file.close()



if __name__ == "__main__":
    main()
