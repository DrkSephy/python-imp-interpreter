# lexer.py 
# --------
# The input to the lexer will be a stream of characters. 
# We will read an entire input file into memory, and the 
# output will be a list of tokens. Each token comprises a
# value (the string it represents) and a tag (to indicate
# what kind of token it is). The parser will use these to 
# decide how to create the AST. 

# Since writing a lexer for any language is pretty similar, 
# we will create a generic lexer using a list of regular 
# expressions and corresponding tags. 

# Algorithm:
#   
# 1. For each expression, the lexer will check whether the input
#    text matches at the current position.
# 2. If a match is found, the matching text is extracted into a 
#    token, along with the regular expression's tag.
# 3. If the regular expression has no tag associated with it, the 
#    text is discarded (like whitespace or comments). 
# 4. If there is no matching regex, we report an error and quit. 
# 5. Repeat until there are no more characters left to match. 

import sys
import re

def lex(characters, token_exprs):
    pos = 0
    tokens = []
    while pos < len(characters):
        match = None
        for token_expres in token_exprs: 
            pattern, tag = token_exprs
            regex = re.compile(pattern)
            match = regex.match(characters, pos)
            if match:
                text = match.group(0)
                if tag:
                    token = (text, tag)
                    tokens.append(token)
                break
            if not match:
                sys.stderr.write('Illegal character: %s\\n' % characters[pos])
                sys.exit(1)
            else:
                pos = match.end(0)
    return tokens 