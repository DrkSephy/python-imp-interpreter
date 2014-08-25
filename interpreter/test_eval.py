import unittest
from imp_lexer import *
from imp_parser import *

class TestEvaluation(unittest.TestCase):
    def program_test(self, code, expected_env):
        tokens = imp_lex(code)
        result = imp_parse(tokens)
        self.assertNotEquals(None, result)
        program = result.value
        env = {}
        program.eval(env)
        self.assertEquals(expected_env, env)
        