# 🔄 Guia de Migração - Estrutura Antiga → Nova

Este documento explica as diferenças entre a estrutura antiga (`/src`) e a nova estrutura modular (`/compiler`), e como migrar código.

## 📊 Comparação das Estruturas

### Estrutura Antiga (`/src`)

```
src/
├── lexer.py              # Análise léxica básica
├── parser.py             # Parser com lógica misturada
├── codegen.py            # PROBLEMA: Faz parser + semântica + TAC
├── symbol_table.py       # Tabela de símbolos
├── runtime.py            # Activation records
├── interpreter.py        # Interpretador TAC
└── compiler_etapa7.py    # Integração (duplicação)
```

**Problemas:**
- ❌ `codegen.py` mistura 3 fases diferentes
- ❌ Múltiplos "main" (main.py, codegen.py, compiler_etapa7.py)
- ❌ Sem separação clara de responsabilidades
- ❌ Difícil testar individualmente
- ❌ Sem otimizações
- ❌ Sem geração de assembly

### Nova Estrutura (`/compiler`) ✨

```
compiler/
├── lexer.py           # ÚNICO: Análise léxica
├── parser.py          # ÚNICO: Análise sintática
├── ast.py             # NOVO: Construção de AST
├── analyzer.py        # NOVO: Apenas análise semântica
├── symbol_table.py    # Melhorado: Compatível com analyzer
├── ir.py              # NOVO: Definição de IR/TAC
├── ir_generator.py    # NOVO: Apenas geração de IR
├── optimizer.py       # NOVO: Framework de otimização
├── peephole.py        # NOVO: Otimizações peephole
├── codegen.py         # NOVO: Coordenador de backend
├── assembly.py        # NOVO: Geração de assembly
└── main.py            # ÚNICO PONTO DE ENTRADA
```

**Vantagens:**
- ✅ Cada módulo tem responsabilidade única
- ✅ Fácil testar individualmente
- ✅ Pipeline claro e linear
- ✅ Otimizações modulares
- ✅ Geração de assembly completa
- ✅ Conforme arquitetura do professor

## 🔀 Mapeamento de Funcionalidades

### Tokenização

**Antiga:**
```python
from src.lexer import lexer
lexer.input(codigo)
tokens = list(lexer)
```

**Nova:**
```python
from compiler.lexer import tokenize
tokens = tokenize(codigo)
```

### Parsing

**Antiga:**
```python
from src.parser import parser
from src.lexer import lexer
result = parser.parse(codigo, lexer=lexer)
```

**Nova:**
```python
from compiler.parser import parse_from_code
parse_tree = parse_from_code(codigo)
```

### AST

**Antiga:** ❌ Não existia separadamente (misturado no parser)

**Nova:**
```python
from compiler.ast import build_ast
ast = build_ast(parse_tree)
```

### Análise Semântica

**Antiga:**
```python
# Estava misturada no codegen.py
from src.codegen import infer_type, symbol_table
# Uso complicado e acoplado
```

**Nova:**
```python
from compiler.analyzer import SemanticAnalyzer
analyzer = SemanticAnalyzer()
success, errors, symbol_table = analyzer.analyze(ast)
```

### Geração de TAC

**Antiga:**
```python
# Estava misturada no codegen.py
from src.codegen import generate_tac
tac = generate_tac(node)
```

**Nova:**
```python
from compiler.ir_generator import IRGenerator
ir_gen = IRGenerator(symbol_table)
ir_program = ir_gen.generate(ast)
```

### Pipeline Completo

**Antiga:**
```python
# Tinha que chamar múltiplos arquivos manualmente
from src.lexer import lexer
from src.parser import parser
from src.codegen import generate_tac
# ... código complicado
```

**Nova (SIMPLES!):**
```python
from compiler import compile

result = compile(codigo, optimize=True, verbose=True)

# Resultado contém TUDO:
result['tokens']        # Tokens
result['parse_tree']    # Parse tree
result['ast']           # AST
result['symbol_table']  # Tabela de símbolos
result['ir']            # IR original
result['optimized_ir']  # IR otimizado
result['assembly']      # Assembly
result['errors']        # Erros (se houver)
result['success']       # True/False
```

## 📝 Exemplos de Migração

### Exemplo 1: Compilação Básica

#### Código Antigo (Complexo)
```python
from src.lexer import lexer
from src.parser import parser
from src.codegen import symbol_table, generate_tac

codigo = "int x = 5 + 3;"

# Tokenizar
lexer.input(codigo)
tokens = list(lexer)

# Parsear
parse_tree = parser.parse(codigo, lexer=lexer)

# Gerar TAC (misturado com semântica)
tac_code = generate_tac(parse_tree)

# Imprimir
for instr in tac_code:
    print(instr)
```

