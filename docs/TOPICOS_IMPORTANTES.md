# 📋 Tópicos Importantes para Funcionamento do Compilador

---

## 🎯 Resumo Executivo

O compilador é composto por **7 fases principais** que trabalham de forma integrada. Cada fase tem responsabilidades claras:

| Fase | Arquivo | Função | Status |
|------|---------|--------|--------|
| 1️⃣ **Léxico** | `lexer.py` | Tokenização | ✅ Completo |
| 2️⃣ **Sintático** | `parser.py` | Parse LL(1) | ✅ Completo |
| 3️⃣ **AST** | `ast/ast_builder.py` | Árvore Sintática | ✅ Completo |
| 4️⃣ **Semântica** | `ast/analyzer.py` | Análise Semântica | ✅ Completo |
| 5️⃣ **IR** | `ir/ir_generator.py` | TAC + Quádruplas | ✅ Completo |
| 6️⃣ **Otimização** | `optimizer/optimizer.py` | Otimizações | ✅ Completo |
| 7️⃣ **Assembly** | `codegen/assembly.py` | Geração Assembly | ✅ Completo |

---

# 📍 TÓPICOS PRINCIPAIS

## 1️⃣ **LEXER (Análise Léxica)**

### 📁 Arquivo Principal
- **`compiler/lexer.py`** — 76 linhas

### 🎯 Objetivo
Converter texto bruto em **tokens** (unidades léxicas)

### 🔧 O que faz

```python
# ENTRADA: "int x = 5 + 3;"
# SAÍDA: [INT, ID('x'), EQUALS, NUMBER(5), PLUS, NUMBER(3), SEMICOLON]
```

### 📋 Componentes Principais

#### 1. **Tokens Definidos** (21 tipos)
```python
tokens = (
    'ID', 'NUMBER',                              # Identificadores e números
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS',  # Operadores
    'LT', 'GT', 'LE', 'GE', 'EQ', 'NE',        # Comparadores
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',     # Delimitadores
    'SEMICOLON', 'COMMA',                        # Pontuação
)
```

#### 2. **Palavras Reservadas** (7 palavras-chave)
```python
reserved = {
    'if': 'IF',
    'else': 'ELSE', 
    'while': 'WHILE',
    'for': 'FOR',
    'return': 'RETURN',
    'int': 'INT',
    'print': 'PRINT'
}
```

#### 3. **Regras Léxicas** (Regex)
```python
# Tokens simples (1 caractere)
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
...

# Identificadores e palavras-chave
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # Verifica se é palavra-chave
    return t

# Números (inteiros)
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Quebras de linha (rastreamento)
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignora espaços
t_ignore = ' \t'

# Tratamento de erros
def t_error(t):
    print(f"[ERRO LÉXICO] Caractere ilegal '{t.value[0]}'")
    t.lexer.skip(1)
```

#### 4. **Função Principal**
```python
def tokenize(source_code):
    """Retorna lista de tokens do código-fonte"""
    local_lexer = lex.lex()
    local_lexer.input(source_code)
    return list(local_lexer)
```

### 🔍 Exemplo Real

```
ENTRADA:        "int x = 5;"
                 ↓
TOKENIZAÇÃO:    [INT, ID('x'), EQUALS, NUMBER(5), SEMICOLON]
                 ↓
SAÍDA:          [
                  Token(INT, 'int', 1),
                  Token(ID, 'x', 1),
                  Token(EQUALS, '=', 1),
                  Token(NUMBER, 5, 1),
                  Token(SEMICOLON, ';', 1)
                ]
```

### ⚙️ Dependência Externa
- **PLY (Python Lex-Yacc)** — biblioteca de lexing automático

---

## 2️⃣ **PARSER (Análise Sintática)**

### 📁 Arquivo Principal
- **`compiler/parser.py`** — 358 linhas

### 🎯 Objetivo
Converter tokens em **árvore sintática** (Parse Tree)

