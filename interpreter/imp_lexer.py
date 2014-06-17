# IMP Lexer
# ---------
# Using our general lexer, we can now build a lexer for IMP. 
# We will define tags for each of our tokens. IMP only needs
# three tags:
# 
#   1. RESERVED : tag indicator for a reserved word or operator
#   2. INT : tag indicator for a literal integer
#   3. ID : tag indicator for identifiers