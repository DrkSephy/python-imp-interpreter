/*  Structure of an Interpreter
 *  ---------------------------
 *  In order to represent a program in memory, we build an interpreter 
 *  which is the intermediate representation (IR). We'll be building 
 *  an interpreter for the IMP language, and the intermediate representation
 *  will correspond directly to the syntax of the language. 

 *  We will build a class for each kind of expression or statement. 
 *  In more complicated languages, it is useful to have more than a 
 *  syntactic representation but also a semantic representation which
 *  is easier to analyze and execute. 

 * The interpreter will execute within three stages:
    
    1. Split characters in the source code into tokens.
    2. Organize the tokens into an abstract syntax tree (AST). The AST
       is our intermediate representation.
    3. Evaluate the AST and print the state at the end of execution.
*/

/*  Writing a Lexer 
 *  ---------------
 *  The process of splitting characters into tokens is called lexing and 
 *  is performed by a lexer. Tokens are short strings that contain the most
 *  basic parts of the program such as numbers, identifiers, keywords and 
 *  operators. Our lexer will ignore whitespace and comments, because they are
 *  ignored by the interpreter. 

                        y:= x * 2 + 3 
                              |
                              |
                              V
                            LEXER

                 [y] [:=] [x] [*] [2] [+] [3]

  * The process of organizing tokens into an abstract syntax tree is called
  * parsing. The parser extracts the structure of the program into a form
  * we can evaluate. 

  * The process of actually executing the parsed AST is called evaluation. 



*/