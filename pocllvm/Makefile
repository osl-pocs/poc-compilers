COMPILER=clang++
CFLAGS= -g -O3 `llvm-config --cxxflags` -std=c++17
CINCLUDE=-I `pwd` -I `pwd`/include
SOURCES=`pwd`/src/pocllvm.cpp


.PHONY: clean-build
clean-build:
	rm -f *.o pocllvm


.PHONY: compile-all
compile-all: clean-build
	$(COMPILER) ${CFLAGS} ${CINCLUDE} ${SOURCES} -o pocllvm


.PHONY: run-test
run-test:
	./bilex source.blx


.PHONY: all
all: build-parser build-lexer combine-lexer-parser compile-source
