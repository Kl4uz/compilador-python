# 📚 GUIA DE ESTUDOS - Mini Compilador

## Objetivo
Este guia vai te ajudar a entender **cada etapa** do projeto, o que foi implementado, e como explicar o código (especialmente a Etapa 7).

---

## 📋 Visão Geral das Etapas

```
Etapa 1: Planejamento (conceitual)
Etapa 2: Definição do Alfabeto e Tokens ✅
Etapa 3: Análise Léxica (Lexer) ✅
Etapa 4: Análise Sintática (Parser) ✅
Etapa 5: Análise Semântica ✅
Etapa 6: Geração de Código Intermediário (TAC) ✅
Etapa 7: Ambientes de Execução ✅ ← FOCO PRINCIPAL
```

---

# ETAPA 2: Alfabeto e Tokens

## 📖 O que é?
Definir os "ingredientes" básicos da linguagem.

## 🎯 O que faz?
- Define quais caracteres são válidos na linguagem
- Lista os tokens (palavras e símbolos) que o compilador reconhece

## 💻 Onde está implementado?
**Arquivo:** `src/lexer.py` (linhas 3-28)

## 📝 Como explicar:

### Alfabeto (conjunto de caracteres válidos):
```
Σ = {a-z, A-Z, 0-9, +, -, *, /, =, ;, (, ), {, }, espaço, tab, \n}
```

### Tokens (palavras/símbolos reconhecidos):
```python
tokens = (
    'ID',          # identificadores (nomes de variáveis)
    'NUMBER',      # números inteiros
    'PLUS',        # símbolo +
    'MINUS',       # símbolo -
    'TIMES',       # símbolo *
    'DIVIDE',      # símbolo /
    'EQUALS',      # símbolo =
    'SEMICOLON',   # símbolo ;
    # ... etc
)
```

### Palavras Reservadas:
```python
reserved = {
    'if': 'IF',
    'while': 'WHILE',
    'return': 'RETURN',
    'int': 'INT',
    'print': 'PRINT'
}
```

## 🗣️ Como explicar na apresentação:
> "Primeiro definimos o alfabeto da linguagem, que são os caracteres válidos. Depois listamos os tokens, que são as 'palavras' que nosso compilador vai reconhecer. Por exemplo, `int` é uma palavra reservada, `+` é um operador, e `x` seria um identificador."

---

# ETAPA 3: Análise Léxica (Lexer)

## 📖 O que é?
Transformar o código fonte em uma sequência de tokens.

## 🎯 O que faz?
Lê o código caractere por caractere e agrupa em tokens válidos.

**Exemplo:**
```
Input:  "x = 10 + 20;"
Output: [ID(x), EQUALS, NUMBER(10), PLUS, NUMBER(20), SEMICOLON]
```

## 💻 Onde está implementado?
**Arquivo:** `src/lexer.py` (completo)

## 📝 Como explicar cada parte:

### 1. Expressões Regulares (ERs):
```python
t_PLUS    = r'\+'                    # reconhece o símbolo +
t_NUMBER  = r'\d+'                   # reconhece 1 ou mais dígitos
t_ID      = r'[a-zA-Z_][a-zA-Z0-9_]*'  # reconhece identificadores
```

**Como funciona:**
- `\d+` significa "um ou mais dígitos"
- `[a-zA-Z_]` significa "uma letra ou underscore"
- `[a-zA-Z0-9_]*` significa "zero ou mais letras, dígitos ou underscores"

### 2. Funções de Reconhecimento:
```python
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # verifica se é palavra reservada
    return t
```

**O que faz:**
1. Reconhece um identificador
2. Verifica se é palavra reservada (como `int`, `while`)
3. Se for reservada, muda o tipo do token
4. Se não, mantém como `ID`

### 3. Caracteres Ignorados:
```python
t_ignore = ' \t'  # ignora espaços e tabs

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)  # conta linhas
```

### 4. Tratamento de Erros:
```python
def t_error(t):
    print(f"Caractere ilegal: '{t.value[0]}'")
    t.lexer.skip(1)  # pula o caractere inválido
```

## 🧪 Como testar:
```bash
cd src
python test_lexer.py
```

