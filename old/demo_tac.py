"""
DEMONSTRAÇÃO: Geração de Código Intermediário (Código de Três Endereços)
"""

from lexer import lexer
from codegen import parser, generate_tac, print_tac, symbol_table

print("=" * 70)
print("DEMONSTRAÇÃO: GERAÇÃO DE CÓDIGO DE TRÊS ENDEREÇOS (TAC)")
print("=" * 70)

# Teste 1: Atribuições simples
print("\n📝 TESTE 1: Atribuições Simples")
print("-" * 70)

code1 = """
x = 10;
y = 20;
z = 30;
"""

print("Código Fonte:")
print(code1)

ast1 = parser.parse(code1, lexer=lexer)
print("AST Gerada:", ast1)

tac1 = generate_tac(ast1)
print("\n✅ Código TAC (Três Endereços):")
print_tac(tac1)

print(f"\n📊 Tabela de Símbolos: {symbol_table}")

# Resetar para próximo teste
symbol_table.clear()

# Teste 2: Expressões Aritméticas
print("\n\n📝 TESTE 2: Expressões Aritméticas")
print("-" * 70)

code2 = """
a = 5 + 3;
b = 10 - 2;
c = 4 * 6;
d = 20 / 4;
"""

print("Código Fonte:")
print(code2)

ast2 = parser.parse(code2, lexer=lexer)
tac2 = generate_tac(ast2)
print("\n✅ Código TAC (Três Endereços):")
print_tac(tac2)

print(f"\n📊 Tabela de Símbolos: {symbol_table}")

symbol_table.clear()

# Teste 3: Expressões Complexas
print("\n\n📝 TESTE 3: Expressões Complexas (Múltiplas Operações)")
print("-" * 70)

code3 = """
x = 5 + 3 * 2;
y = (10 + 5) * 2;
z = x + y;
"""

print("Código Fonte:")
print(code3)

ast3 = parser.parse(code3, lexer=lexer)
tac3 = generate_tac(ast3)
print("\n✅ Código TAC (Três Endereços):")
print_tac(tac3)

print(f"\n📊 Tabela de Símbolos: {symbol_table}")

symbol_table.clear()

# Teste 4: Com Print
print("\n\n📝 TESTE 4: Expressões com Print")
print("-" * 70)

code4 = """
resultado = 10 + 20 * 2;
print(resultado);
"""

print("Código Fonte:")
print(code4)

ast4 = parser.parse(code4, lexer=lexer)
tac4 = generate_tac(ast4)
print("\n✅ Código TAC (Três Endereços):")
print_tac(tac4)

print(f"\n📊 Tabela de Símbolos: {symbol_table}")

symbol_table.clear()

# Teste 5: Exemplo Completo
print("\n\n📝 TESTE 5: Exemplo Completo (do arquivo code.txt)")
print("-" * 70)

with open("tests/code.txt") as f:
    code5 = f.read()

print("Código Fonte:")
print(code5)

ast5 = parser.parse(code5, lexer=lexer)
tac5 = generate_tac(ast5)
print("\n✅ Código TAC (Três Endereços):")
print_tac(tac5)

print(f"\n📊 Tabela de Símbolos: {symbol_table}")

# Resumo Final
print("\n\n" + "=" * 70)
print("✅ RESUMO: TODAS AS FUNCIONALIDADES IMPLEMENTADAS")
print("=" * 70)

print("""
1. ✅ Geração de código intermediário após análise sintática
2. ✅ Produção de código de três endereços a partir da AST
3. ✅ Testes com atribuições simples
4. ✅ Testes com expressões aritméticas (+, -, *, /)
5. ✅ Testes com expressões complexas (múltiplos operadores)
6. ✅ Variáveis temporárias (t1, t2, t3...) geradas automaticamente
7. ✅ Tabela de símbolos integrada
8. ✅ Análise semântica básica (inferência de tipos)
9. ✅ Preparado para otimizações futuras (formato TAC padrão)

📌 FORMATO TAC (Three Address Code):
   - Cada instrução tem no máximo 3 operandos
   - Formato: resultado = operando1 operador operando2
   - Facilita análise e otimização
   - Base para geração de código assembly/máquina
""")

print("=" * 70)
print("🎉 DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
print("=" * 70)
