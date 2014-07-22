# IMP Lexer
# ---------
# Using our general lexer, we can now build a lexer for IMP. 
# We will define tags for each of our tokens. IMP only needs
# three tags:
# 
#   1. RESERVED : tag indicator for a reserved word or operator
#   2. INT : tag indicator for a literal integer
#   3. ID : tag indicator for identifiers

import lexer

# Bind tags for keywords

RESERVED = 'RESERVED'
INT      = 'INT'
ID       = 'ID'

# Next, we define token expressions which will be used in the lexer.
# We start with the characters we will drop (whitespace and comments)
# 'r' before each regex means the string is "raw". 
# Python will not handle any escape characters, which allows us to 
# include backslashes in the strings, which are used by the regex
# engine to escape operators like "+" and "*".

token_exprs = [
    (r'[ \n\t]+',              None),
    (r'#[^\n]*',               None),
    (r'\:=',                   RESERVED),
    (r'\(',                    RESERVED),
    (r'\)',                    RESERVED),
    (r';',                     RESERVED),
    (r'\+',                    RESERVED),
    (r'-',                     RESERVED),
    (r'\*',                    RESERVED),
    (r'/',                     RESERVED),
    (r'<=',                    RESERVED),
    (r'<',                     RESERVED),
    (r'>=',                    RESERVED),
    (r'>',                     RESERVED),
    (r'!=',                    RESERVED),
    (r'=',                     RESERVED),
    (r'and',                   RESERVED),
    (r'or',                    RESERVED),
    (r'not',                   RESERVED),
    (r'if',                    RESERVED),
    (r'then',                  RESERVED),
    (r'else',                  RESERVED),
    (r'while',                 RESERVED),
    (r'do',                    RESERVED),
    (r'end',                   RESERVED),
    (r'[0-9]+',                INT),
    (r'[A-Za-z][A-Za-z0-9_]*', ID),
]

# Create our lexer function
def imp_lex(characters):
    return lexer.lex(characters, token_exprs)