**Saída esperada:**
```
LexToken(INT,'int',1,0)
LexToken(ID,'soma',1,4)
LexToken(LPAREN,'(',1,8)
```

## 🗣️ Como explicar na apresentação:
> "O lexer lê o código caractere por caractere usando expressões regulares. Por exemplo, quando vê 'int', reconhece como palavra reservada INT. Quando vê 'x123', reconhece como identificador ID. O resultado é uma lista de tokens que vai para o parser."

**Demonstração ao vivo:**
```python
from lexer import lexer
lexer.input("x = 10;")
for tok in lexer:
    print(tok)
```

---

# ETAPA 4: Análise Sintática (Parser)

## 📖 O que é?
Verifica se a sequência de tokens segue as regras gramaticais da linguagem.

## 🎯 O que faz?
Transforma a lista de tokens em uma Árvore Sintática Abstrata (AST).

**Exemplo:**
```
Input (tokens):  [ID(x), EQUALS, NUMBER(5), PLUS, NUMBER(3), SEMICOLON]
Output (AST):    ('assign', 'x', ('+', ('num', 5), ('num', 3)))
```

## 💻 Onde está implementado?
**Arquivo:** `src/codegen.py` (linhas 86-157)

## 📝 Como explicar:

### 1. Gramática da Linguagem (BNF):
```bnf
<program>    ::= <statement_list>
<statement>  ::= <assign> | <print>
<assign>     ::= ID = <expression> ;
<expression> ::= <term> | <expression> + <term>
<term>       ::= <factor> | <term> * <factor>
<factor>     ::= NUMBER | ID | ( <expression> )
```

**O que isso significa:**
- Um programa é uma lista de comandos
- Um comando pode ser atribuição ou print
- Expressões seguem precedência matemática (*, / antes de +, -)

### 2. Implementação das Regras:
```python
def p_stmt_assign(p):
    '''statement : ID EQUALS expression SEMICOLON'''
    p[0] = ('assign', p[1], p[3])
```

**Como ler:**
- `statement :` → estou definindo o que é um statement
- `ID EQUALS expression SEMICOLON` → sequência de tokens esperada
- `p[1]` → primeiro token (ID)
- `p[3]` → terceiro token (expression)
- `p[0]` → resultado (nó da AST)

### 3. Precedência de Operadores:
```python
precedence = (
    ('left', 'PLUS', 'MINUS'),      # + e - têm precedência baixa
    ('left', 'TIMES', 'DIVIDE'),    # * e / têm precedência alta
    ('right', 'EQUALS'),             # = associa da direita
)
```

**Resultado:**
- `5 + 3 * 2` é interpretado como `5 + (3 * 2)` ✅
- Não como `(5 + 3) * 2` ❌

## 🧪 Como testar:
```bash
cd src
python codegen.py
```

## 🗣️ Como explicar na apresentação:
> "O parser verifica se os tokens seguem a gramática. Por exemplo, para 'x = 5 + 3;', ele verifica: tem ID? ✅ Tem EQUALS? ✅ Tem expressão válida? ✅ Tem ponto-e-vírgula? ✅ Então gera a AST correspondente."

**Visualização da AST:**
```
Código: x = 5 + 3;

AST:
  assign
  ├── x (variável)
  └── +
      ├── 5
      └── 3
```

---

# ETAPA 5: Análise Semântica

## 📖 O que é?
Verifica se o código faz sentido (além da sintaxe).

## 🎯 O que faz?
- Verifica tipos das variáveis
- Detecta uso de variáveis não declaradas
- Anota a AST com informações de tipo e escopo

## 💻 Onde está implementado?
**Arquivo:** `src/codegen.py` (linhas 15-27, 98-100)

## 📝 Como explicar:

### 1. Tabela de Símbolos:
```python
symbol_table = {}

# Ao processar: x = 10;
symbol_table['x'] = {'type': 'int', 'scope': 'global'}
```

**O que armazena:**
- Nome da variável
- Tipo (int, float, etc.)
- Escopo (global, local)

### 2. Inferência de Tipos:
```python
def infer_type(node):
    if node[0] == 'num':
        return 'int'  # número literal é int
    elif node[0] == 'id':
        return symbol_table.get(node[1], {}).get('type', 'unknown')
    elif node[0] in ('+', '-', '*', '/'):
        left_type = infer_type(node[1])
        right_type = infer_type(node[2])
        if left_type == 'int' and right_type == 'int':
            return 'int'
```

