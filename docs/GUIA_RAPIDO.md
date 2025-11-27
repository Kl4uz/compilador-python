# 📖 Guia Rápido de Referência

Referência rápida para usar o compilador no dia a dia.

## 🚀 Início Rápido (5 minutos)

```bash
# 1. Instalar
pip install ply

# 2. Testar
python test_compiler.py

# 3. Demonstração
python demo_completo.py
```

## 💻 Uso Básico

### Método 1: API Python (Recomendado)

```python
from compiler import compile

codigo = """
int main() {
    int x = 10;
    print(x);
    return 0;
}
"""

result = compile(codigo)

if result['success']:
    print("✓ OK!")
else:
    print("✗ Erros:", result['errors'])
```

### Método 2: Linha de Comando

```bash
# Compilar arquivo
python compiler/main.py tests/hello_world.txt

# Com detalhes
python compiler/main.py tests/hello_world.txt --verbose

# Salvar assembly
python compiler/main.py tests/code.txt -o output.asm

# Sem otimizações
python compiler/main.py tests/code.txt --no-optimize
```

## 📦 O Que Vem no `result`

```python
result = compile(codigo)

result['success']         # True/False
result['tokens']          # Lista de tokens
result['parse_tree']      # Parse tree
result['ast']             # AST
result['symbol_table']    # Tabela de símbolos
result['ir']              # IR original
result['optimized_ir']    # IR otimizado
result['assembly']        # Assembly
result['errors']          # Lista de erros
```

## 🔧 Opções do `compile()`

```python
compile(
    source_code,           # Código fonte (obrigatório)
    optimize=True,         # Habilitar otimizações
    verbose=False          # Imprimir detalhes
)
```

## 📝 Sintaxe Suportada

```c
// Declaração de função
int nome_funcao(int param1, int param2) {
    // corpo
    return valor;
}

// Variáveis
int x = 5;

// Operações
int y = x + 3 * 2;

// Atribuição
x = y - 10;

// Chamada de função
int z = soma(x, y);

// Print
print(z);

// Return
return z;
```

## 🧪 Testando Módulos Individuais

```bash
# Cada módulo pode ser testado:
python compiler/lexer.py
python compiler/parser.py
python compiler/ast.py
python compiler/analyzer.py
python compiler/ir_generator.py
python compiler/optimizer.py
python compiler/peephole.py
python compiler/assembly.py
python compiler/codegen.py
```

## 🐛 Debugging

### Ver Tokens
```python
from compiler.lexer import tokenize

tokens = tokenize(codigo)
for tok in tokens:
    print(tok)
```

### Ver Parse Tree
```python
from compiler.parser import parse_from_code

tree = parse_from_code(codigo)
print(tree)
```

### Ver AST
```python
from compiler.parser import parse_from_code
from compiler.ast import build_ast, print_ast

tree = parse_from_code(codigo)
ast = build_ast(tree)
print_ast(ast)
```

### Ver Erros Semânticos
```python
from compiler.parser import parse_from_code
from compiler.ast import build_ast
from compiler.analyzer import SemanticAnalyzer

tree = parse_from_code(codigo)
ast = build_ast(tree)

analyzer = SemanticAnalyzer()
success, errors, symbol_table = analyzer.analyze(ast)

if not success:
    for error in errors:
        print(f"Erro: {error}")
```

### Ver IR
```python
from compiler import compile

result = compile(codigo)
result['ir'].print_code()
```

### Ver IR Otimizado
```python
from compiler import compile

result = compile(codigo, optimize=True)
result['optimized_ir'].print_code()
```

### Ver Assembly
```python
from compiler import compile

result = compile(codigo)
for linha in result['assembly']:
    print(linha)
```

## 📊 Exemplos Prontos

### Hello World
```python
from compiler import compile

codigo = """
int main() {
    int x = 42;
    print(x);
    return 0;
}
"""

result = compile(codigo, verbose=True)
```

### Com Função
```python
from compiler import compile

codigo = """
int soma(int a, int b) {
    return a + b;
}

int main() {
    int x = soma(5, 3);
    print(x);
    return 0;
}
"""

result = compile(codigo, verbose=True)
```

