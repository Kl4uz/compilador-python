# Mini Compilador em Python

Bem-vindo ao repositório do **Mini Compilador em Python**, um projeto acadêmico desenvolvido para a disciplina de Compiladores. Este projeto tem como objetivo implementar um compilador simples para uma linguagem de programação minimalista, cobrindo as fases de análise léxica, sintática, semântica e geração de código.

## Sobre o Projeto

Este mini compilador processará uma linguagem simples (a ser definida, ex.: mini-Python ou aritmética básica) e será implementado em Python. O projeto é desenvolvido por uma equipe de estudantes, com foco em aprendizado colaborativo e aplicação prática de conceitos de compiladores.

### Objetivos

- Implementar um lexer para tokenização.
- Construir um parser para gerar uma Árvore de Sintaxe Abstrata (AST).
- Realizar análise semântica para verificar tipos e escopo.
- Gerar código de saída (ex.: bytecode ou assembly simples).
- Testar o compilador com casos de uso variados.

### Equipe

- Lucas Farias
- José Lucas
- Ester Araiz
- Henrique Noronha

*(Substitua os nomes acima pelos membros reais da equipe.)*

## Estrutura do Repositório

```
compilador-python/
├── README.md                 # Documentação principal
├── main.py                   # Ponto de entrada (CLI)
├── requirements.txt          # Dependências do projeto
├── .gitignore                # Arquivos ignorados pelo Git
├── src/                      # Código fonte
│   ├── lexer.py              # Analisador léxico
│   ├── parser.py              # Analisador sintático
│   ├── ast_builder.py         # Construtor de AST
│   ├── semantic.py            # Analisador semântico
│   ├── symbol_table.py        # Tabela de símbolos com escopos
│   ├── ir_generator.py        # Gerador de código intermediário (TAC)
│   ├── optimizer.py            # Otimizador de código
│   ├── assembly_generator.py  # Gerador de código assembly
│   ├── compiler.py            # Pipeline principal do compilador
│   ├── test_pipeline.py       # Testes do pipeline
│   ├── runtime.py             # Activation Records e Runtime Stack
│   ├── interpreter.py         # Interpretador TAC
│   ├── compiler_etapa7.py    # Sistema completo integrado (legado)
│   ├── codegen.py             # Gerador de código TAC (legado)
│   └── codegen_full.py        # Gerador de código com funções (legado)
├── tests/                     # Testes unitários e exemplos
│   ├── test_lexer.py
│   ├── test_parser.py
│   ├── hello_world.txt        # Exemplo básico
│   ├── code.txt               # Exemplo de expressões
│   └── test_functions.txt     # Exemplo com funções
├── docs/                      # Documentação detalhada
│   ├── pipeline.md            # Documentação do pipeline
│   ├── ETAPA7_AMBIENTES_EXECUCAO.md
│   └── ...
└── examples/                  # Exemplos de entrada
    └── hello_world.txt
```

## Dependências

As seguintes bibliotecas Python serão usadas no projeto (atualizaremos conforme necessário):

- **Python 3.8+**: Linguagem principal.
- **PLY (Python Lex-Yacc)**: Para análise léxica e sintática.
- **pytest**: Para testes unitários e integração.
- **black** (opcional): Para formatação de código.
- **pre-commit** (opcional): Para verificações automáticas antes de commits.

Instale as dependências com:

```pip install -r requirements.txt```

## Configuração inicial

1. Clone o repositorio

```bash
git clone https://github.com/Kl4uz/compilador-python.git
cd compilador-python
```

2. Crie um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as Dependências

```bash
pip install -r requirements.txt
```

## Uso Rápido

### Compilação Básica

```bash
# Compilar um arquivo
python main.py tests/test_functions.txt

# Compilar com otimização e salvar saída
python main.py tests/test_functions.txt -o output.ir --optimize

# Modo verboso (mostra todas as fases)
python main.py tests/test_functions.txt -v

# Gerar código assembly
python main.py tests/test_functions.txt --assembly
```

### Usando a API Python

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
    compiler.print_results(result)
else:
    for error in result["errors"]:
        print(f"Erro: {error}")
```

### Executar Testes

```bash
# Testes do pipeline completo
python src/test_pipeline.py
```

## Pipeline de Compilação

O compilador segue um pipeline tradicional de múltiplas fases:

1. **Análise Léxica** (`lexer.py`) - Tokenização do código fonte
2. **Análise Sintática** (`parser.py`) - Construção da AST
3. **Análise Semântica** (`semantic.py`) - Verificação de tipos e escopos
4. **Geração de IR** (`ir_generator.py`) - Código intermediário (TAC)
5. **Otimização** (`optimizer.py`) - Otimizações do código
6. **Geração de Assembly** (`assembly_generator.py`) - Código assembly (opcional)

Veja a documentação completa em [`docs/pipeline.md`](docs/pipeline.md).

## Como Contribuir

- Crie uma branch para sua feature: ``git checkout -b feature/nome-da-tarefa.``
- Faça commits atômicos com mensagens claras (ex.: `feat: adiciona lexer para operadores`).
- Envie um Pull Request para a branch `main` com descrição detalhada.

---

## 🎯 Etapa 7 - Ambientes de Execução (IMPLEMENTADO!)

### ✅ Funcionalidades Implementadas:

#### **Atividade 1 - Modelagem do Ambiente de Execução:**
- ✅ Organização de memória (código, dados globais, heap, stack)
- ✅ Comportamento da pilha de ativação para chamadas de funções
- ✅ Armazenamento de variáveis globais, locais e parâmetros

#### **Atividade 2 - Implementação do Registro de Ativação:**
- ✅ Estrutura completa de Activation Record contendo:
  * Parâmetros formais
  * Variáveis locais
  * Valor de retorno
  * Links dinâmico e estático
  * Endereço de retorno
  * Variáveis temporárias
- ✅ Demonstração de criação e destruição durante execução

#### **Atividade 3 - Integração com Tabela de Símbolos:**
- ✅ Associação de escopo e offset às variáveis
- ✅ Distinção entre variáveis globais e locais
- ✅ Simulação de recuperação de valores durante chamada de função

### 🚀 Como Executar a Etapa 7:

```bash
# Executar o compilador completo com exemplo de função
python src/compiler_etapa7.py
```

### 📖 Documentação Completa:
Veja a documentação detalhada em: **`docs/ETAPA7_AMBIENTES_EXECUCAO.md`**

### 🧪 Código de Teste:
```c
int soma(int a, int b) {
    int r = a + b;
    return r;
}

int main() {
    int x = soma(2, 3);
    print(x);
    return 0;
}
```

**Saída:**
```
>>> OUTPUT: 5
```

### 📊 Recursos Implementados:
- **Tabela de Símbolos** com escopos aninhados (`src/symbol_table.py`)
- **Activation Records** completos (`src/runtime.py`)
- **Runtime Stack** para gerenciar chamadas (`src/runtime.py`)
- **Gerador de TAC** para funções (`src/compiler_etapa7.py`)
- **Interpretador TAC** com simulação de execução (`src/interpreter.py`)

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
