"""
Testa o compilador com o exemplo de chamadas aninhadas
Usa o novo pipeline de compilação
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.compiler import Compiler
from src.interpreter import TACInterpreter

# Lê o código
with open("tests/test_nested_calls.txt") as f:
    code = f.read()

print("=" * 60)
print("CÓDIGO FONTE:")
print("=" * 60)
print(code)

print("\n" + "=" * 60)
print("COMPILANDO:")
print("=" * 60)

# Compila usando o novo pipeline
compiler = Compiler(optimize=False)
result = compiler.compile(code)

if not result["success"]:
    print("ERROS NA COMPILAÇÃO:")
    for error in result["errors"]:
        print(f"  - {error}")
    sys.exit(1)

# Converte IR para formato de lista de strings (compatível com interpretador)
ir_instructions = result["ir"]
tac_code = []
for instr in ir_instructions:
    if instr.op == "END_FUNC":
        tac_code.append(str(instr))
        tac_code.append("")  # Linha em branco
    elif instr.op and (instr.op != "=" or instr.result):
        tac_code.append(str(instr))

# Imprime TAC
print("\nCÓDIGO TAC:")
print("-" * 60)
for line in tac_code:
    print(line)

# Executa
print("\n" + "=" * 60)
print("EXECUÇÃO:")
print("=" * 60)
interpreter = TACInterpreter(tac_code)
interpreter.execute()

# Estado final
print("\n" + "=" * 60)
print("ESTADO FINAL:")
print("=" * 60)
interpreter.runtime.print_stack()
