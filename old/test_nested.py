"""
Testa o compilador com o exemplo de chamadas aninhadas
"""

from lexer import lexer
from compiler_etapa7 import parser, Compiler, Interpreter

with open("../tests/test_nested_calls.txt") as f:
    code = f.read()

print("=" * 60)
print("CÓDIGO FONTE:")
print("=" * 60)
print(code)

print("\n" + "=" * 60)
print("COMPILANDO E EXECUTANDO:")
print("=" * 60)

# Parse
ast = parser.parse(code, lexer=lexer)

# Compila
compiler = Compiler()
tac = compiler.compile(ast)

# Imprime TAC
print("\nCÓDIGO TAC:")
print("-" * 60)
for line in tac:
    if line:
        print(line)

# Executa
print("\n" + "=" * 60)
print("EXECUÇÃO:")
print("=" * 60)
interpreter = Interpreter(tac)
interpreter.run()

# Estado final
print("\n" + "=" * 60)
print("ESTADO FINAL:")
print("=" * 60)
interpreter.runtime.print_stack()
