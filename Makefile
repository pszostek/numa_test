BINARIES := testNumaO2 testNumaO3 testNumaO2Ftree testNumaO3NoVec testNumaO2_malloc testNumaO3_malloc
 
DOTS:=$(wildcard *.dot)
PDFS=$(DOTS:.dot=.pdf)

all: ${BINARIES}
pdf: ${PDFS}

testNumaO2_malloc: testNuma_malloc.cpp
		g++ -ftree-vectorize -fopenmp -std=c++11 $^ -o $@
testNumaO3_malloc: testNuma_malloc.cpp
		g++ -ftree-vectorize -fopenmp -std=c++11 $^ -o $@
testNumaO2: testNuma.cpp
		g++ -fopenmp -std=c++11 -lnuma $^ -o $@
testNumaO3: testNuma.cpp
		g++ -O3 -fopenmp -std=c++11 -lnuma $^ -o $@
testNumaO2Ftree: testNuma.cpp
		g++ -O2 -fopenmp -mavx -ftree-vectorize -std=c++11 -lnuma $^ -o $@
testNumaO3NoVec: testNuma.cpp
		g++ -O3 -fno-tree-vectorize -fopenmp -std=c++11 -lnuma $^ -o $@

%.pdf : %.dot
	neato -Tpdf -o $@ $<

.PHONY: clean
clean:
		rm -f ${BINARIES} *.pdf