### 🔧 Tipo de Parser
- **LL(1) Top-Down** — Recursive Descent com lookahead de 1 token
- **Não-ambíguo** — Uma única forma de parser

### 📋 Estrutura do Parser

#### 1. **Classe Principal**
```python
class LL1Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0                    # Position no stream
        self.current_token = tokens[0]  # Token atual
        self.errors = []                # Erros encontrados
```

#### 2. **Métodos Essenciais**
```python
def match(self, expected_type):
    """Verifica e consome um token esperado"""
    if self.current_token.type == expected_type:
        token = self.current_token
        self.advance()
        return token
    else:
        self.error(f"Esperado {expected_type}")
        return None

def peek(self):
    """Olha 1 token à frente sem consumir"""
    return self.current_token.type

def advance(self):
    """Avança para próximo token"""
    self.pos += 1
    if self.pos < len(self.tokens):
        self.current_token = self.tokens[self.pos]
```

#### 3. **Funções de Parsing** (Um método por não-terminal)

```python
# PROGRAMA → DECLARAÇÃO*
def program(self):
    declarations = self.declaration_list()
    return ('program', declarations)

# DECLARAÇÃO → FUNÇÃO | STATEMENT
def declaration(self):
    if self.peek() == 'INT':
        # Tenta diferenciar função vs atribuição
        if eh_funcao():
            return self.function_declaration()
        else:
            return self.statement()

# FUNÇÃO → INT ID ( PARAMS ) { STATEMENTS }
def function_declaration(self):
    self.match('INT')
    name = self.match('ID').value
    self.match('LPAREN')
    params = self.parameter_list() if self.peek() != 'RPAREN' else []
    self.match('RPAREN')
    self.match('LBRACE')
    body = self.statement_list()
    self.match('RBRACE')
    return ('function', name, params, body)

# EXPRESSÃO → COMPARAÇÃO
def expression(self):
    return self.comparison()

# COMPARAÇÃO → TERMO ((< | > | <= | >=) TERMO)*
def comparison(self):
    left = self.term()
    while self.peek() in ['LT', 'GT', 'LE', 'GE', 'EQ', 'NE']:
        op = self.current_token.type
        self.advance()
        right = self.term()
        left = (op, left, right)  # Node binário
    return left

# TERMO → FATOR ((+ | -) FATOR)*
def term(self):
    left = self.factor()
    while self.peek() in ['PLUS', 'MINUS']:
        op = self.current_token.value
        self.advance()
        right = self.factor()
        left = (op, left, right)  # Node binário
    return left

# FATOR → NÚMERO | ID | EXPRESSÃO_PARÊNTESES
def factor(self):
    if self.peek() == 'NUMBER':
        return self.match('NUMBER').value
    elif self.peek() == 'ID':
        return self.match('ID').value
    elif self.peek() == 'LPAREN':
        self.advance()
        expr = self.expression()
        self.match('RPAREN')
        return expr
```

#### 4. **Gramática BNF Implícita**

```
program        → declaration_list
declaration_list → declaration*
declaration    → function_declaration | statement

function_declaration 
               → INT ID LPAREN parameter_list? RPAREN LBRACE statement_list RBRACE

parameter_list → parameter (COMMA parameter)*
parameter      → INT ID

statement_list → statement*
statement      → decl_assign | assign | print_stmt | return_stmt | if_stmt | while_stmt | for_stmt

decl_assign    → INT ID EQUALS expression SEMICOLON
assign         → ID EQUALS expression SEMICOLON
print_stmt     → PRINT LPAREN expression RPAREN SEMICOLON
return_stmt    → RETURN expression? SEMICOLON

if_stmt        → IF LPAREN expression RPAREN LBRACE statement_list RBRACE (ELSE LBRACE statement_list RBRACE)?
while_stmt     → WHILE LPAREN expression RPAREN LBRACE statement_list RBRACE
for_stmt       → FOR LPAREN statement expression SEMICOLON statement RPAREN LBRACE statement_list RBRACE

expression     → comparison
comparison     → term ((LT | GT | LE | GE | EQ | NE) term)*
term           → factor ((PLUS | MINUS) factor)*
factor         → (TIMES | DIVIDE) factor | unary

unary          → MINUS unary | primary
primary        → NUMBER | ID | LPAREN expression RPAREN
```

