all: test sample.py.hpp

sample.py.hpp: sample.py
	echo "sample" | ./py2cpp.py > sample.py.hpp

test: test.cpp sample.py.hpp
	g++ test.cpp -o test -l python3.2mu
	echo "#!/bin/sh" > run
	echo "PYTHONPATH=`pwd` ./test" >> run
        chmod +x run

clean:
	rm sample.py.hpp test run
