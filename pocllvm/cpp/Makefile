COMPILER=clang++
CFLAGS= -g -O3 `llvm-config --cxxflags --ldflags --system-libs --libs core` -std=c++17
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
	./pocllvm source.blx


.PHONY: all
all: build-parser build-lexer combine-lexer-parser compile-source

.PHONY: docker-run
docker-run:
	docker-compose run pocllvm