### 📊 Exemplo Real

```
ENTRADA TOKENS:
  [INT, ID('x'), EQUALS, NUMBER(5), SEMICOLON]

PARSING:
  program()
    → declaration_list()
      → declaration()
        → statement()
          → decl_assign()
            → match('INT')
            → match('ID') → 'x'
            → match('EQUALS')
            → expression() → NUMBER(5)
            → match('SEMICOLON')

PARSE TREE RETORNADO:
  ('program', [
    ('decl_assign', 'x', 5)
  ])
```

---

## 3️⃣ **AST (Árvore Sintática Abstrata)**

### 📁 Arquivos
- **`compiler/ast/ast_builder.py`** — Construir AST
- **`compiler/ast/analyzer.py`** — Análise Semântica
- **`compiler/ast/symbol_table.py`** — Tabela de Símbolos

### 🎯 Objetivo
Transformar Parse Tree em **estrutura semântica** mais limpa

### 📋 Tipos de Nós

```python
class ASTNode:
    """Classe base para todos nós AST"""
    def __init__(self, node_type):
        self.node_type = node_type

class ProgramNode(ASTNode):
    def __init__(self, declarations):
        super().__init__('program')
        self.declarations = declarations

class FunctionNode(ASTNode):
    def __init__(self, name, params, body):
        super().__init__('function')
        self.name = name
        self.params = params
        self.body = body

class DeclAssignNode(ASTNode):
    def __init__(self, name, value):
        super().__init__('decl_assign')
        self.name = name
        self.value = value

class BinOpNode(ASTNode):
    def __init__(self, op, left, right):
        super().__init__('binop')
        self.op = op
        self.left = left
        self.right = right

class IfNode(ASTNode):
    def __init__(self, condition, then_block, else_block=None):
        super().__init__('if')
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

class WhileNode(ASTNode):
    def __init__(self, condition, body):
        super().__init__('while')
        self.condition = condition
        self.body = body
```

---

## 4️⃣ **ANÁLISE SEMÂNTICA**

### 📁 Arquivo Principal
- **`compiler/ast/analyzer.py`** — 164 linhas

### 🎯 Objetivo
Validar **tipos, escopos e declarações**

### 🔧 Verificações Realizadas

1. **Verificação de Tipos**
   ```python
   # ✅ Tipo correto
   int x = 5;           # OK
   
   # ❌ Tipo incorreto
   int x = "string";    # ERRO
   ```

2. **Verificação de Declaração**
   ```python
   # ✅ Variável declarada
   int x = 5;
   print(x);            # OK
   
   # ❌ Variável não declarada
   print(y);            # ERRO: Variável 'y' não declarada
   ```

3. **Verificação de Escopo**
   ```python
   int main() {
       int x = 5;       # Escopo global
       if (x > 0) {
           int y = 10;  # Escopo local do if
       }
       print(y);        # ERRO: 'y' não existe neste escopo
   }
   ```

4. **Verificação de Duplicatas**
   ```python
   int x = 5;
   int x = 10;          # ERRO: Variável 'x' já declarada
   ```

5. **Verificação de Return**
   ```python
   int soma(int a, int b) {
       int r = a + b;
       return r;        # OK
   }
   
   int funcao() {
       int x = 5;
       # ERRO: Função 'funcao' precisa de 'return'
   }
   ```

### 📋 Classe Principal

```python
class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors = []
        self.current_function = None
    
    def analyze(self, ast_node):
        """Retorna: (sucesso, erros, tabela_símbolos)"""
        self.errors = []
        self.visit(ast_node)
        return len(self.errors) == 0, self.errors, self.symbol_table
    
    def visit(self, node):
        """Padrão Visitor para AST"""
        method_name = f'visit_{node.node_type}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
```

