# Pipeline de Compilação

Este documento descreve o pipeline completo de compilação implementado no projeto.

## Visão Geral

O compilador segue um pipeline tradicional de múltiplas fases:

```
Código Fonte → Lexer → Parser → Semantic → IR Generator → Optimizer → Assembly Generator
```

## Fases do Pipeline

### 1. Análise Léxica (Lexer)

**Módulo:** `src/lexer.py`

A análise léxica converte o código fonte em uma sequência de tokens.

**Entrada:** Código fonte (string)
**Saída:** Lista de tokens

**Função principal:**
```python
from src.lexer import tokenize
tokens = tokenize(source_code)
```

**Tokens suportados:**
- Palavras reservadas: `if`, `else`, `while`, `return`, `int`, `print`
- Operadores: `+`, `-`, `*`, `/`, `=`
- Delimitadores: `(`, `)`, `{`, `}`, `;`, `,`
- Literais: números inteiros
- Identificadores: variáveis e funções

### 2. Análise Sintática (Parser)

**Módulo:** `src/parser.py`

A análise sintática constrói uma Árvore de Sintaxe Abstrata (AST) a partir dos tokens.

**Entrada:** Lista de tokens
**Saída:** AST (formato tupla, convertida para ASTNode)

**Função principal:**
```python
from src.parser import parse
ast = parse(source_code)
```

**Estrutura da AST:**
- Nós representam elementos sintáticos (programa, função, expressão, etc.)
- Formato inicial: tuplas (compatibilidade)
- Formato final: ASTNode (estrutura de classes)

### 3. Análise Semântica (Semantic Analyzer)

**Módulo:** `src/semantic.py`

A análise semântica verifica:
- Declaração de variáveis e funções
- Tipos e compatibilidade de tipos
- Escopos e visibilidade
- Uso correto de identificadores

**Entrada:** AST
**Saída:** AST anotada + erros/avisos

**Uso:**
```python
from src.semantic import SemanticAnalyzer
from src.symbol_table import SymbolTable

symbol_table = SymbolTable()
analyzer = SemanticAnalyzer(symbol_table)
success = analyzer.analyze(ast)
```

**Verificações realizadas:**
- Variáveis declaradas antes do uso
- Tipos compatíveis em operações
- Funções declaradas antes da chamada
- Parâmetros corretos
- Divisão por zero (constantes)

### 4. Geração de Código Intermediário (IR Generator)

**Módulo:** `src/ir_generator.py`

Gera código intermediário no formato TAC (Three-Address Code).

**Entrada:** AST
**Saída:** Lista de instruções IR

**Uso:**
```python
from src.ir_generator import IRGenerator

generator = IRGenerator(symbol_table)
ir_instructions = generator.generate(ast)
```

**Formato TAC:**
```
FUNCTION main:
BEGIN_FUNC
t1 = 2 + 3
x = t1
PRINT x
RETURN 0
END_FUNC
```

**Instruções suportadas:**
- Atribuição: `x = y`
- Operações binárias: `t1 = a + b`
- Chamadas de função: `t1 = CALL func, 2`
- Controle: `FUNCTION`, `BEGIN_FUNC`, `END_FUNC`, `RETURN`
- I/O: `PRINT`

### 5. Otimização (Optimizer)

**Módulo:** `src/optimizer.py`

Aplica otimizações no código intermediário.

**Entrada:** Lista de instruções IR
**Saída:** Lista de instruções IR otimizadas

**Uso:**
```python
from src.optimizer import Optimizer

optimizer = Optimizer()
optimized_ir = optimizer.optimize(ir_instructions)
```

**Otimizações implementadas:**
- **Constant Folding:** Avalia expressões constantes em tempo de compilação
  - `t1 = 5 + 3` → `t1 = 8`
- **Remoção de Atribuições Redundantes:** Remove `x = x`
- **Remoção de Temporários Não Utilizados:** Remove variáveis temporárias que não são usadas
- **Remoção de Código Morto:** Remove código após return inalcançável

### 6. Geração de Assembly (Assembly Generator)

**Módulo:** `src/assembly_generator.py`

Converte código intermediário em código assembly (opcional).

**Entrada:** Lista de instruções IR
**Saída:** Código assembly

**Uso:**
```python
from src.assembly_generator import AssemblyGenerator

generator = AssemblyGenerator(target_arch="x86_64")
assembly = generator.generate(ir_instructions)
```

**Arquitetura suportada:**
- x86_64 (Linux)

## Pipeline Principal

**Módulo:** `src/compiler.py`

O módulo `Compiler` orquestra todas as fases:

```python
from src.compiler import Compiler

compiler = Compiler(optimize=True, generate_assembly=False)
result = compiler.compile(source_code)
```

**Resultado:**
```python
{
    "success": bool,
    "ast": ASTNode,
    "ir": List[IRInstruction],
    "optimized_ir": List[IRInstruction],
    "assembly": List[str],
    "symbol_table": SymbolTable,
    "errors": List[str],
    "warnings": List[str]
}
```

## Exemplo de Uso Completo

```python
from src.compiler import Compiler

code = """
int soma(int a, int b) {
    int r = a + b;
    return r;
}

int main() {
    int x = soma(2, 3);
    print(x);
    return 0;
}
"""

compiler = Compiler(optimize=True)
result = compiler.compile(code)

if result["success"]:
    print("Compilação bem-sucedida!")
    compiler.print_results(result)
else:
    print("Erros encontrados:")
    for error in result["errors"]:
        print(f"  - {error}")
```

## Interface de Linha de Comando

```bash
python main.py arquivo.txt -o saida.ir --optimize --verbose
```

**Opções:**
- `-o, --output`: Arquivo de saída
- `--no-optimize`: Desabilita otimizações
- `--assembly`: Gera código assembly
- `-v, --verbose`: Modo verboso

## Estrutura de Módulos

```
src/
├── lexer.py              # Análise léxica
├── parser.py              # Análise sintática
├── ast_builder.py         # Construtor de AST
├── semantic.py            # Análise semântica
├── symbol_table.py        # Tabela de símbolos
├── ir_generator.py        # Geração de IR
├── optimizer.py            # Otimização
├── assembly_generator.py  # Geração de assembly
└── compiler.py            # Pipeline principal
```

## Fluxo de Dados

```
Código Fonte
    ↓
[Lexer] → Tokens
    ↓
[Parser] → AST (tupla)
    ↓
[AST Builder] → AST (ASTNode)
    ↓
[Semantic Analyzer] → AST anotada
    ↓
[IR Generator] → Código IR
    ↓
[Optimizer] → Código IR otimizado
    ↓
[Assembly Generator] → Código Assembly (opcional)
```

## Tratamento de Erros

Cada fase pode gerar erros:
- **Léxico:** Caracteres ilegais
- **Sintático:** Erros de sintaxe
- **Semântico:** Erros de tipos, escopo, etc.
- **IR:** Erros na geração de código
- **Otimização:** Avisos sobre otimizações não aplicadas

Todos os erros são coletados e retornados no resultado final.

## Testes

Execute os testes do pipeline:

```bash
python src/test_pipeline.py
```

Os testes cobrem:
1. Análise léxica isolada
2. Análise sintática isolada
3. Análise semântica isolada
4. Geração de IR isolada
5. Otimização isolada
6. Pipeline completo
7. Casos de erro

