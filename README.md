# 🚀 Mini Compilador em Python

Compilador didático implementado **conforme metodologia ensinada em aula**, para uma mini-linguagem C-like, cobrindo todas as fases clássicas de compilação:

- Análise léxica  
- Análise sintática  
- Análise semântica  
- Geração de código intermediário (TAC / Quádruplas)  
- Otimizações  
- Geração de código assembly MIPS-like  

Projeto acadêmico para a disciplina de **Compiladores**.

---

## 👥 Equipe

- Lucas Farias  
- José Lucas  
- Ester Araiz  
- Henrique Noronha  
- **Laura Barbosa**

---

## 📚 Sobre o Projeto

Este é um **compilador educacional** que transforma código fonte em **assembly MIPS-like**, passando por todas as etapas de compilação com uma arquitetura modular e bem documentada.

Principais objetivos:

- Servir como material de estudo para disciplinas de Compiladores
- Ilustrar um pipeline completo, de código-fonte até assembly
- Mostrar otimizações clássicas em código intermediário (TAC)

---

## ✨ Características

- ✅ **Pipeline completo** de compilação  
- ✅ **Separação clara** de fases (léxico → sintático → semântico → IR → otimização → assembly)  
- ✅ **Análise semântica robusta** com detecção de erros  
- ✅ **Suporte a funções** e chamadas aninhadas  
- ✅ **Código intermediário** (Three-Address Code - TAC + quádruplas)  
- ✅ **Otimizações**:  
  - Constant folding  
  - Dead code elimination  
  - Copy propagation  
  - Common Subexpression Elimination (CSE)  
  - Peephole  
  - Simplificações algébricas  
- ✅ **Geração de assembly** MIPS-like  
- ✅ **Módulos independentes e testáveis**  

---

## 📁 Estrutura do Repositório

```text
compilador-python/
├── run.py                     # Interface principal (use este!)
├── README.md                  # Este arquivo
├── requirements.txt           # Dependências
├── test_compiler.py           # Suite de testes integrada

├── compiler/                  # ⭐ NOVO COMPILADOR MODULAR
│   ├── README.md              # Documentação detalhada do módulo
│   ├── __init__.py
│   ├── main.py                # 🎯 Pipeline unificado
│   ├── lexer.py               # Análise léxica
│   ├── parser_ll1.py          # Parser LL(1) (recursive descent)
│   ├── ast.py                 # Árvore Sintática Abstrata (AST)
│   ├── analyzer.py            # Análise semântica
│   ├── symbol_table.py        # Tabela de símbolos
│   ├── ir.py                  # Definição de IR (TAC, quádruplas)
│   ├── ir_generator.py        # Geração de IR
│   ├── optimizer.py           # Otimizações (CSE, CF, DCE, CP, AS)
│   ├── peephole.py            # Otimizações peephole
│   ├── codegen.py             # Coordena geração de código
│   └── assembly.py            # Geração de assembly MIPS-like

├── src/                       # Implementação original (legado)
│   ├── lexer.py
│   ├── parser.py
│   ├── codegen.py
│   ├── symbol_table.py
│   ├── runtime.py
│   ├── interpreter.py
│   └── compiler_etapa7.py

├── tests/                     # Arquivos de teste
│   ├── simples.txt
│   ├── hello_world.txt
│   ├── code.txt
│   ├── teste_cse.txt
│   ├── exemplo_professor.txt
│   ├── test_functions.txt
│   └── test_nested_calls.txt

├── demos/                     # Demonstrações
│   ├── demo_completo.py
│   └── teste_expressoes.py

├── docs_projeto/              # Documentação do projeto
│   ├── GUIA_RAPIDO.md
│   ├── COMANDOS.md
│   └── README_OLD.md

└── docs/                      # Documentação teórica
    ├── GUIA_DE_ESTUDOS.md
    ├── ETAPA7_AMBIENTES_EXECUCAO.md
    └── RESUMO_ETAPA7.md
````

---

## 🚀 Como Usar

### 📦 Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/Kl4uz/compilador-python.git
cd compilador-python

# 2. Instale as dependências
pip install -r requirements.txt
```

> Requer **Python 3.8+**

---

### 💻 Modo 1: Linha de Comando (run.py)

#### Compilar expressão direta

```bash
python run.py -e "5 + 3 * 2"
```

#### Compilar arquivo

```bash
python run.py -f tests/simples.txt
```

#### Modo verbose (mostra TODAS as fases)

```bash
python run.py -f tests/exemplo_professor.txt --verbose
```

#### Modo quiet (saída resumida)

```bash
python run.py -f tests/simples.txt --quiet
```

#### Salvar assembly em arquivo

