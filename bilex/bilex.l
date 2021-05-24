/* options */
%option noyywrap

%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "bilex.h"
#include "bilex.tab.h"

extern "C" int yylex();

%}

DIGIT           [0-9]
NUMBER          {DIGIT}+
ANY             .+
WHITESPACE      [ \t\n\r]

%%

{NUMBER}                { printf("ANY %s\n", yytext); yylval.integer_ = atoi(yytext); return NUMBER; }
{ANY}                   { printf("ANY %s\n", yytext); return ANY; }
{WHITESPACE}            ; /* ignore whitespace */

%%


int main(int argc, char **argv) {
    int i;

    /* just read stdin */
    if(argc < 2) {
        while (yylex() != 0);
        return 0;
    }

    for(i = 1; i < argc; i++) {
        FILE *f = fopen(argv[i], "r");

        if(!f) {
            perror(argv[i]);
            return (1);
        }

        yyrestart(f);
        while (yylex() != 0) ;
        fclose(f);
    }

    return 0;
}
