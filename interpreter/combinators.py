# combinators.py
# --------------
# Language agnostic combinator library
#
# Combinators are one way to write a parser. A parser is essentially
# a function. It accepts a stream of tokens as an input. If it is 
# successful, the parser will consume some tokens from the stream.
# It returns part of the final AST, along with the remaining tokens.
# A combinator is a function which produces a parser as its output,
# usually after taking one or more parsers as an input, hence the name
# "combinator". We can use a combinator to create a complete parser 
# for a language like IMP by creating lots of smaller parsers for 
# parts of the language, then using combinators to build the final
# parser. 

# Parser combinators are usually fairly generic, and can be used with
# any language. First, we will write a language agnostic library of 
# combinators, then use that to write our IMP parser. 

class Result:
    """
    Input: 
        value: part of the AST
        pos:   the index of the next token in the stream

    Returns: `Result` object on success, or `None` on failure. 
    """
    def __init__(self, value, pos):
        self.value = value
        self.pos = pos

    def __repr__(self):
        return 'Result(%s, %d)' % (self.value, self.pos)

# Parsers are functions which take a stream of tokens as input. 
# We will define parsers as objects with a __call__ method. This 
# means that a parser object will behave as if it were a function, 
# but we can also provide additional functionality by defining
# some operators.

# The __call__ method does the parsing. It's input is a full list 
# of tokens, which are returned by the lexer, and an index into the
# list indicating the next token. The default implementation will
# always return `None` (failure), and the subclasses of `Parser` will
# provide their own __call__ implementation. 

# The other methods: __add__, __mul__, __or__, __xor__ define the 
# `+`, `*`, `|`, `^` operators. Each operator provides a shortcut
# for calling a different combinator. 

class Parser:
    def __call__(self, tokens, pos):
        return None # subclasses will override this

    def __add__(self, other):
        return Concat(self, other)

    def __or__(self, other):
        return Alternate(self, other)

    def __xor__(self, function):
        return Process(self, function)

# The simplest combinator is `Reserved`, which will be used to parse
# reserved words and operators. It accepts tokens with a specific 
# value and tag. 

# NOTE: Tokens are nothing but value-tag pairs, where:
#       token[0] : value
#       token[1] : tag

class Reserved(Parser):
    def __init__(self, value, tag):
        self.value = value
        self.tag = tag

    def __call__(self, tokens, pos):
        if pos < len(tokens) and tokens[pos][0] == self.value and tokens[pos][1] is self.tag:
            return Result(tokens[pos][0], pos + 1)
        else:
            return None 

# The next class we implement is the `Tag` combinator. It matches any
# token which has a particular tag. The value can be anything.

class Tag(Parser):
    def __init__(self, tag):
        self.tag = tag

    def __call__(self, tokens, pos):
        if pos < len(tokens) and tokens[pos][1] is self.tag:
            return Result(tokens[pos][0], pos + 1)
        else:
            return None

# The `Tag` and `Reserved` combinators are our primitives. All combinators 
# will be built out of them at the most basic level. 

# In order to parse more complicated expressions, we can create an `concat` 
# combinator which will take two parsers as input (left and right). When 
# the concat parser is applied, it will apply the left parser, followed by
# the right parser. If both parsers are successful, the result value will 
# be a pair containing the left and right results. If either parser is 
# unsuccessful, `None` will be returned. 

class Concat(Parser):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, tokens, pos):
        left_result = self.left(tokens, pos)
        if left_result:
            right_result = self.right(tokens, left_result.pos)
            if right_result:
                combined_value = (left_result.value, right_result.value)
                return Result(combined_value, right_result.pos)
        return None 

# `Concat` is useful for parsing sequences of tokens. For example, to parse
# ` 1 + 2 `, we can write this as :
# parser = Concat(Concat(Tag(INT), Reserved('+', RESERVED)), Tag(Int))
# or using the + operator shorthand:
# parser = Tag(INT) + Reserved('+', RESERVED) + Tag(INT)

# The next combinator we build is the `Alternate` combinator. Like the `Concat`
# parser, it also takes a left and right parser as input. It starts by applying
# the left parser, and if successful that result is returned. If unsuccessful, 
# it applies the right parser and returns its result.

class Alternate(Parser):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, tokens, pos):
        left_result = self.left(tokens, pos)
        if left_result:
            return left_result
        else:
            right_result = self.right(tokens, pos)
            return right_result

# The `Alternate` class is useful for choosing among several possible parsers. 
# For example, if we wanted to parse any binary operator:
# 
#   parser = Reserved('+', RESERVED) | 
#            Reserved('-', RESERVED) |
#            Reserved('*', RESERVED) |
#            Reserved('/', RESERVED)

# The `Opt` Parser is useful for optional text, such as the else-caluse of an 
# if-statement. It takes one parser as input. If that parser is successful when 
# applied, the result is returned normally. If it fails, a successful result is 
# still returned, but the value of that result is `None`. No tokens are to be 
# consumed in the failing case, the result position is the same as the initial 
# position. 

class Opt(Parser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        result = self.parser(tokens.pos)
        if result:
            return result
        else:
            return Result(None, pos)

# The `Rep` parser applies its input parser repeatedly until it fails. This is 
# useful for generating lists of things. NOTE: `Rep` will successfully match an 
# empty list and consume no tokens if its parser fails the first time it is 
# applied. 

