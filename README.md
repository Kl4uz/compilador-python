# 🚀 Mini-Compilador Python# 🚀 Mini Compilador em Python



Compilador didático implementado **conforme metodologia ensinada em aula**.Bem-vindo ao repositório do **Mini Compilador em Python**, um projeto acadêmico completo desenvolvido para a disciplina de Compiladores. 



## 👥 EquipeEste projeto implementa um **compilador completo** para uma mini-linguagem C-like, cobrindo todas as fases: **análise léxica, sintática, semântica, geração de código intermediário, otimizações e geração de assembly**.

- Lucas Farias

- José Lucas  ## 📚 Sobre o Projeto

- Ester Araiz

- Henrique NoronhaCompilador educacional que transforma código fonte em assembly MIPS-like, passando por todas as etapas clássicas de compilação com arquitetura modular e bem documentada.



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



## 📊 Pipeline de Compilaçãoif result['success']:

    print("✓ Compilação bem-sucedida!")

**Conforme metodologia do professor:**    for linha in result['assembly']:

        print(linha)

| Fase | Entrada | Saída | Arquivo |else:

|------|---------|-------|---------|    print("✗ Erros:", result['errors'])

| **1. Léxico** | Código fonte | Tokens | `lexer.py` |```

| **2. Sintático LL(1)** | Tokens | Parse Tree | `parser_ll1.py` ✅ |

| **3. AST** | Parse Tree | AST | `ast.py` |#### Via Linha de Comando

| **4. Semântica** | AST | Tabela Símbolos | `analyzer.py` |

| **5. IR** | AST | TAC + Quádruplas | `ir_generator.py` ✅ |```bash

| **6. Otimizações** | IR | IR Otimizado | `optimizer.py` ✅ |# Compilar arquivo

| **7. Assembly** | IR | MIPS-like | `assembly.py` |python compiler/main.py tests/hello_world.txt --verbose



---# Salvar assembly

python compiler/main.py tests/code.txt -o output.asm

## ✅ Implementado Conforme Professor

# Sem otimizações

### ✅ Parser LL(1) Top-Downpython compiler/main.py tests/code.txt --no-optimize

- **Recursive Descent** manual```

- **Lookahead de 1 token**

- Cada não-terminal = função recursiva### Testes

- Arquivo: `compiler/parser_ll1.py`

```bash

### ✅ Eliminação de Subexpressões Comuns (CSE)# Rodar suite completa de testes

```pythonpython test_compiler.py

# Antes:

t1 = a + b# Testar módulo individual

t2 = a + b  # redundante!python compiler/lexer.py

python compiler/parser.py

# Depois (CSE):python compiler/optimizer.py

t1 = a + b```

t2 = t1     # reutiliza!

```## 📦 Dependências



### ✅ Formato Quádruplas- **Python 3.8+**: Linguagem principal

```- **PLY (Python Lex-Yacc) 3.11**: Análise léxica e sintática

(operação, arg1, arg2, resultado)- **pytest**: Testes (opcional)

(*, b, 2, t0)

(+, a, t0, t1)```bash

(assign, t1, -, x)pip install ply

``````



### ✅ Todas as Otimizações## 🔄 Pipeline de Compilação

1. **CSE** - Eliminação de Subexpressões Comuns

2. **Constant Folding** - Avalia em tempo de compilação```

3. **Algebraic Simplification** - x*1→x, x+0→x, x*0→0   Código Fonte (.txt)

4. **Peephole** - x*2→x<<1         ↓

5. **Copy Propagation** - Propaga cópias   [1] LEXER (lexer.py)

6. **Dead Code Elimination** - Remove código morto       → Tokenização

         ↓

---   [2] PARSER (parser.py)

       → Parse Tree (BNF)

## 📖 Exemplo Completo         ↓

   [3] AST Builder (ast.py)

### Entrada:       → Abstract Syntax Tree

```c         ↓

int x = a + b * 2;   [4] ANALYZER (analyzer.py)

```       → Análise Semântica

       → Symbol Table

### Saída (Verbose):         ↓

   [5] IR GENERATOR (ir_generator.py)

```       → Three-Address Code (TAC)

✅ COMPILAÇÃO BEM-SUCEDIDA!         ↓

   [6] OPTIMIZER (optimizer.py + peephole.py)

━━━ TOKENS ━━━       → Constant Folding

28 tokens: INT, ID, EQUALS, ID, PLUS, ID, TIMES, NUMBER, SEMICOLON...       → Dead Code Elimination

       → Copy Propagation

━━━ TABELA DE SÍMBOLOS ━━━       → Peephole Optimization

main: function (params=0)         ↓

  a: int   [7] ASSEMBLY GENERATOR (assembly.py)

  b: int       → Código MIPS-like

  x: int         ↓

    Assembly (.asm)

━━━ CÓDIGO INTERMEDIÁRIO (TAC) ━━━```

0: begin_func main

1: a = 7## ✅ Etapas Implementadas

2: b = 8

3: t0 = b * 2| Etapa | Descrição | Status | Módulo |

4: t1 = a + t0|-------|-----------|--------|--------|

5: x = t1| **2** | Alfabeto e definição de tokens | ✅ Completo | `lexer.py` |

6: return 0| **3** | Análise léxica (tokenização) | ✅ Completo | `lexer.py` |

7: end_func main| **4** | Análise sintática (parser BNF) | ✅ Completo | `parser.py` |

| **5** | Análise semântica | ✅ Completo | `analyzer.py` |

━━━ QUÁDRUPLAS ━━━| **6** | Geração de código intermediário (TAC) | ✅ Completo | `ir_generator.py` |

