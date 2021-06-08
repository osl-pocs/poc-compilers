#ifndef _BILEX_AST_H_
#define _BILEX_AST_H_

#include "bilex.h"
#include <string>


enum class NodeType {
    kINTEGER,
    kFLOAT,
    kBOOLEAN,
    kSTRING,
    kOPADD,
    kOPSUB,
    kOPMUL,
    kOPDIV,
    kPARENOPEN,
    kPARENCLOSE,
    kIF,
    kWHILE,
    kFOR,
    kASSIGN,
    kEQ,
    kNEQ,
    kNOT,
    kLT,
    kLE,
    kGT,
    kGE,
    kNEG
};


struct AST {
    NodeType nodetype;
    struct AST* l;
    struct AST* r;
};


struct LiteralInteger {
    NodeType nodetype;
    int value;
};

struct LiteralFloat {
    NodeType nodetype;
    float value;
};

struct LiteralBoolean {
    NodeType nodetype;
    Boolean value;
};

struct LiteralString {
    NodeType nodetype;
    char* value;
};


struct AST* newast(NodeType nodetype, struct AST* l, struct AST* r);

struct AST* newint(int value);

struct AST* newfloat(float value);

struct AST* newboolean(Boolean value);

struct AST* newstring(char* value);

void treefree(struct AST* ast);

void printAST(struct AST* ast);

#endif
