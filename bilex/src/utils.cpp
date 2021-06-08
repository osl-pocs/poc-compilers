#include <iostream>
#include <ctype.h>
#include <string>

#include "bilex.h"
#include "bilex.tab.h"


/*
 * Used for debugging the parser.
 */

std::string token_to_string(int tok)
{
    switch (tok) {
    case 0:
        return "EOF";
    case EOL:
        return "EOF";
    case INTEGER:
        return "INTEGER";
    case FLOAT:
        return "FLOAT";
    case STRING:
        return "STRING";
    case BOOLEAN:
        return "BOOLEAN";
    case ANY:
        return "ANY";
    case ERROR:
        return "ERROR";
    case '+':
        return "'+'";
    case '-':
        return "'-'";
    case '*':
        return "'*'";
    case '/':
        return "'/'";
    default:
        return("<Invalid Token>");
    }
}


void print_token(int tok)
{

    std::cerr << token_to_string(tok);

    switch (tok) {
    case STRING:
        std::cerr << " = " << " \""  << yylval.string_ << "\"";
        break;
    case INTEGER:
        std::cerr << " = " << yylval.integer_;
        break;
    case FLOAT:
        std::cerr << " = " << yylval.float_;
        break;
    case BOOLEAN:
        std::cerr << (yylval.boolean_ ? " = true" : " = false");
        break;
    case ERROR:
        std::cerr << " = " << yylval.error_message;
        break;
    }
}