#### Código Novo (Simples)
```python
from compiler import compile

codigo = "int x = 5 + 3;"

result = compile(codigo, verbose=True)

if result['success']:
    result['ir'].print_code()
    print("\nAssembly:")
    for linha in result['assembly']:
        print(linha)
```

### Exemplo 2: Análise Semântica

#### Código Antigo (Não existia separado)
```python
# Estava tudo misturado no codegen.py
# Sem forma clara de verificar erros semânticos antes da geração
```

#### Código Novo (Clara separação)
```python
from compiler.parser import parse_from_code
from compiler.ast import build_ast
from compiler.analyzer import SemanticAnalyzer

codigo = """
int main() {
    x = 5;  // ERRO: variável não declarada
    return 0;
}
"""

parse_tree = parse_from_code(codigo)
ast = build_ast(parse_tree)

analyzer = SemanticAnalyzer()
success, errors, symbol_table = analyzer.analyze(ast)

if not success:
    print("Erros encontrados:")
    for error in errors:
        print(f"  - {error}")
else:
    print("Sem erros semânticos!")
```

### Exemplo 3: Otimizações

#### Código Antigo
```python
# ❌ NÃO EXISTIA
```

#### Código Novo
```python
from compiler.parser import parse_from_code
from compiler.ast import build_ast
from compiler.analyzer import SemanticAnalyzer
from compiler.ir_generator import IRGenerator
from compiler.optimizer import Optimizer, ConstantFolding
from compiler.peephole import PeepholeOptimizer

codigo = "int x = 5 + 3;"  # Será otimizado para x = 8

# Pipeline
parse_tree = parse_from_code(codigo)
ast = build_ast(parse_tree)
_, _, symbol_table = SemanticAnalyzer().analyze(ast)

# Gerar IR
ir_gen = IRGenerator(symbol_table)
ir = ir_gen.generate(ast)

print("IR original:")
ir.print_code()

# Otimizar
optimizer = Optimizer()
optimizer.add_optimization(ConstantFolding())
optimizer.add_optimization(PeepholeOptimizer())

optimized = optimizer.optimize(ir)

print("\nIR otimizado:")
optimized.print_code()
```

### Exemplo 4: Assembly

#### Código Antigo
```python
# ❌ NÃO EXISTIA
```

#### Código Novo
```python
from compiler import compile

codigo = """
int main() {
    int x = 5;
    int y = x + 3;
    print(y);
    return 0;
}
"""

result = compile(codigo)

if result['success']:
    print("Assembly gerado:")
    for linha in result['assembly']:
        print(linha)
```

## 🧪 Testes

### Estrutura Antiga
```bash
# Não tinha testes automatizados organizados
```

### Nova Estrutura
```bash
# Suite completa de testes
python test_compiler.py

# Teste individual de módulo
python compiler/lexer.py
python compiler/parser.py
python compiler/analyzer.py
python compiler/optimizer.py
```

## 📦 Importações

### Importar Compilador Antigo
```python
# Múltiplas importações confusas
from src.lexer import lexer
from src.parser import parser
from src.codegen import generate_tac, symbol_table
```

### Importar Compilador Novo
```python
# Uma única importação
from compiler import compile

# Ou importações específicas
from compiler.lexer import tokenize
from compiler.parser import parse_from_code
from compiler.ast import build_ast
from compiler.analyzer import SemanticAnalyzer
```

## 🚀 Vantagens da Nova Estrutura

1. **Modularidade**: Cada fase em arquivo separado
2. **Testabilidade**: Cada módulo testável isoladamente
3. **Clareza**: Pipeline óbvio e linear
4. **Extensibilidade**: Fácil adicionar novas otimizações
5. **Conformidade**: Segue arquitetura do professor
6. **Completude**: Inclui otimizações e assembly
7. **Documentação**: Cada módulo bem documentado
8. **API Simples**: Função `compile()` única

## 🔧 Checklist de Migração

Para migrar código da estrutura antiga para a nova:

- [ ] Substituir `from src.*` por `from compiler.*`
- [ ] Usar `compile()` para pipeline completo
- [ ] Separar lógica em fases distintas
- [ ] Adicionar tratamento de erros semânticos
- [ ] Aproveitar otimizações (opcional)
- [ ] Gerar assembly se necessário
- [ ] Atualizar testes para usar nova API
- [ ] Revisar documentação

## ⚠️ Nota Importante

A estrutura antiga (`/src`) **NÃO** será removida por enquanto para preservar o histórico. Ela fica como **referência** e **backup**. 

**Use sempre `/compiler` para novos desenvolvimentos!**

## 📞 Suporte

Dúvidas sobre migração? Veja:
- `compiler/README.md` - Documentação da nova estrutura
- `docs/GUIA_DE_ESTUDOS.md` - Guia detalhado
- Teste cada módulo individualmente: `python compiler/modulo.py`
