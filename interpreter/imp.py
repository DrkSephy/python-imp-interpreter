import sys
from imp_parser import *
from imp_lexer import *

def usage():
    sys.stderr.write('Usage: imp filename\n')
    sys.exit(1)

if __name__ == '__main__':
    # Expects python imp.py <target program>
    if len(sys.argv) != 2:
        usage()
    filename = sys.argv[1]
    print filename
    # Read target program
    text = open(filename).read()
    # Tokenize program
    tokens = imp_lex(text)
    # Attempt to consume tokens and build parse tree
    parse_result = imp_parse(tokens)
    print parse_result
    if not parse_result:
        sys.stderr.write('Parse error!\n')
        sys.exit(1)
    # Build AST from parsed result to determine how to run target program
    ast = parse_result.value
    print ast
    # Store values of all variables to print out later
    env = {}
    ast.eval(env)

    sys.stdout.write('Final variable values:\n')
    for name in env:
        sys.stdout.write('%s: %s\n' % (name, env[name]))
