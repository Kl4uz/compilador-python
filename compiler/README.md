

## 📂 Estrutura

```
compiler/
│
├── lexer.py           # Análise Léxica (Tokens)
├── parser.py          # ✅ Análise Sintática LL(1) Top-Down
├── main.py            # Pipeline Integrado
│
├── ast/               # Árvore Sintática Abstrata
│   ├── ast_builder.py     # Construtor da AST
│   ├── analyzer.py        # Análise Semântica
│   └── symbol_table.py    # Tabela de Símbolos
│
├── ir/                # Código Intermediário
│   ├── ir.py              # TAC + Quádruplas
│   └── ir_generator.py    # Gerador de IR
│
├── optimizer/         # Otimizações
│   ├── optimizer.py       # ✅ CSE, CF, DCE, CP
│   └── peephole.py        # Peephole + Algebraic Simplification
│
└── codegen/           # Geração de Código
    ├── codegen.py         # Coordenador
    └── assembly.py        # Assembly MIPS-like
```

## 🎯 Pipeline

```
Código Fonte
    ↓
[lexer.py]      → Tokens
    ↓
[parser.py]     → Parse Tree (LL(1) Top-Down)
    ↓
[ast/]          → AST + Análise Semântica
    ↓
[ir/]           → TAC + Quádruplas
    ↓
[optimizer/]    → IR Otimizado (CSE, CF, DCE, etc)
    ↓
[codegen/]      → Assembly MIPS-like
```

## ✅ Conforme Professor Ensinou

- ✅ **Parser LL(1)** com Recursive Descent (`parser.py`)
- ✅ **Lookahead de 1 token**
- ✅ **CSE** - Common Subexpression Elimination (`optimizer/`)
- ✅ **Quádruplas** - Formato (op, arg1, arg2, result) (`ir/ir.py`)
- ✅ **TAC** - Three-Address Code (`ir/ir.py`)
- ✅ **Otimizações** - 6 tipos implementados (`optimizer/`)

## 📖 Uso

```python
from compiler import compile

result = compile(codigo_fonte)
if result['success']:
    print(result['assembly'])
```

## 🔧 Módulos

### `lexer.py`
- Análise léxica com PLY
- Gera tokens a partir do código fonte

### `parser.py`
- **Parser LL(1) Top-Down**
- **Recursive Descent** manual
- Cada não-terminal = função recursiva

### `ast/`
- `ast_builder.py` - Classes de nós da AST
- `analyzer.py` - Análise semântica
- `symbol_table.py` - Gerenciamento de símbolos

### `ir/`
- `ir.py` - Definição de TAC e Quádruplas
- `ir_generator.py` - Converte AST → IR

### `optimizer/`
- `optimizer.py` - Framework + CSE, CF, DCE, CP
- `peephole.py` - Peephole + Simplificação Algébrica

### `codegen/`
- `codegen.py` - Coordena IR → Assembly
- `assembly.py` - Gera Assembly MIPS-like

---