**Como funciona:**
1. Se é número literal → tipo é `int`
2. Se é variável → busca tipo na tabela de símbolos
3. Se é operação → verifica tipos dos operandos

### 3. AST Anotada:
```python
# AST sem anotação:
('num', 5)

# AST anotada:
('num', 5, {'type': 'int'})
```

**Benefício:**
- Facilita geração de código
- Detecta erros de tipo
- Prepara para otimizações

## 🧪 Como testar:
```bash
python -c "from codegen import parser, symbol_table; from lexer import lexer; code='x=5; y=x+3;'; ast=parser.parse(code, lexer=lexer); print('Tabela:', symbol_table)"
```

## 🗣️ Como explicar na apresentação:
> "A análise semântica verifica se o código faz sentido. Por exemplo, se você tenta usar uma variável que não foi declarada, o compilador dá um warning. Também anota a AST com tipos, então sabemos que '5 + 3' resulta em um int."

---

# ETAPA 6: Geração de Código Intermediário (TAC)

## 📖 O que é?
Transformar a AST em código de três endereços (TAC - Three Address Code).

## 🎯 O que faz?
Gera código intermediário entre a linguagem de alto nível e código de máquina.

**Formato TAC:**
```
resultado = operando1 operador operando2
```

## 💻 Onde está implementado?
**Arquivo:** `src/codegen.py` (função `generate_tac`, linhas 34-81)

## 📝 Como explicar:

### 1. Por que TAC?
- **Simplicidade:** cada instrução tem no máximo 3 operandos
- **Facilita otimização:** formato padronizado
- **Preparação para assembly:** próximo do código de máquina

### 2. Como funciona:
```python
def generate_tac(ast):
    tac = []
    
    def traverse(node):
        if node_type == '+':
            left = traverse(node[1])   # processa lado esquerdo
            right = traverse(node[2])  # processa lado direito
            temp = new_temp()          # cria variável temporária
            tac.append(('+', left, right, temp))  # emite instrução
            return temp
```

### 3. Exemplo Completo:

**Código Fonte:**
```c
x = 5 + 3 * 2;
```

**AST:**
```
assign
├── x
└── +
    ├── 5
    └── *
        ├── 3
        └── 2
```

**TAC Gerado:**
```
t1 = 3 * 2
t2 = 5 + t1
x = t2
```

**Passo a passo:**
1. Processa `3 * 2` → gera `t1 = 3 * 2`
2. Processa `5 + t1` → gera `t2 = 5 + t1`
3. Processa atribuição → gera `x = t2`

### 4. Variáveis Temporárias:
```python
temp_count = 0

def new_temp():
    global temp_count
    temp_count += 1
    return f't{temp_count}'  # gera t1, t2, t3...
```

**Por que temporárias?**
- Quebram expressões complexas em passos simples
- Facilitam otimização
- Correspondem a registradores da CPU

## 🧪 Como testar:
```bash
cd src
python demo_tac.py
```

**Saída:**
```
Código Fonte:
x = 5 + 3 * 2;

Código TAC:
t1 = 3 * 2
t2 = 5 + t1
x = t2
```

## 🗣️ Como explicar na apresentação:
> "O TAC quebra expressões complexas em instruções simples de 3 operandos. Por exemplo, 'x = 5 + 3 * 2' vira três instruções: primeiro multiplica, depois soma, depois atribui. Isso facilita a geração de código assembly depois."

**Demonstração ao vivo:**
```bash
python demo_tac.py
```

---

# ETAPA 7: Ambientes de Execução 🎯 FOCO PRINCIPAL

## 📖 O que é?
Simular como um programa executa: gerenciar memória, chamadas de função e pilha de execução.

## 🎯 O que faz?
1. Gerencia memória (global e local)
2. Cria/destrói Activation Records (frames) ao chamar funções
3. Gerencia pilha de execução (runtime stack)
4. Controla escopo de variáveis

---

## 🏗️ PARTE 1: Tabela de Símbolos com Escopos

### 💻 Arquivo: `src/symbol_table.py`

### 📝 Explicação Detalhada:

