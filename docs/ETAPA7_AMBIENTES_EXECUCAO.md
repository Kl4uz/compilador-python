# Etapa 7 - Ambientes de Execução

## 📋 Documentação Completa

### Equipe:
- Lucas Farias
- José Lucas
- Ester Araiz
- Henrique Noronha

---

## 🎯 Objetivos da Etapa 7

Implementar um sistema completo de **Ambientes de Execução** que simula a execução de funções através de:

1. **Modelagem do Ambiente de Execução**
2. **Implementação de Activation Records (Registros de Ativação)**
3. **Integração com Tabela de Símbolos**

---

## 🏗️ Atividade 1 - Modelagem do Ambiente de Execução

### Organização de Memória

O compilador simula a seguinte organização de memória:

```
┌─────────────────────────┐  ← Endereços altos
│   RUNTIME STACK         │  (Pilha de Execução)
│   - Activation Records  │  - Cresce para baixo
│   - Variáveis Locais    │  - Gerenciada dinamicamente
│   - Parâmetros          │
├─────────────────────────┤
│   HEAP                  │  (Não implementado nesta etapa)
│   (Alocação Dinâmica)   │
├─────────────────────────┤
│   MEMÓRIA GLOBAL        │  (Variáveis Globais)
│   - Variáveis estáticas │  - Tamanho fixo
├─────────────────────────┤
│   CÓDIGO TAC            │  (Código Intermediário)
│   - Instruções          │  - Read-only
│   - Labels de funções   │
└─────────────────────────┘  ← Endereços baixos
```

### Comportamento da Pilha de Ativação

A pilha de execução funciona da seguinte forma:

1. **Chamada de Função:**
   - Um novo **Activation Record (AR)** é criado
   - O AR é **empilhado** (push) no topo da runtime stack
   - Parâmetros são copiados para o AR
   - Controle é transferido para o início da função

2. **Execução:**
   - Variáveis locais são alocadas no AR atual
   - Operações acessam variáveis do AR ou memória global
   - Variáveis temporárias são armazenadas no AR

3. **Retorno de Função:**
   - Valor de retorno é armazenado no AR
   - AR é **desempilhado** (pop) da runtime stack
   - Valor de retorno é copiado para o chamador
   - Controle retorna ao ponto de chamada

### Armazenamento de Variáveis

| Tipo de Variável | Localização | Acesso |
|-----------------|-------------|--------|
| **Globais** | Memória Global (dicionário) | Nome direto |
| **Locais** | AR.local_variables | Nome no escopo atual |
| **Parâmetros** | AR.parameters | Nome no escopo da função |
| **Temporárias** | AR.temporaries | Nome (t1, t2, ...) |

**Algoritmo de Busca de Variáveis:**
```python
def get_value(name):
    if exists_in_current_AR(name):
        return current_AR.get(name)
    elif exists_in_global_memory(name):
        return global_memory[name]
    else:
        error("Variable not found")
```

---

## 🗂️ Atividade 2 - Implementação do Activation Record

### Estrutura do Activation Record

Implementado no arquivo: **`src/runtime.py`**

```python
class ActivationRecord:
    def __init__(self, function_name, return_address=None):
        self.function_name = function_name           # Nome da função
        self.parameters = {}                         # Parâmetros formais
        self.local_variables = {}                    # Variáveis locais
        self.return_value = None                     # Valor de retorno
        self.dynamic_link = None                     # Link para AR do chamador
        self.static_link = None                      # Link para escopo léxico pai
        self.return_address = return_address         # Endereço de retorno
        self.temporaries = {}                        # Variáveis temporárias
```

### Componentes do AR:

| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| **function_name** | Identificação da função | "soma", "main" |
| **parameters** | Dicionário {nome: valor} dos parâmetros | {"a": 2, "b": 3} |
| **local_variables** | Dicionário {nome: valor} das variáveis locais | {"r": 5} |
| **return_value** | Valor que a função retorna | 5 |
| **dynamic_link** | Ponteiro para o AR anterior na pilha | AR[main] |
| **static_link** | Ponteiro para escopo léxico pai (para closures) | Não usado nesta etapa |
| **return_address** | Endereço (PC) para continuar após return | "main+5" |
| **temporaries** | Variáveis temporárias (t1, t2, etc.) | {"t1": 5} |

