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