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
├── README.md                 # Documentação inicial
├── requirements.txt          # Dependências do projeto
├── .gitignore                # Arquivos ignorados pelo Git
├── src/                      # Código fonte
│   ├── lexer.py              # Analisador léxico
│   ├── parser.py
│   ├── semantic.py
│   ├── codegen.py
│   ├── main.py
├── tests/                    # Testes unitários
│   ├── test_lexer.py
│   ├── test_parser.py
├── examples/                 # Exemplos de entrada
│   └── hello_world.txt
└── docs/                     # Documentação detalhada
└── grammar.md
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

## Como Contribuir 
- Crie uma branch para sua feature: ``git checkout -b feature/nome-da-tarefa.``
- Faça commits atômicos com mensagens claras (ex.: `feat: adiciona lexer para operadores`).
- Envie um Pull Request para a branch `main` com descrição detalhada.


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