```bash
python run.py -f tests/code.txt -o output.asm
```

---

### 🎮 Modo 2: Interativo (REPL)

```bash
python run.py
```

Depois, digite expressões / comandos:

```text
>>> 5 + 3 * 2
>>> int x = a + b * 2;
>>> sair
```

---

### 🐍 Modo 3: Via Python (API)

```python
from compiler import compile

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

result = compile(codigo, optimize=True, verbose=True)

if result["success"]:
    print("✓ Compilação bem-sucedida!")
    for linha in result["assembly"]:
        print(linha)
else:
    print("✗ Erros:", result["errors"])
```

---

## 📊 Pipeline de Compilação

**Conforme metodologia do professor:**

| Fase               | Entrada      | Saída              | Arquivo                       |
| ------------------ | ------------ | ------------------ | ----------------------------- |
| 1. Léxico          | Código fonte | Tokens             | `lexer.py`                    |
| 2. Sintático LL(1) | Tokens       | Parse Tree         | `parser_ll1.py`               |
| 3. AST             | Parse Tree   | AST                | `ast.py`                      |
| 4. Semântica       | AST          | Tabela de Símbolos | `analyzer.py`                 |
| 5. IR (TAC)        | AST          | TAC + Quádruplas   | `ir_generator.py`             |
| 6. Otimizações     | IR           | IR Otimizado       | `optimizer.py`, `peephole.py` |
| 7. Assembly        | IR           | MIPS-like          | `assembly.py`                 |

---

## ✅ Funcionalidades por Etapa

### 🔹 Análise Léxica (Etapas 2–3)

* Reconhecimento de tokens (palavras-chave, operadores, identificadores, números)
* Tratamento de espaços em branco e comentários
* Detecção de erros léxicos

### 🔹 Análise Sintática (Etapa 4)

* Parser baseado em gramática BNF
* Precedência de operadores
* Suporte a declarações de função
* Expressões aritméticas
* Detecção de erros sintáticos

### 🔹 Análise Semântica (Etapa 5)

* Verificação de tipos
* Verificação de escopo (variáveis, funções)
* Detecção de variáveis não declaradas
* Verificação de parâmetros e número de argumentos
* Árvore anotada com tipos e escopos

### 🔹 Código Intermediário (IR / TAC)

* Formato de **Three-Address Code (TAC)**
* Representação em **quádruplas**:
  `(operação, arg1, arg2, resultado)`

Exemplo:

```text
(*, b, 2, t0)
(+, a, t0, t1)
(assign, t1, -, x)
```

### 🔹 Otimizações

1. **CSE** – Eliminação de Subexpressões Comuns
2. **Constant Folding** – Avaliação em tempo de compilação
3. **Algebraic Simplification** – `x*1 → x`, `x+0 → x`, `x*0 → 0`
4. **Peephole** – Micro-otimizações locais (`x*2 → x<<1`, etc.)
5. **Copy Propagation** – Propaga cópias simples
6. **Dead Code Elimination** – Remove código morto

### 🔹 Geração de Assembly (Etapas 6–7)

* Geração de código **MIPS-like**
* Instruções do tipo LOAD/MUL/ADD/STORE
* Alocação de registradores
* Gerenciamento de stack frame (pilha)
* Suporte a funções, chamadas aninhadas e recursivas

---

## 🧪 Testes Rápidos

```bash
# Teste básico
python run.py -f tests/simples.txt

# Teste de CSE e otimizações
python run.py -f tests/teste_cse.txt

# Exemplo do professor
python run.py -f tests/exemplo_professor.txt

# Testes com expressões complexas
python demos/teste_expressoes.py

# Rodar suite completa de testes
python test_compiler.py
```

---

## 📖 Exemplo Completo

### Entrada

```c
int x = a + b * 2;
```

### TAC (Three-Address Code)

```text
t0 = b * 2
t1 = a + t0
x  = t1
```

### Quádruplas

```text
(*, b, 2, t0)
(+, a, t0, t1)
(assign, t1, -, x)
```

### Assembly MIPS-like (trecho ilustrativo)

```asm
main:
  addi $sp, $sp, -4
  sw   $fp, 0($sp)
  move $fp, $sp

  li   $t0, 8
  sw   $t0, b
  li   $t1, 7
  sw   $t1, a

  mul  $t2, $t0, 2
  add  $t3, $t1, $t2
  move $t4, $t3
  sw   $t4, x

  move $v0, 0
  lw   $fp, 0($sp)
  addi $sp, $sp, 4
  jr   $ra
```

---

## 📐 Gramática – Forma BNF (Simplificada)

