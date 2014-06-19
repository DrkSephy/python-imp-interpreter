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

