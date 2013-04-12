#include <stdio.h>
#include "sample.hs.hpp"

int main(int argc, char** argv) {

    sampleziModule::__init__(argc, argv);

    int i;
    for (i = 1; i <= 20; i++) {
        printf("%d ", sampleziModule::fibonacci(i));
    }
    printf("\n");

    sampleziModule::__del__();

    return 0;
}
