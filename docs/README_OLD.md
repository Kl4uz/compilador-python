# 🚀 Mini Compilador em Python

Bem-vindo ao repositório do **Mini Compilador em Python**, um projeto acadêmico completo desenvolvido para a disciplina de Compiladores. 

Este projeto implementa um **compilador completo** para uma mini-linguagem C-like, cobrindo todas as fases: **análise léxica, sintática, semântica, geração de código intermediário, otimizações e geração de assembly**.

## 📚 Sobre o Projeto

Compilador educacional que transforma código fonte em assembly MIPS-like, passando por todas as etapas clássicas de compilação com arquitetura modular e bem documentada.

### ✨ Características

- ✅ **Pipeline completo** de compilação
- ✅ **Separação clara** de fases (léxico → sintático → semântico → IR → otimização → assembly)
- ✅ **Otimizações** (constant folding, dead code elimination, peephole)
- ✅ **Análise semântica** robusta com detecção de erros
- ✅ **Suporte a funções** e chamadas aninhadas
- ✅ **Código intermediário** (Three-Address Code - TAC)
- ✅ **Geração de assembly** MIPS-like
- ✅ **Totalmente testável** (cada módulo independente)

### 👥 Equipe

- Lucas Farias
- José Lucas
- Ester Araiz
- Henrique Noronha

## 📁 Estrutura do Repositório

### 🆕 Nova Estrutura Modular (`/compiler`)

```
compilador-python/
├── README.md                    # Este arquivo
├── requirements.txt             # Dependências
├── test_compiler.py             # Suite completa de testes
│
├── compiler/                    # ⭐ COMPILADOR MODULAR (NOVO)
│   ├── README.md                # Documentação detalhada
│   ├── __init__.py              # Pacote Python
│   ├── main.py                  # 🎯 Pipeline unificado
│   ├── lexer.py                 # Etapa 2-3: Análise léxica
│   ├── parser.py                # Etapa 4: Análise sintática
│   ├── ast.py                   # Construção da AST
│   ├── analyzer.py              # Etapa 5: Análise semântica
│   ├── symbol_table.py          # Tabela de símbolos
│   ├── ir.py                    # Definição de IR (TAC)
│   ├── ir_generator.py          # Etapa 6: Geração de IR
│   ├── optimizer.py             # Framework de otimização
│   ├── peephole.py              # Otimizações peephole
│   ├── codegen.py               # Coordenador de geração
│   └── assembly.py              # Etapa 7: Geração de assembly
│
├── src/                         # Implementação original (legado)
│   ├── lexer.py
│   ├── parser.py
│   ├── codegen.py
│   ├── symbol_table.py
│   ├── runtime.py
│   ├── interpreter.py
│   └── compiler_etapa7.py
│
├── tests/                       # Arquivos de teste
│   ├── hello_world.txt
│   ├── code.txt
│   ├── test_functions.txt
│   └── test_nested_calls.txt
│
└── docs/                        # Documentação
    ├── GUIA_DE_ESTUDOS.md       # Guia completo de estudos
    ├── ETAPA7_AMBIENTES_EXECUCAO.md
    └── RESUMO_ETAPA7.md
```

## 🚀 Início Rápido

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/Kl4uz/compilador-python.git
cd compilador-python

# 2. Instale as dependências
pip install -r requirements.txt
```

### Uso Básico

#### Via Python (Recomendado)

```python
from compiler import compile

# Seu código
codigo = """
int soma(int a, int b) {
    return a + b;
}

int main() {
    int resultado = soma(5, 3);
    print(resultado);
    return 0;
}
"""

# Compilar
result = compile(codigo, optimize=True, verbose=True)

if result['success']:
    print("✓ Compilação bem-sucedida!")
    for linha in result['assembly']:
        print(linha)
else:
    print("✗ Erros:", result['errors'])
```

#### Via Linha de Comando

```bash
# Compilar arquivo
python compiler/main.py tests/hello_world.txt --verbose

# Salvar assembly
python compiler/main.py tests/code.txt -o output.asm

# Sem otimizações
python compiler/main.py tests/code.txt --no-optimize
```

### Testes

```bash
# Rodar suite completa de testes
python test_compiler.py

# Testar módulo individual
python compiler/lexer.py
python compiler/parser.py
python compiler/optimizer.py
```

## 📦 Dependências

- **Python 3.8+**: Linguagem principal
- **PLY (Python Lex-Yacc) 3.11**: Análise léxica e sintática
- **pytest**: Testes (opcional)

```bash
pip install ply
```

## 🔄 Pipeline de Compilação

```
   Código Fonte (.txt)
         ↓
   [1] LEXER (lexer.py)
       → Tokenização
         ↓
   [2] PARSER (parser.py)
       → Parse Tree (BNF)
         ↓
   [3] AST Builder (ast.py)
       → Abstract Syntax Tree
         ↓
   [4] ANALYZER (analyzer.py)
       → Análise Semântica
       → Symbol Table
         ↓
   [5] IR GENERATOR (ir_generator.py)
       → Three-Address Code (TAC)
         ↓
   [6] OPTIMIZER (optimizer.py + peephole.py)
       → Constant Folding
       → Dead Code Elimination
       → Copy Propagation
       → Peephole Optimization
         ↓
   [7] ASSEMBLY GENERATOR (assembly.py)
       → Código MIPS-like
         ↓
    Assembly (.asm)
