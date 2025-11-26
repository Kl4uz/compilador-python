# Documentação dos Módulos

Este documento descreve cada módulo do compilador em detalhes.

## Módulos Principais

### `lexer.py` - Analisador Léxico

**Responsabilidade:** Tokenização do código fonte

**Classes/Funções principais:**
- `tokenize(source_code: str) -> List[Token]`: Tokeniza o código fonte

**Tokens suportados:**
- Palavras reservadas: `if`, `else`, `while`, `return`, `int`, `print`
- Operadores: `+`, `-`, `*`, `/`, `=`
- Delimitadores: `(`, `)`, `{`, `}`, `;`, `,`
- Literais: números inteiros
- Identificadores: variáveis e funções

**Exemplo:**
```python
from src.lexer import tokenize

tokens = tokenize("int x = 5;")
# Retorna lista de tokens: [INT, ID('x'), EQUALS, NUMBER(5), SEMICOLON]
```

---

### `parser.py` - Analisador Sintático

**Responsabilidade:** Construção da AST a partir dos tokens

**Classes/Funções principais:**
- `parse(source_code: str) -> tuple`: Analisa sintaticamente e retorna AST em formato tupla

**Gramática suportada:**
- Declarações de funções
- Declarações de variáveis
- Expressões aritméticas
- Chamadas de função
- Statements: atribuição, return, print

**Exemplo:**
```python
from src.parser import parse

ast = parse("int x = 5 + 3;")
# Retorna: ('program', [('assign', 'x', ('+', ('num', 5), ('num', 3)))])
```

---

### `ast_builder.py` - Construtor de AST

**Responsabilidade:** Fornece classes e métodos para construir AST estruturada

**Classes principais:**
- `ASTNode`: Classe base para nós da AST
- `ASTBuilder`: Factory para criar nós da AST

**Métodos principais:**
- `create_program_node()`
- `create_function_node()`
- `create_assignment_node()`
- `create_binary_operation_node()`
- `tuple_to_ast()`: Converte formato tupla para ASTNode
- `ast_to_tuple()`: Converte ASTNode para formato tupla (legado)

**Exemplo:**
```python
from src.ast_builder import ASTBuilder

builder = ASTBuilder()
num1 = builder.create_number_node(5)
num2 = builder.create_number_node(3)
add = builder.create_binary_operation_node("+", num1, num2)
assign = builder.create_assignment_node("x", add)
```

---

### `semantic.py` - Analisador Semântico

**Responsabilidade:** Verificação semântica da AST

**Classes principais:**
- `SemanticAnalyzer`: Realiza análise semântica

**Verificações realizadas:**
- Declaração de variáveis antes do uso
- Tipos compatíveis em operações
- Funções declaradas antes da chamada
- Parâmetros corretos
- Divisão por zero (constantes)
- Escopos e visibilidade

**Exemplo:**
```python
from src.semantic import SemanticAnalyzer
from src.symbol_table import SymbolTable

symbol_table = SymbolTable()
analyzer = SemanticAnalyzer(symbol_table)
success = analyzer.analyze(ast)

if not success:
    for error in analyzer.errors:
        print(f"Erro: {error}")
```

---

### `symbol_table.py` - Tabela de Símbolos

**Responsabilidade:** Gerenciamento de símbolos e escopos

**Classes principais:**
- `Symbol`: Representa um símbolo (variável, função, parâmetro)
- `Scope`: Representa um escopo (global ou função)
- `SymbolTable`: Tabela de símbolos com suporte a escopos aninhados

**Funcionalidades:**
- Inserção de símbolos
- Busca de símbolos (escopo léxico)
- Gerenciamento de escopos aninhados
- Cálculo de offsets para activation records

**Exemplo:**
```python
from src.symbol_table import SymbolTable

st = SymbolTable()
st.insert("x", "int")
st.enter_scope("func")
st.insert("y", "int", is_param=True)
symbol = st.lookup("x")  # Busca em escopo atual e pais
```

---

### `ir_generator.py` - Gerador de Código Intermediário

