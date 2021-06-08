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
    case LITERAL_INTEGER:
        return "INTEGER";
    case LITERAL_FLOAT:
        return "FLOAT";
    case LITERAL_STRING:
        return "STRING";
    case LITERAL_BOOLEAN:
        return "BOOLEAN";
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
        return "<Invalid Token:>";
    }
}


void print_token(int tok)
{

    std::cerr << token_to_string(tok);

    switch (tok) {
    case LITERAL_STRING:
        std::cerr << " = " << " \""  << yylval.string_ << "\"";
        break;
    case LITERAL_INTEGER:
        std::cerr << " = " << yylval.integer_;
        break;
    case LITERAL_FLOAT:
        std::cerr << " = " << yylval.float_;
        break;
    case LITERAL_BOOLEAN:
        std::cerr << (yylval.boolean_ ? " = true" : " = false");
        break;
    case ERROR:
        std::cerr << " = " << yylval.error_message;
        break;
    default:
         std::cerr << '(' << tok << ')';
    }
}