#### Classe Symbol (Linhas 8-19):
```python
class Symbol:
    def __init__(self, name, symbol_type, scope, offset=0, is_param=False):
        self.name = name           # nome da variável
        self.type = symbol_type    # tipo (int, float, etc.)
        self.scope = scope         # em que função/escopo está
        self.offset = offset       # posição na memória
        self.is_param = is_param   # é parâmetro de função?
```

**O que cada campo faz:**
- `name`: identifica a variável (ex: "x", "soma")
- `type`: tipo de dado (ex: "int")
- `scope`: onde foi declarada (ex: "global", "main", "soma")
- `offset`: posição relativa na memória (0, 1, 2...)
- `is_param`: `True` se é parâmetro, `False` se é variável local

**Exemplo:**
```python
# Para a função: int soma(int a, int b)
Symbol("a", "int", "soma", offset=0, is_param=True)
Symbol("b", "int", "soma", offset=1, is_param=True)
```

#### Classe Scope (Linhas 22-52):
```python
class Scope:
    def __init__(self, name, parent=None, level=0):
        self.name = name              # nome do escopo
        self.parent = parent          # escopo pai (para busca)
        self.level = level            # nível de aninhamento
        self.symbols = {}             # dicionário de símbolos
        self.offset_counter = 0       # contador de offsets
```

**Estrutura de Escopos:**
```
global (level 0)
├── função main (level 1)
│   └── variável x
└── função soma (level 1)
    ├── parâmetro a
    ├── parâmetro b
    └── variável r
```

**Métodos importantes:**

1. **insert()** - Adiciona símbolo no escopo:
```python
def insert(self, name, symbol_type, is_param=False):
    if name in self.symbols:
        raise Exception(f"Variável '{name}' já existe!")
    
    symbol = Symbol(name, symbol_type, self.name, 
                   self.offset_counter, is_param)
    self.symbols[name] = symbol
    self.offset_counter += 1
    return symbol
```

2. **lookup()** - Busca símbolo (escopo léxico):
```python
def lookup(self, name):
    if name in self.symbols:
        return self.symbols[name]  # achou aqui
    elif self.parent:
        return self.parent.lookup(name)  # busca no pai
    return None  # não existe
```

**Exemplo de busca:**
```
Buscar "x" dentro da função soma:
1. Procura em soma → não tem
2. Procura no pai (global) → achou! ✅
```

#### Classe SymbolTable (Linhas 55-99):
```python
class SymbolTable:
    def __init__(self):
        self.global_scope = Scope("global")
        self.current_scope = self.global_scope
        self.scopes_stack = [self.global_scope]
```

**Métodos principais:**

1. **enter_scope()** - Entra em nova função:
```python
def enter_scope(self, scope_name):
    new_scope = Scope(scope_name, parent=self.current_scope, 
                     level=len(self.scopes_stack))
    self.scopes_stack.append(new_scope)
    self.current_scope = new_scope
```

**Visualização:**
```
Antes:  [global] ← current
Depois: [global, soma] ← current
```

2. **exit_scope()** - Sai da função:
```python
def exit_scope(self):
    self.scopes_stack.pop()
    self.current_scope = self.scopes_stack[-1]
```

**Visualização:**
```
Antes:  [global, soma] ← current
Depois: [global] ← current
```

## 🗣️ Como explicar:
> "A tabela de símbolos gerencia escopos aninhados. Quando entramos numa função, criamos um novo escopo. Quando procuramos uma variável, primeiro olhamos no escopo atual, se não achar, sobe para o pai (escopo léxico). Cada variável tem um offset que indica sua posição na memória."

---

## 🏗️ PARTE 2: Activation Records e Runtime Stack

### 💻 Arquivo: `src/runtime.py`

### 📝 Explicação Detalhada:

#### Classe ActivationRecord (Linhas 7-49):
```python
class ActivationRecord:
    def __init__(self, function_name, return_address=None):
        self.function_name = function_name
        self.parameters = {}          # parâmetros
        self.local_variables = {}     # variáveis locais
        self.return_value = None      # valor de retorno
        self.dynamic_link = None      # AR anterior (quem chamou)
        self.static_link = None       # AR do escopo pai
        self.return_address = return_address  # onde voltar
        self.temporaries = {}         # variáveis temporárias
```

