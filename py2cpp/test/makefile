all: test

sample.py.hpp: sample.py
	PYTHONPATH=`pwd` ../py2cpp.py sample > sample.py.hpp
	cp ../python.hpp ./

test: test.cpp sample.py.hpp
	g++ test.cpp -o test -l python3.2mu
	echo "#!/bin/sh" > run
	echo "PYTHONPATH=`pwd` ./test" >> run
	chmod +x run

clean:
	rm -rf sample.py.hpp test run __pycache__ python.hpp