0: (begin_func, main, -, -)| **7** | Ambientes de execução + Assembly | ✅ Completo | `assembly.py` |

1: (assign, 7, -, a)| **Extra** | Otimizações | ✅ Completo | `optimizer.py`, `peephole.py` |

2: (assign, 8, -, b)

3: (*, b, 2, t0)## 🎯 Funcionalidades

4: (+, a, t0, t1)

5: (assign, t1, -, x)### Análise Léxica (Etapa 2-3)

6: (return, 0, -, -)- ✅ Reconhecimento de tokens (palavras-chave, operadores, identificadores, números)

7: (end_func, main, -, -)- ✅ Tratamento de espaços em branco e comentários

- ✅ Detecção de erros léxicos

━━━ ASSEMBLY (MIPS-like) ━━━

main:### Análise Sintática (Etapa 4)

  addi $sp, $sp, -4- ✅ Parser baseado em gramática BNF

  sw $fp, 0($sp)- ✅ Precedência de operadores

  move $fp, $sp- ✅ Suporte a declarações de função

  li $t0, 8- ✅ Expressões aritméticas

  sw $t0, b- ✅ Detecção de erros sintáticos

  li $t1, 7

  sw $t1, a### Análise Semântica (Etapa 5)

  mul $t2, $t0, 2- ✅ Verificação de tipos

  add $t3, $t1, $t2- ✅ Verificação de escopo (variáveis e funções)

  move $t4, $t3- ✅ Detecção de variáveis não declaradas

  sw $t4, x- ✅ Verificação de parâmetros de função

  move $v0, 0- ✅ Validação de número de argumentos

  lw $fp, 0($sp)

  addi $sp, $sp, 4### Geração de Código (Etapa 6-7)

  jr $ra- ✅ Código intermediário (Three-Address Code)

```- ✅ Otimizações:

  - Constant folding (5+3 → 8)

---  - Dead code elimination

  - Copy propagation

## 🧪 Testes Rápidos  - Peephole (x+0 → x, x*1 → x)

  - Simplificação algébrica (x-x → 0)

```bash- ✅ Geração de assembly MIPS-like

# Teste básico- ✅ Alocação de registradores

python run.py -f tests/simples.txt- ✅ Gerenciamento de pilha (stack frames)



# Teste CSE (vê otimização acontecendo!)### Ambientes de Execução (Etapa 7)

python run.py -f tests/teste_cse.txt- ✅ Activation Records completos

- ✅ Runtime Stack para chamadas de função

# Exemplo do professor- ✅ Tabela de símbolos com escopos aninhados

python run.py -f tests/exemplo_professor.txt- ✅ Suporte a chamadas recursivas e aninhadas

- ✅ Links dinâmicos e estáticos

# Teste com expressões complexas

python demos/teste_expressoes.py## 📖 Documentação

```

- **`compiler/README.md`**: Documentação detalhada da arquitetura modular

---- **`docs/GUIA_DE_ESTUDOS.md`**: Guia completo de estudos (500+ linhas)

- **`docs/ETAPA7_AMBIENTES_EXECUCAO.md`**: Documentação da Etapa 7

## 📚 Documentação Adicional- **Cada módulo**: Possui docstrings e exemplos de teste



Veja `docs_projeto/` para:---

- **GUIA_RAPIDO.md** - Referência rápida

- **COMANDOS.md** - Lista de comandos úteis## Licenca

- **README_OLD.md** - Documentação anterior completa

Este projeto esta licenciado sob a MIT license.

---

## Gramatica - Forma BNF

## 🎯 Metodologia Aplicada

```bnf

### Análise Léxica

- Expressões Regulares (ER)<program> ::= <stmt_list>

- PLY gera AFD automaticamente

<stmt_list> ::= <stmt> | <stmt> <stmt_list>

### Análise Sintática

- **LL(1) Top-Down** ✅<stmt> ::= <assign_stmt> 

- **Recursive Descent** ✅         | <if_stmt> 

- **1 token de lookahead** ✅         | <while_stmt> 

         | <print_stmt>

### Código Intermediário

- **Three-Address Code (TAC)** ✅<assign_stmt> ::= <id> "=" <expr> ";"

- **Quádruplas** ✅

<if_stmt> ::= "if" "(" <expr> ")" "{" <stmt_list> "}" 

### Otimizações            | "if" "(" <expr> ")" "{" <stmt_list> "}" "else" "{" <stmt_list> "}"

- **CSE** (Common Subexpression Elimination) ✅

- **Constant Folding** ✅<while_stmt> ::= "while" "(" <expr> ")" "{" <stmt_list> "}"

- **Dead Code Elimination** ✅

- **Copy Propagation** ✅<print_stmt> ::= "print" "(" <expr> ")" ";"

- **Algebraic Simplification** ✅

<expr> ::= <term> | <expr> "+" <term> | <expr> "-" <term>

### Assembly

- **MIPS-like**<term> ::= <factor> | <term> "*" <factor> | <term> "/" <factor>

- **LOAD/MUL/ADD/STORE** ✅

<factor> ::= <number> | <id> | "(" <expr> ")"

---

<id> ::= <letter> { <letter> | <digit> }

## 📝 Licença

<number> ::= <digit> { <digit> }

MIT License

<letter> ::= "a" | "b" | ... | "z" | "A" | "B" | ... | "Z"

---

<digit> ::= "0" | "1" | ... | "9"

**📚 Projeto Acadêmico - Disciplina de Compiladores**

```

*Implementado conforme metodologia ensinada em aula.*

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