```

## ✅ Etapas Implementadas

| Etapa | Descrição | Status | Módulo |
|-------|-----------|--------|--------|
| **2** | Alfabeto e definição de tokens | ✅ Completo | `lexer.py` |
| **3** | Análise léxica (tokenização) | ✅ Completo | `lexer.py` |
| **4** | Análise sintática (parser BNF) | ✅ Completo | `parser.py` |
| **5** | Análise semântica | ✅ Completo | `analyzer.py` |
| **6** | Geração de código intermediário (TAC) | ✅ Completo | `ir_generator.py` |
| **7** | Ambientes de execução + Assembly | ✅ Completo | `assembly.py` |
| **Extra** | Otimizações | ✅ Completo | `optimizer.py`, `peephole.py` |

## 🎯 Funcionalidades

### Análise Léxica (Etapa 2-3)
- ✅ Reconhecimento de tokens (palavras-chave, operadores, identificadores, números)
- ✅ Tratamento de espaços em branco e comentários
- ✅ Detecção de erros léxicos

### Análise Sintática (Etapa 4)
- ✅ Parser baseado em gramática BNF
- ✅ Precedência de operadores
- ✅ Suporte a declarações de função
- ✅ Expressões aritméticas
- ✅ Detecção de erros sintáticos

### Análise Semântica (Etapa 5)
- ✅ Verificação de tipos
- ✅ Verificação de escopo (variáveis e funções)
- ✅ Detecção de variáveis não declaradas
- ✅ Verificação de parâmetros de função
- ✅ Validação de número de argumentos

### Geração de Código (Etapa 6-7)
- ✅ Código intermediário (Three-Address Code)
- ✅ Otimizações:
  - Constant folding (5+3 → 8)
  - Dead code elimination
  - Copy propagation
  - Peephole (x+0 → x, x*1 → x)
  - Simplificação algébrica (x-x → 0)
- ✅ Geração de assembly MIPS-like
- ✅ Alocação de registradores
- ✅ Gerenciamento de pilha (stack frames)

### Ambientes de Execução (Etapa 7)
- ✅ Activation Records completos
- ✅ Runtime Stack para chamadas de função
- ✅ Tabela de símbolos com escopos aninhados
- ✅ Suporte a chamadas recursivas e aninhadas
- ✅ Links dinâmicos e estáticos

## 📖 Documentação

- **`compiler/README.md`**: Documentação detalhada da arquitetura modular
- **`docs/GUIA_DE_ESTUDOS.md`**: Guia completo de estudos (500+ linhas)
- **`docs/ETAPA7_AMBIENTES_EXECUCAO.md`**: Documentação da Etapa 7
- **Cada módulo**: Possui docstrings e exemplos de teste

---

## Licenca

Este projeto esta licenciado sob a MIT license.

## Gramatica - Forma BNF

```bnf

<program> ::= <stmt_list>

<stmt_list> ::= <stmt> | <stmt> <stmt_list>

<stmt> ::= <assign_stmt> 
         | <if_stmt> 
         | <while_stmt> 
         | <print_stmt>

<assign_stmt> ::= <id> "=" <expr> ";"

<if_stmt> ::= "if" "(" <expr> ")" "{" <stmt_list> "}" 
            | "if" "(" <expr> ")" "{" <stmt_list> "}" "else" "{" <stmt_list> "}"

<while_stmt> ::= "while" "(" <expr> ")" "{" <stmt_list> "}"

<print_stmt> ::= "print" "(" <expr> ")" ";"

<expr> ::= <term> | <expr> "+" <term> | <expr> "-" <term>

<term> ::= <factor> | <term> "*" <factor> | <term> "/" <factor>

<factor> ::= <number> | <id> | "(" <expr> ")"

<id> ::= <letter> { <letter> | <digit> }

<number> ::= <digit> { <digit> }

<letter> ::= "a" | "b" | ... | "z" | "A" | "B" | ... | "Z"

<digit> ::= "0" | "1" | ... | "9"

