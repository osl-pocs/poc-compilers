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
int lineno = 1;
int colnum = 0;


%}

COMMENT_SINGLE_LINE     #.*
COMMENT_OPEN            "/*"
COMMENT_CLOSE           "*/"

DIGIT                   [0-9]
INTEGER                 {DIGIT}+
FLOAT                   {DIGIT}+\.{DIGIT}+
CHAR                    .
ANY                     .

TRUE                    "true"
FALSE                   "false"

WHITESPACE              [ \t\r]
QUOTE                   \"
NEWLINE                 \n

ERROR                   .

%x COMMENT
%x STRING

%%

 /* COMMENTS */
<INITIAL,COMMENT>{NEWLINE} {
    lineno++;
    colnum = 0;
}
<INITIAL,COMMENT>{COMMENT_OPEN}	{
    comment_counter++;
    BEGIN(COMMENT);
}
<INITIAL>{COMMENT_CLOSE} {
    yylval.error_message = "Closed comment found but no open comment found.";
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

    yylval.error_message = (char*) "EOF found but the comment was not closed.";
    return ERROR;
}

{COMMENT_SINGLE_LINE} ;


 /* DATATYPES */

 /* STRING */
<INITIAL>{QUOTE} {
    string_buf[0] = '\0';
    string_buf_ptr = string_buf;
    colnum++;
    BEGIN(STRING);
}
<STRING>{QUOTE} {
    yylval.string_ = string_buf;
    colnum++;
    BEGIN(INITIAL);
    return LITERAL_STRING;
}
<STRING>{CHAR} {
    *string_buf_ptr = yytext[0];
    string_buf_ptr++;
    colnum++;
}
<STRING>{NEWLINE} {
    BEGIN(INITIAL);
    lineno++;
    colnum = 0;

    yylval.error_message = (char*) "A newline was found but the string was not closed.";
    return ERROR;
}
<STRING><<EOF>> {
    BEGIN(INITIAL);
    yylval.error_message = (char*) "A <EOF> was found but the string was not closed.";
    return ERROR;
}

{INTEGER} {
    yylval.integer_ = atoi(yytext);
    colnum += yyleng;
    return LITERAL_INTEGER;
}

{FLOAT} {
    yylval.float_ = atof(yytext);
    colnum += yyleng;
    return LITERAL_FLOAT;
}

{TRUE} {
    yylval.boolean_ = 1;
    colnum += yyleng;
    return LITERAL_BOOLEAN;
}

{FALSE} {
    yylval.boolean_ = 0;
    colnum += yyleng;
    return LITERAL_BOOLEAN;
}

"+" |
"-" |
"*" |
"/" {
    colnum++;
    return yytext[0];
}

{WHITESPACE} {
    colnum += yyleng;
}

{NEWLINE} {
    lineno++;
    colnum=0;
    return EOL;
}

{ERROR} {
    colnum++;
    yylval.error_message = (char*) "It was not possible to create a token.";
    return ERROR;
}

%%
