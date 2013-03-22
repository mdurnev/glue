#include "sample.py.hpp"

int main() {
    Py_Initialize();

    sample::__init__();

    printf("%s\n", (char*)sample::hello());

    printf("%d\n", (int)sample::Sum(25, 37));
    printf("%s\n", (char*)sample::Sum("25", "37"));
    printf("%f\n", (double)sample::Sum(25.1, 37.2));
    printf("%f\n", (double)sample::Sum(25, 37.5));

    sample::Test test;
    printf("%s\n", (char*)test.hello());
    printf("%d\n", (int)test.Sum(25, 37));
    printf("%f\n", (double)test.Sum(1.3, 2.1));

    sample::Test1 test1(-1);
    printf("%s\n", (char*)test1.hello());
    printf("%d\n", (int)test1.Sum(25, 37));

    sample::__del__();

    Py_Finalize();
    return 0;
}


