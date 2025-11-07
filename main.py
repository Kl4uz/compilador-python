from src.lexer import lexer
from src.parser import parser

def compile_code(source_code):
    lexer.input(source_code)
    for token in lexer:
        print(token)
    
    result = parser.parse(source_code, lexer=lexer)
    return result

if __name__ == "__main__":
    with open("tests/hello_world.txt") as f:
        source_code = f.read()

    ast = compile_code(source_code)
    print("AST:", ast)