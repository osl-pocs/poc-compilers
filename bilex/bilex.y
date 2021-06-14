%{
#include <iostream>
#include <math.h>
#include <string>
#include <bits/stdc++.h>
#include "bilex.h"
#include "ast.h"
#include "utils.h"

extern "C" {
    int yylex();
};

extern int lineno;
extern int colnum;

void yyrestart(FILE* input_file);

void yyerror(const std::string s);

%}

%union {
    int integer_;
    float float_;
    Boolean boolean_;
    char* string_;
    struct AST* ast_;
    struct Literal* literal_;
    struct IfStmt* if_;
    char* error_message;
}

/* declare tokens */

/* datatypes */

%token <integer_> LITERAL_INTEGER
%token <float_> LITERAL_FLOAT
%token <string_> LITERAL_STRING
%token <boolean_> LITERAL_BOOLEAN

%token UNDEFINED NIL

%token IN IS

/* FLOW */
%token IF ELSE ELSEIF CASE WHEN SWITCH
%token WHILE FOR

%token ERROR
%token EOL

/* Declare types for the grammar's non-terminals. */
%type <ast_> program stmt_list stmt expr_list expr literal

%left '+' '-'
%left '*' '/'

%start program

%%

program: stmt_list
    {
        if ($1) {
            printAST($1);
            treefree($1);
            printf("\n");
        }
    }
;

stmt_list: stmt { $$ = $1; }
    | stmt_list stmt { $$ = newast(NodeType::kNODE, $1, $2); }
;

stmt: expr_list { $$ = $1; }
    | stmt expr { $$ = newast(NodeType::kNODE, $1, $2); }
;

expr_list: expr { $$ = $1; }
    | expr_list expr { $$ = newast(NodeType::kNODE, $1, $2); }

expr: expr '+' expr { $$ = newast(NodeType::kOPADD, $1, $3); }
    | expr '-' expr { $$ = newast(NodeType::kOPSUB, $1, $3); }
    | expr '*' expr { $$ = newast(NodeType::kOPMUL, $1, $3); }
    | expr '/' expr { $$ = newast(NodeType::kOPDIV, $1, $3); }
    | '(' expr ')' { $$ = $2; }
    | literal { $$ = $1; }
    | EOL { $$ = finishast(NodeType::kEOL); }
    | IF '(' expr_list ')' '{' expr_list '}' { $$ = newif($3, $6); }
;

literal: LITERAL_INTEGER { $$ = newint($1); }
    | LITERAL_FLOAT { $$ = newfloat($1); }
    | LITERAL_BOOLEAN { $$ = newboolean($1); }
    | LITERAL_STRING { $$ = newstring($1); }
;


%%

/*
 * This function is called automatically when Bison detects a parse error.
 */
void yyerror(const std::string s)
{
    std::cerr << "\"" << s << "\" at"
        << " line " << lineno
        << " column " << colnum
        << " near ";
    print_token(yychar);
    std::cerr << std::endl;
    exit(1);
}

int main(int argc, char **argv) {
    int i;

    // just read stdin
    if(argc < 2) {
        while (yyparse() != 0);
        return 0;
    }

    for(i = 1; i < argc; i++) {
        FILE *f = fopen(argv[i], "r");

        if(!f) {
            perror(argv[i]);
            return (1);
        }

        yyrestart(f);
        while (yyparse() != 0) ;
        fclose(f);
    }

    return 0;
}