**O que é um Activation Record (AR)?**
É como uma "caixa" que guarda todas as informações de uma chamada de função.

**Diagrama de um AR:**
```
┌────────────────────────────┐
│ function_name: "soma"      │
├────────────────────────────┤
│ parameters:                │
│   a: 2                     │
│   b: 3                     │
├────────────────────────────┤
│ local_variables:           │
│   r: 5                     │
├────────────────────────────┤
│ temporaries:               │
│   t1: 5                    │
├────────────────────────────┤
│ return_value: 5            │
├────────────────────────────┤
│ dynamic_link: → AR[main]   │
├────────────────────────────┤
│ return_address: "main+10"  │
└────────────────────────────┘
```

**Métodos:**

1. **set_parameter()** - Define parâmetro:
```python
def set_parameter(self, name, value):
    self.parameters[name] = value
```

2. **set_local()** - Define variável local:
```python
def set_local(self, name, value):
    self.local_variables[name] = value
```

3. **get_value()** - Busca valor:
```python
def get_value(self, name):
    if name in self.parameters:
        return self.parameters[name]
    elif name in self.local_variables:
        return self.local_variables[name]
    elif name in self.temporaries:
        return self.temporaries[name]
    return None
```

**Ordem de busca:** parâmetros → locais → temporárias

#### Classe RuntimeStack (Linhas 52-149):
```python
class RuntimeStack:
    def __init__(self):
        self.stack = []               # pilha de ARs
        self.global_memory = {}       # variáveis globais
```

**Estrutura da memória:**
```
┌─────────────────┐  ← Topo (cresce para cima)
│  AR[soma]       │
├─────────────────┤
│  AR[main]       │
├─────────────────┤
│  GLOBAL MEMORY  │
│  global_var: 100│
└─────────────────┘
```

**Métodos principais:**

1. **push()** - Empilha novo AR:
```python
def push(self, activation_record):
    if self.stack:
        activation_record.dynamic_link = self.stack[-1]  # link para anterior
    self.stack.append(activation_record)
    print(f"[PUSH] AR de '{activation_record.function_name}'")
```

**Visualização:**
```
Antes:  [AR[main]]
        ↓ push(AR[soma])
Depois: [AR[main], AR[soma]]
                    ↑ topo
```

2. **pop()** - Desempilha AR:
```python
def pop(self):
    ar = self.stack.pop()
    print(f"[POP] AR de '{ar.function_name}'")
    return ar
```

3. **get_value()** - Busca valor de variável:
```python
def get_value(self, name):
    # 1. Tenta no AR atual
    if self.stack:
        value = self.current_frame().get_value(name)
        if value is not None:
            return value
    
    # 2. Tenta na memória global
    if name in self.global_memory:
        return self.global_memory[name]
    
    # 3. Se é número, retorna direto
    if isinstance(name, (int, float)):
        return name
    
    raise Exception(f"Variável '{name}' não encontrada")
```

**Ordem de busca:**
1. AR atual (parâmetros, locais, temporárias)
2. Memória global
3. Se é constante numérica, retorna direto

## 🗣️ Como explicar:
> "O Activation Record é como uma caixa que guarda tudo de uma chamada de função: parâmetros, variáveis locais e onde voltar. A Runtime Stack é uma pilha dessas caixas. Quando chamamos uma função, empilhamos um novo AR. Quando ela retorna, desempilhamos."

**Demonstração visual:**
```bash
cd src
python runtime.py
```

**Você verá:**
```
Estado 1: [AR[main]]
Estado 2: [AR[main], AR[soma]]  ← chamou soma
Estado 3: [AR[main]]             ← soma retornou
Estado 4: []                     ← main retornou
```

---

## 🏗️ PARTE 3: Compilador Integrado

### 💻 Arquivo: `src/compiler_etapa7.py`

### 📝 Explicação Detalhada:

#### Classe Compiler (Linhas 148-243):

**Método compile():**
```python
def compile(self, ast):
    self._process(ast)
    return self.code
```