### 📊 Tabela de Símbolos

```python
class SymbolTable:
    """Gerencia escopos e símbolos"""
    def __init__(self):
        self.scopes = [{}]  # Lista de dicts (escopos)
    
    def insert(self, name, var_type, is_param=False):
        """Insere símbolo no escopo atual"""
        self.scopes[-1][name] = {
            'type': var_type,
            'is_param': is_param,
            'offset': len(self.scopes[-1])
        }
    
    def lookup(self, name):
        """Busca símbolo em todos escopos"""
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None
    
    def enter_scope(self, name):
        """Entra em novo escopo (função, bloco)"""
        self.scopes.append({})
    
    def exit_scope(self):
        """Sai do escopo atual"""
        self.scopes.pop()
```

---

## 5️⃣ **IR GENERATOR (Geração de Código Intermediário)**

### 📁 Arquivo Principal
- **`compiler/ir/ir_generator.py`** — 202 linhas

### 🎯 Objetivo
Converter AST em **Three-Address Code (TAC) / Quádruplas**

### 🔧 Método de Geração

Usa padrão **Visitor** para percorrer AST:

```python
class IRGenerator:
    def __init__(self, symbol_table):
        self.ir_program = IRProgram()
        self.temp_counter = 0
        self.label_count = 0
    
    def new_temp(self):
        """Cria variável temporária única"""
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp
    
    def new_label(self):
        """Cria label único"""
        label = f"L{self.label_count}"
        self.label_count += 1
        return label
    
    def emit(self, op, a1=None, a2=None, res=None):
        """Emite quádrupla"""
        self.ir_program.emit(op, a1, a2, res)
```

### 📋 Visitadores (um por tipo de nó)

```python
# OPERAÇÕES ARITMÉTICAS
def visit_binop(self, node):
    left = self.visit(node.left)
    right = self.visit(node.right)
    temp = self.new_temp()
    self.emit(node.op, left, right, temp)  # (op, left, right, temp)
    return temp

# ATRIBUIÇÃO
def visit_assign(self, node):
    val = self.visit(node.value)
    self.emit('assign', val, None, node.name)  # (assign, valor, -, var)

# PRINT
def visit_print(self, node):
    val = self.visit(node.value)
    self.emit('print', val)  # (print, valor, -, -)

# RETORNO
def visit_return(self, node):
    if node.value:
        val = self.visit(node.value)
        self.emit('return', val)  # (return, valor, -, -)

# IF/ELSE
def visit_if(self, node):
    cond = self.visit(node.condition)
    Ltrue = self.new_label()
    Lfalse = self.new_label()
    Lend = self.new_label()
    
    self.emit('IF_GOTO', cond, None, Ltrue)    # (IF_GOTO, cond, -, Ltrue)
    self.emit('GOTO', None, None, Lfalse)      # (GOTO, -, -, Lfalse)
    self.emit('LABEL', None, None, Ltrue)      # (LABEL, -, -, Ltrue)
    # ... corpo ...
    self.emit('LABEL', None, None, Lend)       # (LABEL, -, -, Lend)

# WHILE
def visit_while(self, node):
    Lbegin = self.new_label()
    Lend = self.new_label()
    
    self.emit('LABEL', None, None, Lbegin)     # (LABEL, -, -, Lbegin)
    cond = self.visit(node.condition)
    self.emit('IF_FALSE_GOTO', cond, None, Lend)  # (IF_FALSE_GOTO, cond, -, Lend)
    # ... corpo ...
    self.emit('GOTO', None, None, Lbegin)      # (GOTO, -, -, Lbegin)
    self.emit('LABEL', None, None, Lend)       # (LABEL, -, -, Lend)
```

---

## 6️⃣ **OPTIMIZER (Otimizações)**

### 📁 Arquivos
- **`compiler/optimizer/optimizer.py`** — 237 linhas
- **`compiler/optimizer/peephole.py`** — Otimizações aritméticas

### 🎯 Objetivo
Reduzir tamanho e melhorar eficiência do código intermediário

