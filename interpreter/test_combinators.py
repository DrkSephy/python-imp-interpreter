import unittest
from imp_lexer import *
from combinators import *

id = Tag(ID)
integer = Tag(INT)
def keyword(s):
    return Reserved(s, RESERVED)

class TestCombinators(unittest.TestCase):
    def combinator_test(self, code, parser, expected):
        tokens = imp_lex(code)
        result = parser(tokens, 0)
        self.assertNotEquals(None, result)
        self.assertEquals(expected, result.value)