**Processamento de Funções:**
```python
elif node_type == 'func':
    func_name = node[1]
    params = node[2]
    body = node[3]
    
    # Emite label da função
    self._emit(f"FUNCTION {func_name}:")
    self._emit("BEGIN_FUNC")
    
    # Entra no escopo
    self.symbol_table.enter_scope(func_name)
    
    # Processa parâmetros
    for param in params:
        self.symbol_table.insert(param, 'int', is_param=True)
        self._emit(f"PARAM {param}")
    
    # Processa corpo
    self._process(body)
    
    # Termina função
    self._emit("END_FUNC")
    self.symbol_table.exit_scope()
```

**Processamento de Chamadas:**
```python
elif node_type == 'call':
    func = node[1]
    args = node[2]
    
    # Emite argumentos
    for arg in args:
        arg_result = self._process(arg)
        self._emit(f"ARG {arg_result}")
    
    # Emite chamada
    temp = new_temp()
    self._emit(f"{temp} = CALL {func}, {len(args)}")
    return temp
```

#### Classe Interpreter (Linhas 246-360):

**Método _call_function():**
```python
def _call(self, func, args):
    # 1. Cria AR
    ar = ActivationRecord(func)
    self.runtime.push(ar)
    
    # 2. Define parâmetros
    param_idx = 0
    while ...:
        if instr.startswith("PARAM "):
            param = instr.split()[1]
            if param_idx < len(args):
                ar.set_parameter(param, args[param_idx])
                param_idx += 1
    
    # 3. Executa instruções
    while pc < len(self.code):
        # ... processa cada instrução TAC ...
        
        # Quando encontra CALL, chama recursivamente
        if " CALL " in instr:
            result = self._call(called_func, call_args)
    
    # 4. Desempilha e retorna
    ar = self.runtime.pop()
    return ar.return_value
```

## 🗣️ Como explicar:
> "O compilador gera TAC incluindo instruções de função (FUNCTION, PARAM, CALL, RETURN). O interpretador executa esse TAC, criando ARs quando chama funções e destruindo quando retornam. É uma simulação de como um programa real executa."

---

## 🎬 EXEMPLO COMPLETO PASSO A PASSO

### Código:
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

### Passo 1: Análise Léxica
```
Tokens: [INT, ID(soma), LPAREN, INT, ID(a), ...]
```

### Passo 2: Análise Sintática
```
AST:
  program
  ├── func(soma, [a, b])
  │   └── r = a + b
  │       return r
  └── func(main, [])
      └── x = soma(2, 3)
          print(x)
```

### Passo 3: Análise Semântica
```
Tabela de Símbolos:
  Escopo global: (vazio)
  Escopo soma: a(int), b(int), r(int)
  Escopo main: x(int)
```

### Passo 4: Geração de TAC
```
FUNCTION soma:
BEGIN_FUNC
PARAM a
PARAM b
t1 = a + b
r = t1
RETURN r
END_FUNC

FUNCTION main:
BEGIN_FUNC
ARG 2
ARG 3
t2 = CALL soma, 2
x = t2
PRINT x
RETURN 0
END_FUNC
```

### Passo 5: Execução (Runtime)

**Estado 1: Início de main**
```
Runtime Stack:
┌────────────────┐
│ AR[main]       │ ← topo
│  locals: {}    │
└────────────────┘
```

**Estado 2: Chamada soma(2, 3)**
```
Runtime Stack:
┌────────────────┐
│ AR[soma]       │ ← topo
│  params: {a:2, │
│           b:3} │
│  locals: {}    │
├────────────────┤
│ AR[main]       │
│  locals: {}    │
└────────────────┘
```

**Estado 3: Executando r = a + b**
```
Runtime Stack:
┌────────────────┐
│ AR[soma]       │ ← topo
│  params: {a:2, │
│           b:3} │
│  locals: {r:5} │
│  temps: {t1:5} │
├────────────────┤
│ AR[main]       │
└────────────────┘
```

**Estado 4: Return de soma**
```
Runtime Stack:
┌────────────────┐
│ AR[main]       │ ← topo
│  locals: {x:5} │
└────────────────┘

AR[soma] foi desempilhado, retornou 5
```

**Estado 5: Print e fim**
```
>>> OUTPUT: 5

Runtime Stack: []
(pilha vazia)
```

---

## 🧪 COMO TESTAR TUDO

### Teste Completo:
```bash
cd src
python compiler_etapa7.py
```