**Responsabilidade:** Geração de código TAC (Three-Address Code)

**Classes principais:**
- `IRInstruction`: Representa uma instrução IR
- `IRGenerator`: Gera código IR a partir da AST

**Formato TAC:**
```
FUNCTION main:
BEGIN_FUNC
t1 = 5 + 3
x = t1
PRINT x
RETURN 0
END_FUNC
```

**Exemplo:**
```python
from src.ir_generator import IRGenerator

generator = IRGenerator(symbol_table)
ir = generator.generate(ast)
generator.print_ir()
```

---

### `optimizer.py` - Otimizador

**Responsabilidade:** Otimização do código intermediário

**Classes principais:**
- `Optimizer`: Aplica otimizações no código IR

**Otimizações implementadas:**
- **Constant Folding:** `t1 = 5 + 3` → `t1 = 8`
- **Remoção de Atribuições Redundantes:** Remove `x = x`
- **Remoção de Temporários Não Utilizados**
- **Remoção de Código Morto**

**Exemplo:**
```python
from src.optimizer import Optimizer

optimizer = Optimizer()
optimized_ir = optimizer.optimize(ir_instructions)
print(optimizer.get_optimization_report())
```

---

### `assembly_generator.py` - Gerador de Assembly

**Responsabilidade:** Geração de código assembly a partir do IR

**Classes principais:**
- `AssemblyGenerator`: Gera código assembly

**Arquiteturas suportadas:**
- x86_64 (Linux)

**Exemplo:**
```python
from src.assembly_generator import AssemblyGenerator

generator = AssemblyGenerator(target_arch="x86_64")
assembly = generator.generate(ir_instructions)
generator.print_assembly()
```

---

### `compiler.py` - Pipeline Principal

**Responsabilidade:** Orquestração de todas as fases de compilação

**Classes principais:**
- `Compiler`: Pipeline principal do compilador
- `CompilationError`: Exceção para erros de compilação

**Fases executadas:**
1. Análise Léxica
2. Análise Sintática
3. Análise Semântica
4. Geração de IR
5. Otimização (opcional)
6. Geração de Assembly (opcional)

**Exemplo:**
```python
from src.compiler import Compiler

compiler = Compiler(optimize=True, generate_assembly=False)
result = compiler.compile(source_code)

if result["success"]:
    compiler.print_results(result)
```

---

## Módulos Auxiliares

### `runtime.py` - Runtime Stack

**Responsabilidade:** Simulação de ambiente de execução

**Classes principais:**
- `ActivationRecord`: Registro de ativação (stack frame)
- `RuntimeStack`: Pilha de execução

**Funcionalidades:**
- Gerenciamento de activation records
- Resolução de variáveis via dynamic link
- Memória global e local

---

### `interpreter.py` - Interpretador TAC

**Responsabilidade:** Execução de código TAC

**Classes principais:**
- `Interpreter`: Interpreta e executa código TAC

**Funcionalidades:**
- Execução de instruções TAC
- Chamadas de função
- Gerenciamento de pilha de execução

---

## Fluxo de Dados Entre Módulos

```
source_code
    ↓
[lexer.py] → tokens
    ↓
[parser.py] → AST (tupla)
    ↓
[ast_builder.py] → AST (ASTNode)
    ↓
[semantic.py] + [symbol_table.py] → AST anotada
    ↓
[ir_generator.py] → IR
    ↓
[optimizer.py] → IR otimizado
    ↓
[assembly_generator.py] → Assembly
```

## Dependências Entre Módulos

```
compiler.py
├── lexer.py
├── parser.py
├── semantic.py
│   └── symbol_table.py
├── ir_generator.py
│   ├── ast_builder.py
│   └── symbol_table.py
├── optimizer.py
│   └── ir_generator.py
└── assembly_generator.py
    └── ir_generator.py
```

## Convenções de Código

- **Imports:** Use imports relativos dentro de `src/` (`.module`)
- **Tipos:** Use type hints quando possível
- **Documentação:** Docstrings em todas as classes e funções públicas
- **Erros:** Use exceções específicas (`CompilationError`)

