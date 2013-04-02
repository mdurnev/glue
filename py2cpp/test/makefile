PYTHON_VERSION=3\.2
PYTHON_LIB=`ls /usr/lib/ | grep libpython$(PYTHON_VERSION).*\.so$$ | sed s:lib:: | sed s:.so::`

all: test

sample.py.hpp: sample.py
	PYTHONPATH=`pwd` ../py2cpp.py sample > sample.py.hpp
	cp ../python.hpp.in ./python.hpp
	sed -i s:##PYTHON_VERSION##:$(PYTHON_VERSION):g ./python.hpp

test: test.cpp sample.py.hpp
	g++ test.cpp -o test -l $(PYTHON_LIB)
	echo "#!/bin/sh" > run
	echo "PYTHONPATH=`pwd` ./test" >> run
	chmod +x run

.PHONY: clean
clean:
	rm -rf sample.py.hpp test run __pycache__ python.hpp
