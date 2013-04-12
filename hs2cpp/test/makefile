all: test

hs: sample.hs
	../hs2cpp.py sample.hs
	ghc sample.hs.conv.hs

sample.o: sample.cpp
	g++ -I/usr/lib/ghc/include -c sample.cpp

test: hs sample.o
	ghc -threaded -no-hs-main -o test -lstdc++ sample.hs.conv.o sample.o

.PHONY: clean
clean:
	rm -f *.hi *.o *_stub.h *.conv.hs *.hs.hpp test

