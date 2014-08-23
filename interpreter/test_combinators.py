import unittest
from imp_lexer import *
from combinators import *

id = Tag(ID)
integer = Tag(INT)
def keyword(s):
    return Reserved(s, RESERVED)

class TestCombinators(unittest.TestCase):
    pass