### Demonstração de Criação e Destruição

**Exemplo de execução:**

```c
int soma(int a, int b) {
    int r = a + b;
    return r;
}

int main() {
    int x = soma(2, 3);
}
```

**Trace da Pilha:**

```
Estado 1: Início de main()
┌───────────────────┐
│ AR[main]          │ ← Topo
│  locals: {}       │
└───────────────────┘

Estado 2: Chamada soma(2, 3)
┌───────────────────┐
│ AR[soma]          │ ← Topo
│  params: {a:2, b:3}
│  locals: {}       │
├───────────────────┤
│ AR[main]          │
│  locals: {}       │
└───────────────────┘

Estado 3: Execução r = a + b
┌───────────────────┐
│ AR[soma]          │ ← Topo
│  params: {a:2, b:3}
│  locals: {r: 5}   │
│  temps: {t1: 5}   │
├───────────────────┤
│ AR[main]          │
│  locals: {}       │
└───────────────────┘

Estado 4: Return de soma
┌───────────────────┐
│ AR[main]          │ ← Topo
│  locals: {x: 5}   │
└───────────────────┘

Estado 5: Return de main
(Pilha vazia)
```

---

## 🔗 Atividade 3 - Integração com Tabela de Símbolos

### Tabela de Símbolos com Escopos

Implementado no arquivo: **`src/symbol_table.py`**

```python
class SymbolTable:
    def __init__(self):
        self.global_scope = Scope("global", parent=None, level=0)
        self.current_scope = self.global_scope
        self.scopes_stack = [self.global_scope]
    
    def enter_scope(self, scope_name):
        """Entra em um novo escopo (função)"""
        new_scope = Scope(scope_name, parent=self.current_scope, 
                         level=len(self.scopes_stack))
        self.scopes_stack.append(new_scope)
        self.current_scope = new_scope
    
    def exit_scope(self):
        """Sai do escopo atual"""
        self.scopes_stack.pop()
        self.current_scope = self.scopes_stack[-1]
```

### Estrutura de um Symbol:

```python
class Symbol:
    def __init__(self, name, symbol_type, scope, offset=0, is_param=False):
        self.name = name              # Nome da variável
        self.type = symbol_type       # Tipo (int, float, etc.)
        self.scope = scope            # Escopo onde foi declarada
        self.offset = offset          # Offset no AR
        self.is_param = is_param      # É parâmetro?
```

### Exemplo de Tabela de Símbolos:

Para o código:
```c
int global_var;

int soma(int a, int b) {
    int r = a + b;
    return r;
}

int main() {
    int x = soma(2, 3);
}
```

**Tabela Resultante:**

```
┌─────────────────────────────────────────┐
│ ESCOPO: global (Nível 0)                │
├─────────────────────────────────────────┤
│ global_var: int (offset=0)              │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ ESCOPO: soma (Nível 1)                  │
├─────────────────────────────────────────┤
│ a: int (offset=0) [PARAM]               │
│ b: int (offset=1) [PARAM]               │
│ r: int (offset=2)                       │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ ESCOPO: main (Nível 1)                  │
├─────────────────────────────────────────┤
│ x: int (offset=0)                       │
└─────────────────────────────────────────┘
```

### Distinção entre Variáveis Globais e Locais

O compilador distingue variáveis globais e locais através do **escopo na tabela de símbolos**:

```python
def lookup_variable(name):
    """Busca variável seguindo escopo léxico"""
    # 1. Procura no escopo atual (local)
    symbol = current_scope.lookup_local(name)
    if symbol:
        return symbol
    
    # 2. Procura nos escopos pais (global)
    parent = current_scope.parent
    while parent:
        symbol = parent.lookup_local(name)
        if symbol:
            return symbol
        parent = parent.parent
    
    # 3. Não encontrou
    return None
```

### Simulação de Recuperação de Valores durante Chamada

O interpretador recupera valores usando a **RuntimeStack**:

