from lexer import lexer

code = "int soma(int a)"
lexer.input(code)

for tok in lexer:
    print(tok)