### Testando Otimizações
```python
from compiler import compile

codigo = """
int main() {
    int x = 5 + 3;     // Será otimizado para x = 8
    int y = x * 1;     // Será otimizado para y = x
    int z = y + 0;     // Será otimizado para z = y
    print(z);
    return 0;
}
"""

# Sem otimizações
result1 = compile(codigo, optimize=False)
print("IR sem otimizar:")
result1['ir'].print_code()

# Com otimizações
result2 = compile(codigo, optimize=True)
print("\nIR otimizado:")
result2['optimized_ir'].print_code()
```

## 🎯 Casos de Uso Comuns

### Caso 1: Verificar se código compila
```python
from compiler import compile

result = compile(codigo)
if result['success']:
    print("✓ Código válido")
else:
    print("✗ Erros encontrados:")
    for error in result['errors']:
        print(f"  - {error}")
```

### Caso 2: Gerar assembly de arquivo
```python
from compiler import compile_file

result = compile_file("meu_codigo.txt")
if result['success']:
    with open("output.asm", "w") as f:
        for linha in result['assembly']:
            f.write(linha + "\n")
    print("Assembly salvo em output.asm")
```

### Caso 3: Comparar com e sem otimização
```python
from compiler import compile

sem = compile(codigo, optimize=False)
com = compile(codigo, optimize=True)

instrucoes_antes = len(sem['ir'].get_instructions())
instrucoes_depois = len(com['optimized_ir'].get_instructions())

print(f"Antes: {instrucoes_antes} instruções")
print(f"Depois: {instrucoes_depois} instruções")
print(f"Redução: {instrucoes_antes - instrucoes_depois} instruções")
```

### Caso 4: Analisar tabela de símbolos
```python
from compiler import compile

result = compile(codigo)
if result['success']:
    result['symbol_table'].print_table()
```

## ⚠️ Erros Comuns

### Erro: "Variável não declarada"
```c
int main() {
    x = 5;  // ERRO: int x = 5;
    return 0;
}
```

### Erro: "Função não declarada"
```c
int main() {
    int x = foo(5);  // ERRO: função foo não existe
    return 0;
}
```

### Erro: "Número errado de argumentos"
```c
int soma(int a, int b) {
    return a + b;
}

int main() {
    int x = soma(5);  // ERRO: faltou segundo argumento
    return 0;
}
```

### Erro: "Função deve ter return"
```c
int calcular(int x) {
    int y = x + 1;
    // ERRO: faltou return
}
```

## 📚 Documentação Completa

- `compiler/README.md` - Arquitetura detalhada
- `docs/GUIA_DE_ESTUDOS.md` - Guia de estudos completo
- `MIGRACAO.md` - Migração da estrutura antiga
- `RESUMO_REESTRUTURACAO.md` - Resumo do que foi feito

## 🆘 Ajuda

### Problema: "Import error"
```bash
# Certifique-se que está no diretório raiz
cd compilador-python
python -c "from compiler import compile; print('OK')"
```

### Problema: "PLY not found"
```bash
pip install ply
```

### Problema: "parsetab.py conflicts"
```bash
# Remova cache do PLY
rm compiler/parsetab.py
rm src/parsetab.py
```

## 🎓 Para Aprender

1. **Comece com**: `demo_completo.py`
2. **Depois leia**: `compiler/README.md`
3. **Estude cada módulo**: `python compiler/modulo.py`
4. **Teste**: `python test_compiler.py`
5. **Aprofunde**: `docs/GUIA_DE_ESTUDOS.md`

## ⚡ Atalhos Úteis

```bash
# Testar tudo
python test_compiler.py

# Demo interativa
python demo_completo.py

# Compilar arquivo rapidamente
python compiler/main.py arquivo.txt -v

# Ver apenas IR
python -c "from compiler import compile; compile('int main(){return 0;}')['ir'].print_code()"

# Ver apenas erros
python -c "from compiler import compile; print(compile('int main(){x=5;return 0;}')['errors'])"
```

## 🏁 Checklist para Apresentação

- [ ] Instalar dependências: `pip install ply`
- [ ] Rodar testes: `python test_compiler.py` (todos devem passar)
- [ ] Testar demo: `python demo_completo.py`
- [ ] Compilar exemplo: `python compiler/main.py tests/hello_world.txt -v`
- [ ] Verificar estrutura: todos os 13 módulos em `/compiler`
- [ ] Ler documentação: `compiler/README.md`

---

**Dúvidas?** Veja a documentação completa em `compiler/README.md`
