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

from imp_lexer import *
from combinators import *
from imp_ast import *

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

# Next up is handling operators and precedence. It is easy to define another kind of `aexp` 
# parser and throw it together with `aexp_term`. This would result in a simple expression:
# 
#                                   1 + 2 * 3
# being parsed incorrectly as:
#
#                                   (1 + 2) * 3
#
# The parser needs to be aware of operator precedence, and it needs to group together operations
# with higher precedence. To do this, we need to define a few helper functions.

def process_binop(op):
    return lambda l, r: BinopAexp(op, 1, r)
  
# `process_binop` is what actually constructs the `BinopAexp` objects It takes any arithmetic 
# operator and returns a function that combines a pair of expressions using that operator. 
# `process_binop` will be used with the `Exp` combinator(* operator). `Exp` parses a list of 
# expressions. The left operator of `Exp` is a parser that will match individual elements of 
# the list (arithmetic expressions in our case). The right operand is a parser that will match 
# the separators (operators). No matter which separator is matched, the right parser will return
# a function which, given the matched separator, returns a combining function. The combining 
# function takes the parsed expressions to the left and right of the separator and returns a 
# single, combined expression. `process_binop` is actually what will be returned by the right 
# parser.

# Next we define our precedence levels and a combinator to deal with them. 

def any_operator_in_list(ops):
    op_parsers = [keyword(op) for op in ops]
    parser = reduce(lambda l, r: l | r, op_parsers)
    return parser

aexp_precedence_levels = [
    ['*', '/'],
    ['+', '-'],
]

# `any_operator_in_list` takes in a list of keyword strings and returns a parser that will
# match any of them. We will call this on `aexp_prededence_levels`, which contains a list of 
# operators for each precedence level (highest precedence first).

def precedence(value_parser, precedence_levels, combine):
    def op_parser(precedence_level):
        return any_operator_in_list(precedence_level) ^ combine
    parser = value_parser * op_parser(precedence_levels[0])
    for precedence_level in precedence_levels[1:]:
        parser = parser * op_parser(precedence_level)
    return parser

# `precedence` does most of the operations needed. The first argument, `value_parser` is a 
# parser that can read the basic parts of an expression: numbers, variables and groups. That 
# will be `aexp_term`. `precedence_levels` is a list of lists of operators, one list for each 
# level. We use `aexp_precedence_levels` for this. `combine` will take a function which, given
# an operator, returns a function to build a larger expression out of two smaller expressions. 
# That is `process_binop`.

# Inside `precedence, we define `op_parser` which, for a given precedence level, reads any
# operator in that level and returns a function which combines two expressios. `op_parser` can
# be used as the right-hand argument of `Exp`. We then start by calling `Exp` with op_parser for
# the highest precedence level, since those operations will need to be grouped together first.
# We use the resulting parser as the element parser (`Exp`'s left argument at the next level. 
# When the loop finishes, the resulting parser can then correctly parse any arithmetic expression.

# An example of the usage is shown below:
#   E0 = value_parser
#   E1 = E0 * op_parser(precedence_levels[0])
#   E2 = E1 * op_parser(precedence_levels[1])

# E0 is the same as `value_parser`, which can parse numbers, variables and groups, but not operators.
# E1 can parse expressions containing everything E0 can match, separated by operators in the
# first precedence level. Therefore, E1 can match a * b / c, but it would raise an error as 
# soon as it encountered a `+` operator. E2 can match expressions E1 can match, separated 
# by operators in the next precedence level. Since we only have two precedence levels, `E2`
# can match any arithmetic expression we support.

# For a real exmaple, see below:
#   4 * a + b / 2 - ( 6 + c )
#   E0(4) + E0(a) + E0(b) / E0(2) - E0(6 + c)
#   E1(4*a) + E1(b/2) - E1(6 + c)
#   E2((4*a) + (b/2) - (6+c))

# We use `precedence` to directly define `aexp`:

