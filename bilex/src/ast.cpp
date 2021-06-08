#include <stdlib.h>

#include "bilex.h"
#include "ast.h"

void yyerror(const char*) {

}


struct AST* newast(NodeType nodetype, struct AST* l, struct AST* r) {
    struct AST* ast = (struct AST*)malloc(sizeof(struct AST));

    if (!ast) {
        yyerror("Out of space");
        exit(0);
    }

    ast->nodetype = nodetype;
    ast->l = l;
    ast->r = r;
    return ast;
}

struct AST* newint(int value) {
    struct LiteralInteger* ast = (struct LiteralInteger*) malloc(sizeof(struct LiteralInteger));

    if (!ast) {
        yyerror("Out of space");
        exit(0);
    }

    ast->nodetype = NodeType::kINTEGER;
    ast->value = value;

    return (struct AST*) ast;
}

struct AST* newfloat(float value) {
    struct LiteralFloat* ast = (struct LiteralFloat*) malloc(sizeof(struct LiteralFloat));

    if (!ast) {
        yyerror("Out of space");
        exit(0);
    }

    ast->nodetype = NodeType::kFLOAT;
    ast->value = value;

    return (struct AST*) ast;
}

struct AST* newboolean(Boolean value) {
    struct LiteralBoolean* ast = (struct LiteralBoolean*) malloc(sizeof(struct LiteralBoolean));

    if (!ast) {
        yyerror("Out of space");
        exit(0);
    }

    ast->nodetype = NodeType::kBOOLEAN;
    ast->value = value;

    return (struct AST*) ast;
}

struct AST* newstring(char* value) {
    struct LiteralString* ast = (struct LiteralString*) malloc(sizeof(struct LiteralString));

    if (!ast) {
        yyerror("Out of space");
        exit(0);
    }

    ast->nodetype = NodeType::kSTRING;
    ast->value = value;

    return (struct AST*) ast;
}

/* free a tree of ASTs */
void treefree(struct AST* ast) {
    switch(ast->nodetype) {
    // two subtrees
    case NodeType::kOPADD:
    case NodeType::kOPSUB:
    case NodeType::kOPMUL:
    case NodeType::kOPDIV:
        treefree(ast->r);
    // one subtree
        treefree(ast->l);
    // no subtree
    case NodeType::kINTEGER:
    case NodeType::kFLOAT:
    case NodeType::kBOOLEAN:
    case NodeType::kSTRING:
        break;
    case NodeType::kASSIGN:
        // not available yet
        break;
    /* up to three subtrees */
    case NodeType::kIF:
    case NodeType::kWHILE:
    case NodeType::kFOR:
        // not available yet
        break;
    default:
        printf("internal error: free bad node %i\n", (int) ast->nodetype);
    }

    // always free the node itself
    free(ast);
}

void printAST(struct AST* ast) {

    if(!ast) {
        yyerror("internal error, null eval");
        return;
    }
    switch(ast->nodetype) {
    // constant
    case NodeType::kINTEGER:
        printf("INTEGER(%i)", ((struct LiteralInteger*) ast)->value);
        break;
    case NodeType::kFLOAT:
        printf("FLOAT(%f)", ((struct LiteralFloat*) ast)->value);
        break;
    case NodeType::kBOOLEAN:
        printf("BOOLEAN(%i)", ((struct LiteralBoolean*) ast)->value);
        break;
    case NodeType::kSTRING:
        printf("STRING(%s)", ((struct LiteralString*) ast)->value);
        break;
    // name reference: not implemented yet
    // assignment: not implemented yet
    /* expressions */
    case NodeType::kOPADD:
        printf("(+, ");
        printAST(ast->l);
        printf(", ");
        printAST(ast->r);
        printf(")");
        break;
    case NodeType::kOPSUB:
        printf("(-, ");
        printAST(ast->l);
        printf(", ");
        printAST(ast->r);
        printf(")");
        break;
    case NodeType::kOPMUL:
        printf("(*, ");
        printAST(ast->l);
        printf(", ");
        printAST(ast->r);
        printf(")");
        break;
    case NodeType::kOPDIV:
        printf("(/, ");
        printAST(ast->l);
        printf(", ");
        printAST(ast->r);
        printf(")");
        break;
    // comparisons: not implemented yet
    // control flow: not implemented yet
    default:
        printf("internal error: bad node %i\n", (int) ast->nodetype);
    }
}
