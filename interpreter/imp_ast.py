# imp_ast.py
# ----------
# This file defines the data structures we will be the output of our 
# parser. We will write our parser using our combinator library which 
# will convert the list of tokens returned by the lexer into an AST. 
# Once the AST is finished, we can easily execute the program. 
#
# There are three kinds of structures in IMP:
#   1. Arithmetic expressions, used to compute numbers.
#   2. Boolean expressions, used to compute conditions for if/while statements. 
#   3. Statements
#
# Starting with arithmetic expressions, these can take the following forms:
#   * Literal integer constants, such as 42
#   * Variables such as x, y
#   * Binary operations, such as x + 42, constructed from other arithmetic 
#     expressions. 
#   
# We can group expressions together with parenthesis, such as (x + 2) * 3. 
# The above isn't a different kind of expression, just a different way to 
# parser the expression. 
#
# Implementation:
#   * We will define three classes for the three different expression forms,
#     plus a base class for arithmetic expressions in general. For now, the 
#     classes won't do much except contain data. 
#   * Include a __repr__ method for printing out the AST for debugging purposes.
#   * All AST classes will subclass `Equality` so we can check if two AST objects
#     are the same, to help with testing. 