def aexp():
    return precedence(aexp_term(), aexp_precedence_levels, process_binop)

# Now that we are finished handling arithmetic expressions, we move onto Boolean expressions, 
# which are simpler than arithmetic expressions. We start with the most basic Boolean expression,
# relations.

def process_relop(parsed):
      ((left, op), right) = parsed
      return RelopBexp(op, left, right)

def bexp_relop():
      relops = ['<', '<=', '>', '>=', '=', '!=']
      return aexp() + any_operator_in_list(relops) + aexp() ^ process_relop

# `process_relop` is a function which we use with the `Process` combinator. It just takes three
# concatenated values and creates a `RelopBexp` out of them. In `bexp_relop`, we parse two 
# arithmetic expressions (aexp), separated by a relational operator. We use our method 
# `any_operator_in_list` so we don't have to write a case for every single operator. There is 
# no need to use combinators like `Exp` or precedence` since relational expressions can't be 
# chained together in IMP. 

# The next operator to parse is the `not` expression, which is a unary operation with high 
# precedence.

def bexp_not():
    return keyword('not') + Lazy(bexp_term) ^ (lambda parsed: NotBexp(parsed[1]))

# Above we concatnate the keyword `not` with a Boolean expression term, which is defined 
# below. Since `bexp_not` will be used to define `bexp_term`, we need to use the `Lazy`
# combinator to avoid infinite recursion. 

def bexp_group():
    return keyword('(') + Lazy(bexp) + keyword(')') ^ process_group

def bexp_term():
    return bexp_not()   | \
           bexp_relop() | \
           bexp_group()

# `bexp_group` and `bexp_term` are essentially the same as their arithmetic equivalents. gitgi

# Our last boolean expressions we need to parse are the `AND` and `OR` operators. These operators
# work the same way as the arithmetic operators do, they are evaluated left to right, with `AND`
# having the higher precedence. 

bexp_precedence_levels = [
    ['and'],
    ['or'],
]

def process_logic(op):
    if op == 'and':
        return lambda l, r: AndBexp(l, r)
    elif op == 'or':
        return lambda l, r: OrBexp(l, r)
    else:
        raise RuntimeError('unknown logic operator: ' + op)

def bexp():
    return precedence(bexp_term(), bexp_precedence_levels, process_logic)

# Like `process_binop`, `process_logic` is intended to be used with the `Exp` combinator. It takes
# an operator and returns a function which combines two sub-expressions into an expression using 
# that operator. We pass this along to `precedence`, just like we did with `aexp`. 

# We now move onto parsing IMP statements. 

def assign_stmt():
    def process(parsed):
        ((name, _), exp) = parsed
        return AssignStatement(name, exp)
    return id + keyword(':=') + aexp() ^ process

def stmt_list():
    separator = keyword(';') ^ (lambda x: lambda l, r: CompoundStatement(l, r))
    return Exp(stmt(), separator)

def if_stmt():
    def process(parsed):
        (((((_, condition), _), true_stmt), false_parsed), _) = parsed
        if false_parsed:
            (_, false_stmt) = false_parsed
        else:
            false_stmt = None
        return IfStatement(condition, true_stmt, false_stmt)
    return keyword('if') + bexp() + \
           keyword('then') + Lazy(stmt_list) + \
           Opt(keyword('else') + Lazy(stmt_list)) + \
           keyword('end') ^ process

def while_stmt():
    def process(parsed):
        ((((_, condition), _), body), _) = parsed
        return WhileStatement(condition, body)
    return keyword('while') + bexp() + \
           keyword('do') + Lazy(stmt_list) + \
           keyword('end') ^ process

def stmt():
    return assign_stmt() | \
           if_stmt()     | \
           while_stmt()

# top-level parser
def parser():
    return Phrase(stmt_list())

# parser will parse an entire program. A program is simply a list of statements, 
# but the `Phrase` combinator ensures we use every token in the file, rather
# than ending prematurely if there are any garbage tokens at the end. 
