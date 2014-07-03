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

from equality import *

class Aexp(Equality):
    pass

class IntAexp(Aexp):
    def __init__(self, i):
        self.i = i

    def __repr__(self):
        return 'IntAexp(%d)' % self.i

class VarAexp(Aexp):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'VarAexp(%s)' % self.name

class BinopAexp(Aexp):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.rigt = right

    def __repr__(self):
        return 'BinopAexp(%s, %s, %s' % (self.op, self.left, self.right)

# Boolean expressions are the next on our list. There are four kinds of 
# Boolean expressions.
#
# * Relational expressions (ex: x < 20)
# * AND expressions (such as x < 20 and y > 20)
# * OR expressions
# * NOT expressions
#
# The left and right sides of a relational expressions are arithmetic expressions.
# The left and right sides of any "AND", "OR" or "NOT" expression are Boolean 
# expressions. Restricting the type like this will help us avoid expressions such as:
#
#                                   X < 10 and 30

class Bexp(Equality):
    pass

class ReloBexp(Bexp):
    def __init__(self, op, left, right):
        ... 

class AndBexp(Bexp):
    def __init__(self, left, right):
        ...

class NotBexp(Bexp):
    def __init__(self, exp):
        ...

# Next we focus on statements, which can contain both arithmetic and boolean expressions.
# There are four kinds of statements: assignment, compound, conditional and loops.

class Statement(Equality):
    pass

class AssignStatement(Statement):
    def __init__(self, name, aexp):
        ...

class CompundStatement(Statement):
    def __init__(self, first, second):
        ...

class IfStatement(Statement):
    def __init__(self, condition, true_stmt, false_stmt):
        ...

class WhileStatement(Statement):
    def __init__(self, condition, body):
        ...

# Our AST classes are now set up, and we also have a set of parser combinators. We now
# move on to write our parser. We start with the most basic structures and then work up
# to more complicated structures.
#
# The first parser we will implement is the `keyword` parser, which is a specialized 
# version of the `Reserved` combinator using the `RESERVED` tag that all keyword tokens
# are tagged with. 
#
# NOTE: The `Reserved` tag will match a single token where both the text and tag are the 
# same as the ones given.

def keyword(kw):
    return Reserved(kw, RESERVED)

# `keyword` is actually a combinator because it is a function which returns a parser. 
# It will be used directly in other parsers. 

# The `id` parser is used to match variable names. It uses the `Tag` combinator, which
# matches a token with the specified tag. 

id = Tag(ID)

# The `num` parser is used to match integers. It works similarly to `id`, except it 
# uses the `Process` combinator (actually, the ^ operator, which calls `Process`) to
# convert the token into an actual integer value.

num = Tag(INT) ^ (lambda i: int(i))

# The next parser we need to build is the arithmetic expression parser, since we need to 
# parser these in order to parse Boolean expressions and statements. 
#
# We will first define the `aexp_value` parser, which will convert the values returned 
# by `num` and `id` into actual expressions. 

def aexp_value():
    return (num ^ (lambda i: IntAexp(i))) | \ 
           (id  ^ (lambda v: VarAexp(v))) 
 
# The | operator is shorthand for the `Alternate` combinator. This function will attempt
# to parse an integer expression first, and if that fails it will try to parse a variable
# expression. 

# We've defined aexp_value() as a zero-argument function instead of a global value, like
# we did with `id` and `num`. We will do the same thing with all the other parsers. The 
# reason is that we don't want the code for each parser to be evaluated right away. If we 
# define every parser as a global, each parser would not be able to reference parsers that 
# come after it in the same source file, since they would not be defined yet. This leads to
# not being able to define recursive parsers. 

# The next thing we need to support is grouping with parenthesis in our arithmetic expressions.
# Grouped expressions don't require their own AST class, but they require another parser to 
# handle them. 

def process_group(parsed):
    ((_, p), _) = parsed
    return p

def aexp_group():
    return keyword('(') + Lazy(aexp) + keyword(')'( ^ process_group

# `process_group` is a function used with the `Process` combinator (^ operator). It discards the # parenthesis tokens and returns the expression in between. `aexp_group` is the actual parser. 
# Remember, the `+` operator is shorthand for the `Concat` combinator. So, this will parse '(', 
# followed by an arithmetic expression (which will be parsed by `aexp`, which we define soon), 
# followed by ')'. We need to avoid calling aexp directly since aexp will call `aexp_group`, 
# which will result in infinite recursion. To avoid this, we use the `Lazy` combinator, which 
# defers the call to `aexp` until the parser is actually applied to some input. 

# The next step is to combine `aexp_value` and `aexp_group` using `aexp_term`. An `aexp_term` 
# expression is any basic, self-contained expression where we don't have to worry about operator
# precedence with respect to other expressions.

def aexp_term():
  return aexp_value() | aexp_group()


