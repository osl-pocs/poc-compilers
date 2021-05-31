/* options */
%option noyywrap
%option nodefault

%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "bilex.h"
#include "bilex.tab.h"

extern "C" int yylex();

char string_buf[MAX_STR_CONST];
char *string_buf_ptr;

int comment_counter = 0;
int lineno = 0;


%}

COMMENT_SINGLE_LINE     #.*
COMMENT_OPEN            "/*"
COMMENT_CLOSE           "*/"

DIGIT                   [0-9]
NUMBER                  {DIGIT}+
CHAR                    .
ANY                     .

WHITESPACE              [ \t\n\r]
QUOTE                   \"
NEWLINE                 \n

%x COMMENT
%x STRING

%%

 /* COMMENTS */
<INITIAL,COMMENT>{NEWLINE} {
    lineno++;
}
<INITIAL,COMMENT>{COMMENT_OPEN}	{
    comment_counter++;
    BEGIN(COMMENT);
}
<INITIAL>{COMMENT_CLOSE} {
    return ERROR;
}
<COMMENT>{COMMENT_CLOSE} {
    comment_counter--;
    if (comment_counter <= 0) {
        BEGIN(INITIAL);
        comment_counter = 0;
    }
}
<COMMENT>{CHAR} ;
<COMMENT><<EOF>> {
    BEGIN(INITIAL);
    return ERROR;
}

{COMMENT_SINGLE_LINE} ;


 /* DATATYPES */

 /* STRING */
<INITIAL>{QUOTE} {
    string_buf[0] = '\0';
    string_buf_ptr = string_buf;
    BEGIN(STRING);
}
<STRING>{QUOTE} {
    yylval.string_ = string_buf;
    printf("STRING: %s\n", yylval.string_);

    BEGIN(INITIAL);
    return STRING;
}
<STRING>{CHAR} {
    printf("CHAR: %s\n", yytext);
    *string_buf_ptr = yytext[0];
    string_buf_ptr++;
}
<STRING><<EOF>> {
    BEGIN(INITIAL);
    return ERROR;
}

{NUMBER} {
    printf("NUMBER: %s\n", yytext);
    yylval.integer_ = atoi(yytext);
    return NUMBER;
}

{WHITESPACE} ; /* ignore whitespace */
{ANY} {
    printf("ANY: %s\n", yytext);
    return ANY;
}

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