### 🔧 Otimizações Implementadas

| Otimização | Antes | Depois | Redução |
|-----------|-------|--------|---------|
| **CSE** (Common Subexpression Elimination) | `t1=a+b; t2=a+b` | `t1=a+b; t2=t1` | 1 instr |
| **Constant Folding** | `t0 = 3 * 2` | `t0 = 6` | simplify |
| **Algebraic Simplification** | `t0 = 3 * 2` | `t0 = 3 << 1` | shift otimizado |
| **Dead Code Elimination** | `t1 = a + b; ... (t1 não usado)` | removido | 1 instr |
| **Copy Propagation** | `t1 = x; y = t1` | `y = x` | propaga |
| **Peephole Optimization** | `x * 2` | `x << 1` | mais eficiente |

### 📋 Exemplo Real

```
CÓDIGO ORIGINAL:
  t0 = 3 * 2      ← Constant Folding
  t1 = 5 + t0
  t2 = t1 - 1
  resultado = t2  ← Copy Propagation
  print resultado
  return 0

APÓS CONSTANT FOLDING:
  t0 = 6
  t1 = 5 + 6
  t2 = t1 - 1
  resultado = t2
  print resultado
  return 0

APÓS COPY PROPAGATION:
  t1 = 5 + 6
  t2 = t1 - 1
  resultado = t2
  print resultado
  return 0

APÓS CONSTANT FOLDING (novamente):
  resultado = 10
  print resultado
  return 0

REDUÇÃO: 7 → 3 instruções (57% redução!)
```

---

## 7️⃣ **CODEGEN (Geração de Assembly)**

### 📁 Arquivos
- **`compiler/codegen/codegen.py`** — Coordenador
- **`compiler/codegen/assembly.py`** — Gerador assembly

### 🎯 Objetivo
Converter IR otimizado em **assembly MIPS-like**

### 🔧 Instruções Geradas

```
ENTER                   ← Inicializa frame
LOAD R0, valor          ← Carrega valor em R0
STORE R0, variável      ← Armazena R0 em variável
ADD R0, R1              ← Soma R0 + R1 → R0
SUB R0, R1              ← Subtrai R0 - R1 → R0
MUL R0, R1              ← Multiplica R0 * R1 → R0
SHL R0, n               ← Shift left (R0 << n)
PRINT R0                ← Imprime valor de R0
RET n                   ← Return com valor
LEAVE                   ← Limpa frame
RETURN                  ← Jump volta
```

### 📊 Exemplo Real

```
ENTRADA (IR):
  resultado = 10
  print resultado
  return 0

ASSEMBLY GERADO:
main:
  ENTER
  LOAD R0, 10              ← Carrega 10 em R0
  STORE R0, resultado      ← Guarda em resultado
  PRINT R0                 ← Imprime 10
  RET 0                    ← Return 0
  LEAVE
  RETURN
```

---

## 🧪 **TESTES**

### 📁 Arquivos de Teste
```
tests/
├── alocation.txt         ← Alocação de memória
├── code.txt              ← Código completo
├── conditional.txt       ← IF/ELSE
├── expressao_simples.txt ← Expressões aritméticas
├── function.txt          ← Funções
├── hello_world.txt       ← Hello world
├── loop.txt              ← Loops (WHILE, FOR)
├── rename.txt            ← Renomeação de variáveis
└── simples.txt           ← Código simples
```

### 🔧 Como Rodar Testes

```bash
# Teste rápido
python test_final.py

# Compilar arquivo
python run.py -f tests/expressao_simples.txt

# Modo interativo
python run.py

# Com verbose
python run.py -f tests/code.txt --verbose

# Salvar assembly
python run.py -f tests/code.txt -o output.asm
```

### 📋 Teste Exemplo

