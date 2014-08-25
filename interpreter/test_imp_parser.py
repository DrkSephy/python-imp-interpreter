import unittest
from imp_lexer import *
from imp_parser import *

class TestImpParser(unittest.TestCase):
    def parser_test(self, code, parser, expected):
        tokens = imp_lex(code)
        result = parser(tokens, 0)
        self.assertNotEquals(None, result)
        self.assertEquals(expected, result.value)

    def test_precedence(self):
        def combine(op):
            if op == '*':
                return lambda l, r: int(l) * int(r)
            else:
                return lambda l, r: int(l) + int(r)
            levels = [['*'], ['+']]
            parser = precedence(num, levels, combine)
            self.parser_test('2 * 3 + 4', parser, 10)
            self.parser_test('2 + 3 * 4', parser, 14)

    def test_aexp_num(self):
        self.parser_test('12', aexp(), IntAexp(12))

    def test_aexp_var(self):
        self.parser_test('x', aexp(), VarAexp('x'))

    def test_aexp_group(self):
        self.parser_test('(12)', aexp(), IntAexp(12))