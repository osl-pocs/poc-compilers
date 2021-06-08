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
    char* error_message;
}

/* declare tokens */

/* datatypes */

%token <integer_> INTEGER
%token <float_> FLOAT
%token <string_> STRING
%token <boolean_> BOOLEAN
%token ANY
%token ERROR
%token EOL

/* Declare types for the grammar's non-terminals. */
%type <ast_> expr stmt

%left '+' '-'
%left '*' '/'

%start stmt

%%

stmt: expr { printAST($1); treefree($1); printf("\n"); }
    | stmt expr { printAST($2); treefree($2); printf("\n"); }
;

expr: expr '+' expr { $$ = newast(NodeType::kOPADD, $1, $3); }
    | expr '-' expr { $$ = newast(NodeType::kOPSUB, $1, $3); }
    | expr '*' expr { $$ = newast(NodeType::kOPMUL, $1, $3); }
    | expr '/' expr { $$ = newast(NodeType::kOPDIV, $1, $3); }
    | '(' expr ')' { $$ = $2; }
    | INTEGER { $$ = newint($1); }
    | FLOAT { $$ = newfloat($1); }
    | BOOLEAN { $$ = newboolean($1); }
    | STRING { printf("%s", (char*)" new string "); $$ = newstring((char*)" new string "); }
    | expr EOL {$$ = $1; }
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
