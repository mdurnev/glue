all: test

hs: sample.hs
	../hs2cpp.py sample.hs
	ghc sample.hs.conv.hs

test: hs sample.cpp
	g++ -I/usr/lib/ghc/include -L/usr/lib/ghc -o test -lHSrts_thr sample.hs.conv.o sample.cpp

.PHONY: clean
clean:
	rm -f *.hi *.o *_stub.h *.conv.hs *.hs.hpp

