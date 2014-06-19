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

class Parser:
    def __call__(self, tokens, pos):
        return None # subclasses will override this

    def __add__(self, other):
        return Concat(self, other)

    def __or__(self, other):
        return Alternate(self, other)

    def __xor__(self, function):
        return Process(self, function)
