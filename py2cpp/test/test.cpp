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

    int i;
    PyObj pylist = sample::List();
    printf("[ ");
    for (i = 0; i < (int)pylist.len(); i++) {
        printf("%d ", (int)pylist[i]);
    }
    printf("]\n");

    PyObj pytuple = sample::Tuple();
    printf("( ");
    for (i = 0; i < (int)pytuple.len(); i++) {
        printf("%d ", (int)pytuple[i]);
    }
    printf(")\n");

    std::deque<PyObj> dq = pylist.sequence();
    printf("deque ( ");
    for (i = 0; i < (int)dq.size(); i++) {
        printf("%d ", (int)dq[i]);
    }
    printf(")\n");


    pylist = sample::List1();
    std::deque<int> dqi = pylist.int_sequence();
    std::deque<double> dqd = pylist.double_sequence();
    std::deque<const char*> dqs = pylist.string_sequence();

    printf("deque<int> ( ");
    for (i = 0; i < (int)dqi.size(); i++) {
        printf("%d ", dqi[i]);
    }
    printf(")\n");

    printf("deque<double> ( ");
    for (i = 0; i < (int)dqd.size(); i++) {
        printf("%f ", dqd[i]);
    }
    printf(")\n");

    printf("deque<const char*> ( ");
    for (i = 0; i < (int)dqs.size(); i++) {
        printf("\"%s\" ", dqs[i]);
    }
    printf(")\n");


    std::deque<int>  listi(3);
    listi[0] = 9;
    listi[1] = 8;
    listi[2] = 7;
    PyObj pli = PyObj(listi);
    sample::show(pli);

    std::deque<double>  listd(3);
    listd[0] = 9.7;
    listd[1] = 8.8;
    listd[2] = 7.9;
    PyObj pld = PyObj(listd);
    sample::show(pld);

    std::deque<const char*>  lists(3);
    lists[0] = "I";
    lists[1] = "love";
    lists[2] = "you";
    PyObj pls = PyObj(lists);
    sample::show(pls);

    sample::__del__();

    Py_Finalize();
    return 0;
}


