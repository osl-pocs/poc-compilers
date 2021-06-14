#ifndef _BILEX_AST_H_
#define _BILEX_AST_H_

#include "bilex.h"
#include <string>


enum class NodeType {
    kEOL = 0,
    kNODE = 1,
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

// DATA NODES

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

// Structures

struct IfStmt {
    NodeType nodetype;
    struct AST* condition;
    struct AST* body;
};


// Create new Nodes

struct AST* newast(NodeType nodetype, struct AST* l, struct AST* r);

struct AST* newint(int value);

struct AST* newfloat(float value);

struct AST* newboolean(Boolean value);

struct AST* newstring(char* value);

struct AST* finishast(NodeType nodetype);

struct AST* newif(struct AST* condition, struct AST* body);

void treefree(struct AST* ast);

void printAST(struct AST* ast);

char* nodetype_to_string(AST* ast);

#endif