### Testes Individuais:
```bash
# Lexer
python test_lexer.py

# TAC
python demo_tac.py

# Tabela de Símbolos
python symbol_table.py

# Runtime Stack
python runtime.py

# Chamadas Aninhadas
python test_nested.py
```

---

## 📊 CHECKLIST PARA APRESENTAÇÃO

### Etapa 2: Alfabeto e Tokens ✅
- [ ] Mostrar lista de tokens no `lexer.py`
- [ ] Explicar palavras reservadas
- [ ] Mostrar alfabeto no README

### Etapa 3: Análise Léxica ✅
- [ ] Mostrar ERs no código
- [ ] Demonstrar: `python test_lexer.py`
- [ ] Explicar como reconhece identificadores vs palavras reservadas

### Etapa 4: Análise Sintática ✅
- [ ] Mostrar gramática BNF
- [ ] Explicar precedência de operadores
- [ ] Demonstrar geração de AST

### Etapa 5: Análise Semântica ✅
- [ ] Mostrar tabela de símbolos
- [ ] Explicar inferência de tipos
- [ ] Mostrar AST anotada

### Etapa 6: Geração de TAC ✅
- [ ] Explicar formato de três endereços
- [ ] Demonstrar: `python demo_tac.py`
- [ ] Mostrar variáveis temporárias

### Etapa 7: Ambientes de Execução ✅
- [ ] Explicar Activation Record
- [ ] Demonstrar Runtime Stack: `python runtime.py`
- [ ] Mostrar compilador completo: `python compiler_etapa7.py`
- [ ] Explicar chamadas aninhadas: `python test_nested.py`

---

## 💡 DICAS PARA APRESENTAÇÃO

### 1. Ordem de Explicação:
1. Visão geral (fluxo completo)
2. Etapa por etapa (2 → 3 → 4 → 5 → 6 → 7)
3. Demonstração ao vivo da Etapa 7
4. Q&A

### 2. Demonstrações Ao Vivo:
```bash
# Mostrar lexer tokenizando
python test_lexer.py

# Mostrar TAC sendo gerado
python demo_tac.py

# DESTAQUE: Mostrar pilha em ação
python compiler_etapa7.py
```

### 3. Pontos-Chave da Etapa 7:

**Tabela de Símbolos:**
- "Gerencia escopos aninhados"
- "Busca léxica: procura local, depois sobe para global"
- "Cada variável tem offset (posição na memória)"

**Activation Record:**
- "É como uma caixa que guarda tudo de uma chamada"
- "Contém parâmetros, locais, temporárias e links"
- "Dynamic link aponta para quem chamou"

**Runtime Stack:**
- "Pilha de caixas (ARs)"
- "Push ao chamar, pop ao retornar"
- "Simula como CPU real executa"

### 4. Respostas para Perguntas Comuns:

**P: Por que usar TAC?**
R: "Formato intermediário entre alto nível e assembly. Facilita otimização e geração de código de máquina."

**P: O que é dynamic link?**
R: "Ponteiro para o AR anterior na pilha. Usado em tempo de execução para voltar após chamada."

**P: E static link?**
R: "Ponteiro para escopo léxico pai. Útil para closures e funções aninhadas (não implementado aqui)."

**P: Por que offsets?**
R: "Calculam posição relativa das variáveis no AR. Na memória real, seria usado para endereçamento."

---

## 🎯 RESUMO EXECUTIVO

| Etapa | O que faz | Arquivo Principal | Teste |
|-------|-----------|-------------------|-------|
| 2 | Define alfabeto e tokens | `lexer.py` | Documentado no README |
| 3 | Tokeniza código (ERs) | `lexer.py` | `test_lexer.py` |
| 4 | Verifica sintaxe (gramática) | `codegen.py` | `python codegen.py` |
| 5 | Verifica semântica (tipos) | `codegen.py` | Integrado |
| 6 | Gera TAC | `codegen.py` | `demo_tac.py` |
| 7 | Simula execução | `compiler_etapa7.py` | `compiler_etapa7.py` |

**Fluxo Completo:**
```
Código → Lexer → Tokens → Parser → AST → 
Semântica → AST Anotada → CodeGen → TAC → 
Interpretador → Execução (com Runtime Stack)
```

---

Boa sorte na apresentação! 🚀