```bnf
<program>    ::= <stmt_list>

<stmt_list>  ::= <stmt>
               | <stmt> <stmt_list>

<stmt>       ::= <assign_stmt>
               | <if_stmt>
               | <while_stmt>
               | <print_stmt>

<assign_stmt>::= <id> "=" <expr> ";"

<if_stmt>    ::= "if" "(" <expr> ")" "{" <stmt_list> "}"
               | "if" "(" <expr> ")" "{" <stmt_list> "}" "else" "{" <stmt_list> "}"

<while_stmt> ::= "while" "(" <expr> ")" "{" <stmt_list> "}"

<print_stmt> ::= "print" "(" <expr> ")" ";"

<expr>       ::= <term>
               | <expr> "+" <term>
               | <expr> "-" <term>

<term>       ::= <factor>
               | <term> "*" <factor>
               | <term> "/" <factor>

<factor>     ::= <number>
               | <id>
               | "(" <expr> ")"

<id>         ::= <letter> { <letter> | <digit> }
<number>     ::= <digit> { <digit> }

<letter>     ::= "a" | ... | "z" | "A" | ... | "Z"
<digit>      ::= "0" | ... | "9"
```

---

## 🔠 Autômato Finito Determinístico (AFD) – Léxico

### Tokens da Linguagem

* **Palavras-chave**: `PRINT`, `IF`, `ELSE`, `WHILE`, `RETURN`, `INT`
* **Operadores**: `=` (atribuição), `+` (soma)
* **Delimitadores**: `;`, `(`, `)`
* **Literais**: números inteiros
* **Identificadores**: variáveis e funções

### Alfabeto de Entrada

* `dígito`: `0–9`
* `letra`: `a–z`, `A–Z`
* `_`: underscore
* `=`, `+`, `;`, `(`, `)`
* `espaço`: espaço, tab, quebra de linha
* `outro`: qualquer outro caractere

### Tabela de Transições (Resumo)

| Estado    | dígito | letra | _    | =        | +      | ;        | (        | )        | espaço | outro |
| --------- | ------ | ----- | ---- | -------- | ------ | -------- | -------- | -------- | ------ | ----- |
| **q0**    | q_num  | q_id  | q_id | q_equals | q_plus | q_scolon | q_lparen | q_rparen | q0     | qE    |
| **q_num** | q_num  | qE    | qE   | q0       | q0     | q0       | q0       | q0       | q0     | qE    |
| **q_id**  | q_id   | q_id  | q_id | q0       | q0     | q0       | q0       | q0       | q0     | qE    |
| ...       | ...    | ...   | ...  | ...      | ...    | ...      | ...      | ...      | ...    | ...   |

### Estados Finais (Tokens)

| Estado Final | Token              | Descrição                      |
| ------------ | ------------------ | ------------------------------ |
| q_num        | TOKEN_NUMBER       | Número inteiro                 |
| q_id         | TOKEN_ID / KEYWORD | Identificador ou palavra-chave |
| q_equals     | TOKEN_ASSIGN       | `=`                            |
| q_plus       | TOKEN_PLUS         | `+`                            |
| q_scolon     | TOKEN_SEMICOLON    | `;`                            |
| q_lparen     | TOKEN_LPAREN       | `(`                            |
| q_rparen     | TOKEN_RPAREN       | `)`                            |

---

## 🌳 AST – Árvore Sintática Abstrata & Associações Semânticas

Exemplo de código:

```c
x = 5 + 3;
print(x * 2);
```

AST anotada (forma textual):

```text
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

As ações semânticas no parser:

* Constroem a AST
* Anotam nós com **tipo** e **escopo**
* Preparam para a geração de IR e para verificações semânticas posteriores

---

## 🔁 AST → Código Intermediário (TAC)

Para o mesmo exemplo:

```c
x = 5 + 3;
print(x * 2);
```

Geramos o TAC:

```text
t1 = 5 + 3
x  = t1
t2 = x * 2
print t2
```

Essas temporárias (`t1`, `t2`, …) são geradas no módulo `codegen.py` a partir da AST e do IR.

---

## 📚 Documentação Adicional

Consulte a pasta `docs_projeto/` e `docs/` para:

* `GUIA_RAPIDO.md` – Referência rápida
* `COMANDOS.md` – Lista de comandos úteis
* `README_OLD.md` – Documentação anterior completa
* `GUIA_DE_ESTUDOS.md` – Guia completo de estudos
* `ETAPA7_AMBIENTES_EXECUCAO.md` – Ambientes de execução (Etapa 7)
* `RESUMO_ETAPA7.md` – Resumo teórico da etapa final

---

## 📝 Licença

Este projeto está licenciado sob a **MIT License**.

> Projeto acadêmico da disciplina de Compiladores, implementado conforme metodologia ensinada em aula.
