#include "sample.py.hpp"

int main() {
    Py_Initialize();

    sample::__init__();

    printf("%s\n", (const char*)sample::hello());

    printf("%d\n", (int)sample::Sum(25, 37));
    printf("%s\n", (const char*)sample::Sum("25", "37"));
    printf("%f\n", (double)sample::Sum(25.1, 37.2));
    printf("%f\n", (double)sample::Sum(25, 37.5));

    sample::Test test;
    printf("%s\n", (const char*)test.hello());
    printf("%d\n", (int)test.Sum(25, 37));
    printf("%f\n", (double)test.Sum(1.3, 2.1));

    sample::Test1 test1(-1);
    printf("%s\n", (const char*)test1.hello());
    printf("%d\n", (int)test1.Sum(25, 37));

    try {
        sample::Sum(25, "37");
    }
    catch (PyExcept exc) {
        if (exc.matches(PyExc_TypeError)) {
            printf("TypeError was caught\n");
        }
    }

    try {
        sample::Test t;
        t.Sum(25, "37");
    }
    catch (PyExcept exc) {
    }

    sample::__del__();

    Py_Finalize();
    return 0;
}