```python
def get_value(self, name):
    """Busca valor de variável"""
    # 1. Tenta buscar no AR atual (topo da pilha)
    if self.stack:
        current_ar = self.current_frame()
        
        # Verifica parâmetros
        if name in current_ar.parameters:
            return current_ar.parameters[name]
        
        # Verifica variáveis locais
        if name in current_ar.local_variables:
            return current_ar.local_variables[name]
        
        # Verifica temporárias
        if name in current_ar.temporaries:
            return current_ar.temporaries[name]
    
    # 2. Se não encontrou, busca na memória global
    if name in self.global_memory:
        return self.global_memory[name]
    
    # 3. Se é constante numérica, retorna diretamente
    if isinstance(name, (int, float)):
        return name
    
    # 4. Erro: variável não encontrada
    raise Exception(f"Variable '{name}' not found")
```

---

## 🧪 Teste Completo do Sistema

### Código de Teste:

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

### Executando:

```bash
python src/compiler_etapa7.py
```

### Saída Completa:

```
==================================================
CÓDIGO FONTE:
==================================================
int soma(int a, int b) {
    int r = a + b;
    return r;
}

int main() {
    int x = soma(2, 3);
    print(x);
    return 0;
}

==================================================
COMPILAÇÃO:
==================================================
AST: ('program', [('func', 'soma', ['a', 'b'], ...)])

==================================================
CÓDIGO INTERMEDIÁRIO (TAC):
==================================================
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

==================================================
EXECUÇÃO:
==================================================
[PUSH] Empilhando AR para 'main' (profundidade: 1)
[PUSH] Empilhando AR para 'soma' (profundidade: 2)
[POP] Desempilhando AR de 'soma' (profundidade: 1)
>>> OUTPUT: 5
[POP] Desempilhando AR de 'main' (profundidade: 0)

==================================================
ESTADO FINAL DA PILHA:
==================================================
(Pilha vazia)
```

---

## 📁 Estrutura de Arquivos

```
src/
├── lexer.py              # Análise Léxica (estendido com tokens de funções)
├── symbol_table.py       # Tabela de Símbolos com Escopos
├── runtime.py            # Activation Record + Runtime Stack
├── compiler_etapa7.py    # Compilador Completo (Parser + CodeGen + Interpreter)
└── interpreter.py        # Interpretador TAC (standalone)

tests/
└── test_functions.txt    # Código de teste
```

---

## 🚀 Como Usar

### 1. Teste as Estruturas Individualmente:

```bash
# Testar Tabela de Símbolos
python src/symbol_table.py

# Testar Runtime Stack
python src/runtime.py

# Testar Interpretador
python src/interpreter.py
```

### 2. Compilação e Execução Completa:

```bash
python src/compiler_etapa7.py
```

### 3. Criar Seu Próprio Código:

Crie um arquivo `.txt` com código na sintaxe suportada e modifique o `compiler_etapa7.py` para lê-lo:

```python
with open("tests/meu_codigo.txt") as f:
    code = f.read()
```

---

## ✅ Funcionalidades Implementadas

### Atividade 1 - Modelagem:
- ✅ Organização de memória (Global + Stack)
- ✅ Comportamento da pilha com push/pop
- ✅ Distinção entre variáveis globais, locais e parâmetros

### Atividade 2 - Activation Record:
- ✅ Estrutura completa do AR
- ✅ Parâmetros formais
- ✅ Variáveis locais e temporárias
- ✅ Valor de retorno
- ✅ Links dinâmico e estático
- ✅ Endereço de retorno
- ✅ Demonstração de criação/destruição

### Atividade 3 - Integração:
- ✅ Tabela de símbolos com escopos aninhados
- ✅ Associação de escopo e offset às variáveis
- ✅ Distinção global vs local
- ✅ Simulação completa de execução

---

## 🎓 Conclusão

A **Etapa 7 - Ambientes de Execução** foi implementada com sucesso! O sistema completo:

1. **Compila** código fonte em TAC
2. **Gerencia** escopos e símbolos
3. **Simula** execução com pilha de ativação realista
4. **Demonstra** criação/destruição de activation records

O compilador está pronto para demonstração e pode ser estendido com:
- Estruturas de controle (if/while)
- Tipos de dados adicionais
- Arrays e ponteiros
- Otimizações de código

---

**Data:** 07 de Novembro de 2025  
**Disciplina:** Compiladores  
**Instituição:** [Sua Instituição]
