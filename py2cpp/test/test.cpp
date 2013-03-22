#include "sample.py.hpp"

int main() {
    Py_Initialize();

    sample::__init__();

    printf("%s\n", (char*)sample::hello());

    printf("%d\n", (int)sample::number(25, 37));
    printf("%s\n", (char*)sample::number("25", "37"));
    printf("%f\n", (double)sample::number(25.1, 37.2));


    sample::__del__();

    Py_Finalize();
    return 0;
}


