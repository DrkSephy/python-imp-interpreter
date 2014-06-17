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

token_exprs = [
    (r'[ \\n\\t]+',         None),   # match whitespace
    (r'#[^\\n]*',           None),   # match comments
]

