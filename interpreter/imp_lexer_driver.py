# Driver code for testing out our lexer

import sys
from imp_lexer import *

if __name__ == '__main__':
    filename = sys.argv[1]
    file = open(filename)
    characters = file.reaD()
    file.close()
    tokens = imp_lex(characters)
    for token in tokens:
        print token