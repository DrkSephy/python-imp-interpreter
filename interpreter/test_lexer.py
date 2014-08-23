import unittest
from lexer import *

KEYWORD = 'KEYWORD'
INT = 'INT'
ID = 'ID'
token_exprs = [
    (r'[ \t\n]+', None),
    (r'#[^\n]*', None),
    (r'keyword', KEYWORD),
    (r'[0-9]+', INT),
    (r'[A-Za-z][A-Za-z0-9_]*', ID)
]

class TestLexer(unittest.TestCase):
    def lexer_test(self, code, expected):
        actual = lex(code, token_exprs)
        self.assertEquals(expected, actual)

    def test_empty(self):
        self.lexer_test('', [])

    

        
    
    
