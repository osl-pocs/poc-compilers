#include <stdlib.h>

#include "bilex.h"
#include "ast.h"
#include "utils.h"


int node_count = 1;


void yyerror(const char* text) {
    printf("[EE] %s", text);
}


struct AST* newast(NodeType nodetype, struct AST* l, struct AST* r) {
    struct AST* ast = (struct AST*) malloc(sizeof(struct AST));

    if (!ast) {
        yyerror("Out of space");
        exit(0);
    }

    ast->nodetype = nodetype;
    ast->l = l;
    ast->r = r;
    return ast;
}

struct AST* finishast(NodeType nodetype) {
    struct AST* ast = (struct AST*) malloc(sizeof(struct AST));

    if (!ast) {
        yyerror("Out of space");
        exit(0);
    }

    ast->nodetype = nodetype;
    return ast;
}

// DATA AST

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

// STRUCT AST

struct AST* newif(struct AST* condition, struct AST* body) {
    struct IfStmt* ast = (struct IfStmt*) malloc(sizeof(struct IfStmt));

    if (!ast) {
        yyerror("Out of space");
        exit(0);
    }

    ast->nodetype = NodeType::kIF;
    ast->condition = condition;
    ast->body = body;

    return (struct AST*) ast;
}

// free a tree of ASTs

void treefree(struct AST* ast) {
    if (ast == NULL) {
        return;
    }

    switch(ast->nodetype) {
    // terminal
    case NodeType::kEOL:
        break;
    // two subtrees
    case NodeType::kNODE:
    case NodeType::kOPADD:
    case NodeType::kOPSUB:
    case NodeType::kOPMUL:
    case NodeType::kOPDIV:
        treefree(ast->r);
    // one subtree
        treefree(ast->l);
        break;
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
        treefree(((struct IfStmt*) ast)->condition);
        treefree(((struct IfStmt*) ast)->body);
        break;
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

char* nodetype_to_string(AST* ast) {
    switch(ast->nodetype) {
    case NodeType::kEOL:
        return "EOL";
    case NodeType::kNODE:
        return "NODE";
    // constant
    case NodeType::kINTEGER:
        return "INTEGER";
    case NodeType::kFLOAT:
        return "FLOAT";
    case NodeType::kBOOLEAN:
        return "BOOLEAN";
    case NodeType::kSTRING:
        return "STRING";
    case NodeType::kOPADD:
        return "+";
    case NodeType::kOPSUB:
        return "-";
    case NodeType::kOPMUL:
        return "*";
    case NodeType::kOPDIV:
        return "/";
    case NodeType::kIF:
        return "IF";
    default:
        return "INVALID_NODE_TYPE";
    }
}

void printAST(struct AST* ast) {
    if(!ast) {
        printf("NULL");
        return;
    }

    printf("\n%0*c", node_count, ' ');
    printf("%s", nodetype_to_string(ast));

    switch(ast->nodetype) {
    case NodeType::kEOL:
        return;
    case NodeType::kNODE:
        node_count++;
        printf(": (");
        if (ast->l) {
            printAST(ast->l);
        } else {
            printf("L node empty");
        }

        printf("\n%0*c,", node_count, ' ');

        if (ast->r) {
            printAST(ast->r);
        } else {
            printf("R node empty");
        }
        node_count--;
        printf("\n%0*c)", node_count, ' ');
        break;
    // constant
    case NodeType::kINTEGER:
        printf(
            "(%i)",
            ((struct LiteralInteger*) ast)->value
        );
        break;
    case NodeType::kFLOAT:
        printf(
            "(%f)",
            ((struct LiteralFloat*) ast)->value
        );
        break;
    case NodeType::kBOOLEAN:
        printf(
            "(%i)",
            ((struct LiteralBoolean*) ast)->value
        );
        break;
    case NodeType::kSTRING:
        printf(
            "(%s)",
            ((struct LiteralString*) ast)->value
        );
        break;
    // name reference: not implemented yet
    // assignment: not implemented yet
    /* expressions */
    case NodeType::kOPADD:
    case NodeType::kOPSUB:
    case NodeType::kOPMUL:
    case NodeType::kOPDIV:
        printf(": (");
        node_count++;
        printAST(ast->l);
        printf("\n%0*c,", node_count, ' ');
        printAST(ast->r);
        node_count--;
        printf("\n%0*c)", node_count, ' ');
        break;
    case NodeType::kIF:
        printf("(");
        node_count++;
        printAST(((struct IfStmt*) ast)->condition);
        node_count--;
        printf("\n%0*c) {", node_count, ' ');
        node_count++;
        printAST(((struct IfStmt*) ast)->body);
        node_count--;
        printf("\n%0*c}", node_count, ' ');
        break;
    // comparisons: not implemented yet
    // control flow: not implemented yet
    default:
        printf("internal error: bad node %i\n", (int) ast->nodetype);
    }
}
