#include <stdio.h>
#include "sample.hs.hpp"

int main(int argc, char** argv) {

    sampleModule::__init__(argc, argv);

    int i;
    for (i = 1; i <= 20; i++) {
        printf("%d ", sampleModule::fibonacci(i));
    }
    printf("\n");

    sampleModule::__del__();

    return 0;
}
