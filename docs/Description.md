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