```python
from compiler import compile

codigo = """
int main() {
    int a = 7;
    int b = 8;
    int r = (a + b) * 2;
    return 0;
}
"""

result = compile(codigo, optimize=True, verbose=False)

if result['success']:
    print("✅ Compilação bem-sucedida!")
    print(f"  Tokens: {len(result['tokens'])}")
    print(f"  IR: {len(result['ir'].get_instructions())} instruções")
    print(f"  IR Otimizado: {len(result['optimized_ir'].get_instructions())} instruções")
    for linha in result['assembly']:
        print(linha)
```

---

## 📊 **FLUXO COMPLETO**

```
Código Fonte (.py, .txt, .c)
    ↓
[LEXER] → Tokenização
    ↓ TOKENS
[PARSER LL(1)] → Parse Tree
    ↓ PARSE TREE
[AST BUILDER] → AST
    ↓ AST
[SEMANTIC ANALYZER] → Tabela Símbolos
    ↓ VALIDADO
[IR GENERATOR] → TAC/Quádruplas
    ↓ CÓDIGO INTERMEDIÁRIO
[OPTIMIZER] → CSE, CF, DCE, CP, Peephole
    ↓ IR OTIMIZADO
[CODEGEN] → Assembly MIPS-like
    ↓ ASSEMBLY
[OUTPUT] → Arquivo .asm ou console
```

---

## 🔗 **Integração de Componentes**

```
┌─────────────────────────────────────────────────────────┐
│                  compiler/main.py                       │
│  (Orquestrador do pipeline completo)                    │
└─────────────────────────────────────────────────────────┘
        ↓              ↓              ↓
    LEXER         PARSER            AST
  (lexer.py)   (parser.py)    (ast_builder.py)
        ↓              ↓              ↓
    TOKENS       PARSE TREE         AST
        └──────────────┬──────────────┘
                       ↓
            ┌──────────────────────────┐
            │ SEMANTIC ANALYZER        │
            │ (ast/analyzer.py)        │
            │ + Symbol Table           │
            └──────────────────────────┘
                       ↓
            ┌──────────────────────────┐
            │ IR GENERATOR             │
            │ (ir/ir_generator.py)     │
            └──────────────────────────┘
                       ↓
            TAC/QUÁDRUPLAS (IR)
                       ↓
            ┌──────────────────────────┐
            │ OPTIMIZER                │
            │ (optimizer/optimizer.py) │
            │ - CSE, CF, DCE, CP       │
            │ - Peephole               │
            └──────────────────────────┘
                       ↓
            IR OTIMIZADO
                       ↓
            ┌──────────────────────────┐
            │ CODE GENERATOR           │
            │ (codegen/codegen.py)     │
            └──────────────────────────┘
                       ↓
            ASSEMBLY MIPS-like
                       ↓
        ┌──────────────────────────┐
        │ OUTPUT (run.py)          │
        │ - Console                │
        │ - Arquivo .asm           │
        └──────────────────────────┘
```

---

## 🎓 **Resumo dos Tópicos Críticos**

| Tópico | Criticidade | Por quê |
|--------|-------------|---------|
| **Lexer** | ⭐⭐⭐⭐⭐ | Sem tokens, não há parsing |
| **Parser LL(1)** | ⭐⭐⭐⭐⭐ | Gramática é a espinha dorsal |
| **AST** | ⭐⭐⭐⭐ | Intermediária entre parse e semântica |
| **Análise Semântica** | ⭐⭐⭐⭐⭐ | Verifica validade do código |
| **IR Generator** | ⭐⭐⭐⭐ | Transforma em código executável |
| **Optimizer** | ⭐⭐⭐ | Melhora eficiência (opcional) |
| **Codegen** | ⭐⭐⭐⭐⭐ | Produz resultado final |
| **Testes** | ⭐⭐⭐⭐ | Validam cada fase |

---

## 🚀 **Para Começar**

1. **Entender Lexer** → Tokens
2. **Entender Parser** → Gramática BNF
3. **Entender AST** → Nodes
4. **Entender Semântica** → Validação
5. **Entender IR** → Quádruplas
6. **Entender Otimizações** → Redução
7. **Entender Codegen** → Assembly
