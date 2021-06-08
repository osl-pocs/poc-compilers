# LDFLAGS="-L${CONDA_PREFIX}/lib ${LDFLAGS}"
COMPILER=g++
# removed: -Wno-unused -Wno-deprecated -Wno-write-strings -DDEBUG
CFLAGS= -g -Wall
CINCLUDE=-I `pwd` -I `pwd`/include
SOURCES=`pwd`/src/ast.cpp `pwd`/src/utils.cpp

FLEX_FLAGS= --outfile bilex.lex.yy.c
FLEX=flex ${FLEX_FLAGS}

# removed: --yacc --name-prefix bilex_yy
BISON_FLAGS=-d --debug --verbose --file-prefix bilex
BISON=bison ${BISON_FLAGS}


.PHONY: clean-parser
clean-parser:
	rm -f bilex.tab.*
	rm -f bilex.output


.PHONY: clean-lexer
clean-lexer:
	rm -f bilex.lex.yy.*


.PHONY: clean-build
clean-build:
	rm -f bilex


.PHONY: clean-all
clean-all: clean-parser clean-lexer clean-build


.PHONY: build-lexer
build-lexer: clean-lexer
	${FLEX} bilex.l


.PHONY: build-parser
build-parser: clean-parser
	${BISON} bilex.y


.PHONY: compile-parser
compile-parser: clean-all build-parser build-lexer
	$(COMPILER) ${CFLAGS} ${CINCLUDE} ${SOURCES} bilex.tab.c -lfl -o bilex


.PHONY: compile-lexer
compile-lexer: clean-all build-parser build-lexer
	$(COMPILER) ${CFLAGS} ${CINCLUDE} ${SOURCES} bilex.lex.yy.c -lfl -o bilex


.PHONY: compile-all
compile-all: clean-all build-parser build-lexer
	$(COMPILER) ${CFLAGS} ${CINCLUDE} ${SOURCES} bilex.tab.c bilex.lex.yy.c -lfl -o bilex


.PHONY: run-test
run-test:
	./bilex source.blx


.PHONY: all
all: build-parser build-lexer combine-lexer-parser compile-source