```

# Autômato Finito Determinístico - Compilador Linguagem Mínima

## Tokens da Linguagem

- **Palavras-chave**: PRINT, IF, ELSE, WHILE, RETURN, INT
- **Operadores**: = (atribuição), + (soma)
- **Delimitadores**: ; (ponto e vírgula), ( ) (parênteses)
- **Literais**: números inteiros
- **Identificadores**: variáveis e funções

## Alfabeto de Entrada

- **dígito**: 0-9
- **letra**: a-z, A-Z
- **_**: underscore
- **=**: igual
- **+**: mais
- **;**: ponto e vírgula
- **(**: parêntese esquerdo
- **)**: parêntese direito
- **espaço**: espaço, tab, quebra de linha
- **outro**: qualquer outro caractere

---

## Tabela de Transições do AFD

| Estado | dígito | letra | _ | = | + | ; | ( | ) | espaço | outro |
|--------|--------|-------|---|---|---|---|---|---|---------|-------|
| **q0** | q_num | q_id | q_id | q_equals | q_plus | q_scolon | q_lparen | q_rparen | q0 | qE |
| **q_num** | q_num | qE | qE | q0 | q0 | q0 | q0 | q0 | q0 | qE |
| **q_id** | q_id | q_id | q_id | q0 | q0 | q0 | q0 | q0 | q0 | qE |
| **q_equals** | qE | qE | qE | qE | qE | qE | qE | qE | q0 | qE |
| **q4** | qE | qE | qE | qE | qE | qE | qE | qE | q0 | qE |
| **q_scolon** | qE | qE | qE | qE | qE | qE | qE | qE | q0 | qE |
| **q_lparen** | qE | qE | qE | qE | qE | qE | qE | qE | q0 | qE |
| **q_rparen** | qE | qE | qE | qE | qE | qE | qE | qE | q0 | qE |
| **qE** | qE | qE | qE | qE | qE | qE | qE | qE | qE | qE |

---

## Descrição dos Estados

### Estados Principais

- **q0**: Estado inicial (aguardando próximo token)
- **q1**: Reconhecendo número inteiro
- **q2**: Reconhecendo identificador/palavra-chave
- **q3**: Token de atribuição (=)
- **q4**: Token de soma (+)
- **q5**: Token ponto e vírgula (;)
- **q6**: Token parêntese esquerdo (()
- **q7**: Token parêntese direito ())
- **qE**: Estado de erro

### Estados Finais e Tokens Gerados

| Estado Final | Token Gerado | Descrição |
|-------------|-------------|-----------|
| **q1** | TOKEN_NUMBER | Número inteiro |
| **q2** | TOKEN_ID ou TOKEN_KEYWORD | Identificador ou palavra-chave* |
| **q3** | TOKEN_ASSIGN | Operador de atribuição |
| **q4** | TOKEN_PLUS | Operador de soma |
| **q5** | TOKEN_SEMICOLON | Ponto e vírgula |
| **q6** | TOKEN_LPAREN | Parêntese esquerdo |
| **q7** | TOKEN_RPAREN | Parêntese direito |

*Para o estado q2, é necessária verificação adicional para determinar se é palavra-chave.

---
## Associações semânticas

A etapa de tradução dirigida por sintaxe, as ações semânticas implementadas nas regras do
parser não apenas constroem a AST, mas também podem ser estendidas para incluir
informações de tipos e escopos, tornando a árvore anotada e apta para análises semânticas
posteriores. Isso facilita a verificação de tipos, o controle de variáveis e a detecção de
possíveis erros semânticos, além de preparar a AST para a geração de código.

## Arvore Sintatica Abstrata
Para a implementação precisamos associar ações semânticas às regras da gramática definidas
no parser e gerar uma Árvore de Sintaxe Abstrata (AST) anotada com informações de tipos e
escopos. Abaixo, apresento um artefato com a implementação atualizada do parser, incluindo
ações semânticas para construir a AST anotada.
Para o exemplo de código a seguir:

```Python

x = 5 + 3;

print(x * 2);
```

Teremos a AST gerada:

```cmd
program {'scope': 'global'}

  assign (x) {'type': 'int', 'scope': 'global'}

    + {'type': 'int'}

      num (5) {'type': 'int'}

      num (3) {'type': 'int'}

  print {'type': 'int', 'scope': 'global'}

    * {'type': 'int'}

      id (x) {'type': 'int', 'scope': 'global'}

      num (2) {'type': 'int'}
```

Formando (simplificadamente) a AST:


## Transformar AST em código Intermediário

Para a geração de código intermediário utilizamos a AST denotada anteriormente em 5.2,
mas somente para instruções que contém três operadores por enquanto. Dito isto, optamos
por gerar um TAC, que é um Three-Access-Code, que processa no máximo três operadores
por vez. Por Exemplo:

``` Python

x = 5 + 3;

print(x * 2);
```

Gera:

```
t1 = 5 + 3

x = t1

t2 = x * 2

print t2
```

Concluindo. No arquivo codegen.py são carregados os tokens e o parser gerado em parser.py,

onde  é  construído  as  variáveis  temporárias  chamadas  t1,  t2  e  t3  após  construir  a  AST,

montando claramente as operações realizadas.
