# 🔧 Mini-Compilador em Python

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow.svg)

**Um compilador completo implementado em Python**

[Características](#-características) •
[Instalação](#-instalação) •
[Uso](#-uso) •
[Arquitetura](#-arquitetura) •
[Exemplos](#-exemplos) •
[Equipe](#-equipe)

</div>

---

## 👥 Desenvolvedores
[Lucas Farias]([githu.com/Kl4uz](https://github.com/Kl4uz))
[José Lucas]([https://github.com/lalisalix](https://github.com/lalisalix))
[Ester Arraiz]([https://github.com/esterarraiz](https://github.com/esterarraiz))
[Henrique Noronha]([https://github.com/henrique-noronha](https://github.com/henrique-noronha))
[Laura Barbosa]([https://github.com/tinywin](https://github.com/tinywin))

---
## 📚 Sobre o Projeto

Este é um **mini-compilador acadêmico** desenvolvido para a disciplina de Compiladores. O projeto implementa todas as fases clássicas de um compilador, desde a análise léxica até a geração de código assembly, seguindo a arquitetura pipeline moderna.

### 🎯 Objetivos

- ✅ Implementar um **analisador léxico** (tokenização)
- ✅ Construir um **analisador sintático** (parser)
- ✅ Gerar uma **Árvore Sintática Abstrata** (AST)
- ✅ Realizar **análise semântica** (tipos e escopos)
- ✅ Gerar **código intermediário** (TAC - Three-Address Code)
- ✅ Aplicar **otimizações** (constant folding, dead code elimination)
- ✅ Gerar **código assembly** final
- ✅ Simular **ambientes de execução** (runtime stack)

---

## 🌟 Características

### ✨ Funcionalidades Principais

| Recurso | Status | Descrição |
|---------|--------|-----------|
| **Análise Léxica** | ✅ | Tokenização com suporte a funções, operadores e palavras-chave |
| **Análise Sintática** | ✅ | Parser completo com detecção de erros |
| **AST** | ✅ | Construção de árvore sintática abstrata |
| **Análise Semântica** | ✅ | Verificação de tipos e escopos |
| **Tabela de Símbolos** | ✅ | Gerenciamento de escopos aninhados |
| **Código Intermediário** | ✅ | Geração de TAC (Three-Address Code) |
| **Otimização** | ✅ | Constant folding, dead code elimination, peephole |
| **Geração de Assembly** | ✅ | Código assembly otimizado |
| **Runtime Stack** | ✅ | Simulação de pilha de ativação |
| **Funções** | ✅ | Suporte completo a funções com parâmetros |

### 📋 Linguagem Suportada

```c
// Exemplo de código suportado
int soma(int a, int b) {
    int resultado = a + b;
    return resultado;
}

int main() {
    int x = 10;
    int y = 20;
    int total = soma(x, y);
    print(total);
    
    if (total > 25) {
        print(1);
    } else {
        print(0);
    }
    
    return 0;
}
```

**Suporte a:**
- ✅ Tipos: `int`
- ✅ Variáveis locais e globais
- ✅ Funções com parâmetros e retorno
- ✅ Expressões aritméticas: `+`, `-`, `*`, `/`
- ✅ Operadores relacionais: `<`, `>`, `==`, `!=`, `<=`, `>=`
- ✅ Estruturas de controle: `if/else`, `while`
- ✅ Impressão: `print()`

---

## 🚀 Instalação

### Pré-requisitos

- **Python 3.8+**
- **pip** (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone o repositório**
```bash
git clone https://github.com/Kl4uz/compilador-python.git
cd compilador-python
```

2. **Crie um ambiente virtual** (recomendado)
```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Verifique a instalação**
```bash
python src/main.py --version
```

---

## 💻 Uso

### 🎯 Modos de Execução

O compilador oferece **3 modos** de uso diferentes:

#### 1️⃣ **Modo Expressão** (Compilar diretamente da linha de comando)

Compile código diretamente no terminal usando a flag `-e`:

```bash
python src/main.py -e "x = 5 + 3; print(x);"
```

**Exemplo com saída:**
```bash
$ python src/main.py -e "int x = 10 + 5;"

🔍 [1/7] Análise Léxica...
   ✓ 7 tokens gerados
🌳 [2/7] Análise Sintática...
   ✓ Árvore de parsing construída
🎯 [3/7] Construção da AST...
   ✓ AST gerada
🔬 [4/7] Análise Semântica...
   ✓ Análise semântica concluída
⚙️  [5/7] Geração de Código Intermediário...
   ✓ 2 instruções TAC geradas
⚡ [6/7] Otimização...
   ✓ Otimizado: 2 → 1 instruções
🎯 [7/7] Geração de Assembly...
   ✓ 3 instruções assembly geradas

✅ Compilação bem-sucedida!
```

#### 2️⃣ **Modo Arquivo** (Compilar de arquivo)

Compile um arquivo de código usando a flag `-f`:

```bash
python src/main.py -f examples/hello_world.txt
```

**Exemplo:**
```bash
$ python src/main.py -f examples/functions.txt

📄 Compilando arquivo: examples/functions.txt

🔍 [1/7] Análise Léxica...
   ✓ 45 tokens gerados
🌳 [2/7] Análise Sintática...
   ✓ Árvore de parsing construída
...
✅ Compilação bem-sucedida!
```

#### 3️⃣ **Modo Interativo** (REPL)

Execute sem argumentos para entrar no modo interativo:

```bash
python src/main.py
```

```
╔════════════════════════════════════════════╗
║     MINI-COMPILADOR PYTHON v1.0           ║
║     Modo Interativo (REPL)                ║
╚════════════════════════════════════════════╝

Digite seu código (ou 'exit' para sair):
>>> int x = 10;
✓ Compilado com sucesso!

>>> print(x);
✓ Compilado com sucesso!
>>> OUTPUT: 10

>>> exit
Até logo! 👋
```

---

## 🎛️ Flags e Opções

### Flags Principais

| Flag | Descrição | Exemplo |
|------|-----------|---------|
| `-e, --expr` | Compila expressão inline | `python src/main.py -e "x = 5;"` |
| `-f, --file` | Compila arquivo | `python src/main.py -f code.txt` |
| `-v, --verbose` | Modo verboso (detalhado) | `python src/main.py -f code.txt -v` |
| `-q, --quiet` | Modo silencioso | `python src/main.py -f code.txt -q` |
| `-o, --output` | Salva assembly em arquivo | `python src/main.py -f code.txt -o out.asm` |
| `--no-optimize` | Desativa otimizações | `python src/main.py -e "x=2*3;" --no-optimize` |
| `--show-tokens` | Mostra tokens gerados | `python src/main.py -e "x=5;" --show-tokens` |
| `--show-ast` | Mostra AST gerada | `python src/main.py -e "x=5;" --show-ast` |
| `--show-ir` | Mostra código intermediário | `python src/main.py -e "x=5;" --show-ir` |
| `--version` | Mostra versão | `python src/main.py --version` |
| `--help` | Mostra ajuda | `python src/main.py --help` |

### Exemplos de Uso Avançado

#### 📊 Modo Verbose (Detalhado)

Mostra todos os passos da compilação:

```bash
python src/main.py -f examples/hello_world.txt -v
```

**Saída:**
```
============================================================
📄 CÓDIGO FONTE
============================================================
int main() {
    int x = 10;
    print(x);
    return 0;
}

============================================================
🔍 FASE 1: ANÁLISE LÉXICA
============================================================
Token 1: INT (type: keyword)
Token 2: MAIN (type: identifier)
Token 3: LPAREN (type: delimiter)
...

============================================================
🌳 FASE 2: ÁRVORE SINTÁTICA
============================================================
program
├── function_def (main)
│   └── block
│       ├── declaration (x)
│       ├── print_stmt
│       └── return_stmt
...
```

#### 🤫 Modo Quiet (Silencioso)

Mostra apenas erros (útil para CI/CD):

```bash
python src/main.py -f examples/hello_world.txt -q
```

**Saída apenas se houver erro:**
```
❌ ERRO na linha 5: Variável 'y' não declarada
```

#### 💾 Salvar Assembly em Arquivo

```bash
python src/main.py -f examples/functions.txt -o output.asm
```

Gera arquivo `output.asm`:
```asm
; Código gerado pelo Mini-Compilador v1.0
; Data: 2025-11-28 14:30:00

LOAD R1, 10
STORE x, R1
LOAD R1, x
PRINT R1
HALT
```

#### 🔍 Visualizar Fases Intermediárias

Ver apenas os tokens:
```bash
python src/main.py -e "x = 5 + 3;" --show-tokens
```

Ver apenas a AST:
```bash
python src/main.py -e "x = 5 + 3;" --show-ast
```

Ver apenas o código intermediário (TAC):
```bash
python src/main.py -e "x = 5 + 3;" --show-ir
```

Ver tudo:
```bash
python src/main.py -e "x = 5 + 3;" --show-tokens --show-ast --show-ir -v
```

#### ⚙️ Comparar Com/Sem Otimização

Sem otimização:
```bash
python src/main.py -e "x = 2 * 3;" --no-optimize --show-ir
```
```
TAC Gerado:
t1 = 2 * 3
x = t1
```

Com otimização (padrão):
```bash
python src/main.py -e "x = 2 * 3;" --show-ir
```
```
TAC Otimizado:
x = 6
```

---

## 🏗️ Arquitetura

### Pipeline do Compilador

```
┌─────────────────┐
│  Código Fonte   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 1. Léxico       │ ─────► Tokens
│    (lexer.py)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 2. Sintático    │ ─────► Parse Tree
│    (parser.py)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 3. AST Builder  │ ─────► AST
│ (ast_builder.py)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 4. Semântico    │ ─────► AST Anotada
│  (semantic.py)  │        + Tabela Símbolos
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 5. Gerador IR   │ ─────► TAC
│(ir_generator.py)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 6. Otimizador   │ ─────► TAC Otimizado
│ (optimizer.py)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 7. Gerador Asm  │ ─────► Assembly
│  (codegen.py)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Assembly Final │
└─────────────────┘
```

### 📁 Estrutura de Diretórios

```
compilador-python/
├── README.md                    # Este arquivo
├── requirements.txt             # Dependências Python
├── .gitignore                  # Arquivos ignorados
│
├── src/                        # 📂 Código fonte
│   ├── __init__.py
│   ├── main.py                 # 🎯 Ponto de entrada (CLI)
│   ├── compiler.py             # 🔧 Pipeline principal
│   ├── lexer.py                # 📝 Analisador léxico
│   ├── parser.py               # 🌳 Analisador sintático
│   ├── ast_builder.py          # 🎯 Construtor de AST
│   ├── semantic.py             # 🔬 Análise semântica
│   ├── symbol_table.py         # 📊 Tabela de símbolos
│   ├── ir_generator.py         # ⚙️  Gerador de código intermediário
│   ├── optimizer.py            # ⚡ Otimizador
│   ├── codegen.py              # 🎯 Gerador de assembly
│   ├── runtime.py              # 🏃 Runtime stack simulation
│   └── interpreter.py          # 🎮 Interpretador TAC
│
├── tests/                      # 🧪 Testes
│   ├── test_lexer.py
│   ├── test_parser.py
│   ├── test_semantic.py
│   ├── test_ir.py
│   ├── test_optimizer.py
│   ├── test_codegen.py
│   └── test_pipeline.py        # Teste de integração
│
├── examples/                   # 📚 Exemplos de código
│   ├── hello_world.txt         # Exemplo básico
│   ├── functions.txt           # Funções
│   ├── control_flow.txt        # If/While
│   └── optimization.txt        # Demonstração de otimizações
│
└── docs/                       # 📖 Documentação
    ├── grammar.md              # Gramática da linguagem
    ├── pipeline.md             # Arquitetura do pipeline
    └── ETAPA7_AMBIENTES_EXECUCAO.md
```

---

## 📖 Exemplos

### Exemplo 1: Hello World

**Arquivo:** `examples/hello_world.txt`
```c
int main() {
    int x = 42;
    print(x);
    return 0;
}
```

**Execução:**
```bash
python src/main.py -f examples/hello_world.txt
```

**Assembly Gerado:**
```asm
LOAD R1, 42
STORE x, R1
LOAD R1, x
PRINT R1
HALT
```

### Exemplo 2: Função com Parâmetros

**Arquivo:** `examples/functions.txt`
```c
int soma(int a, int b) {
    return a + b;
}

int main() {
    int resultado = soma(10, 20);
    print(resultado);
    return 0;
}
```

**Execução:**
```bash
python src/main.py -f examples/functions.txt -v
```

**TAC Gerado:**
```
FUNCTION soma
PARAM a
PARAM b
t1 = a + b
RETURN t1
END_FUNCTION

FUNCTION main
t2 = CALL soma, 10, 20
resultado = t2
PRINT resultado
RETURN 0
END_FUNCTION
```

### Exemplo 3: Otimização (Constant Folding)

**Código:**
```c
int main() {
    int x = 2 * 3 + 5;
    print(x);
    return 0;
}
```

**Sem otimização:**
```bash
python src/main.py -f examples/optimization.txt --no-optimize --show-ir
```
```
TAC:
t1 = 2 * 3
t2 = t1 + 5
x = t2
PRINT x
```

**Com otimização (padrão):**
```bash
python src/main.py -f examples/optimization.txt --show-ir
```
```
TAC Otimizado:
x = 11
PRINT x
```

### Exemplo 4: Estruturas de Controle

**Arquivo:** `examples/control_flow.txt`
```c
int main() {
    int x = 10;
    
    if (x > 5) {
        print(1);
    } else {
        print(0);
    }
    
    int i = 0;
    while (i < 3) {
        print(i);
        i = i + 1;
    }
    
    return 0;
}
```

**Execução:**
```bash
python src/main.py -f examples/control_flow.txt
```

**Saída:**
```
>>> OUTPUT: 1
>>> OUTPUT: 0
>>> OUTPUT: 1
>>> OUTPUT: 2
```

---

## 🧪 Testes

### Executar Todos os Testes

```bash
pytest tests/ -v
```

### Executar Testes Específicos

```bash
# Testar apenas o lexer
pytest tests/test_lexer.py -v

# Testar apenas o pipeline completo
pytest tests/test_pipeline.py -v
```

### Cobertura de Testes

```bash
pytest tests/ --cov=src --cov-report=html
```

Abre o relatório: `open htmlcov/index.html`

---

## 🐛 Tratamento de Erros

O compilador detecta e reporta diversos tipos de erros:

### Erros Léxicos
```bash
$ python src/main.py -e "int x = @;"

❌ ERRO LÉXICO (linha 1, coluna 9):
   Caractere inválido: '@'
```

### Erros Sintáticos
```bash
$ python src/main.py -e "int x = 5"

❌ ERRO SINTÁTICO (linha 1):
   Esperado ';' após declaração
```

### Erros Semânticos
```bash
$ python src/main.py -e "x = y + 5;"

❌ ERRO SEMÂNTICO (linha 1):
   Variável 'y' não declarada
```

```bash
$ python src/main.py -e "int x = 5; x = 10 + 20 + 30;"

❌ ERRO SEMÂNTICO (linha 1):
   Variável 'x' já declarada neste escopo
```

---

## 🎓 Documentação Acadêmica

### Gramática da Linguagem

Veja a gramática completa em: [`docs/grammar.md`](docs/grammar.md)

**Resumo:**
```
<program>    ::= <stmt_list>
<stmt_list>  ::= <stmt> | <stmt> <stmt_list>
<stmt>       ::= <assign_stmt> | <if_stmt> | <while_stmt> | <print_stmt>
<expr>       ::= <term> (('+' | '-') <term>)*
<term>       ::= <factor> (('*' | '/') <factor>)*
<factor>     ::= <number> | <id> | '(' <expr> ')'
```

### Arquitetura do Pipeline

Documentação detalhada: [`docs/pipeline.md`](docs/pipeline.md)

### Ambientes de Execução (Etapa 7)

Detalhes sobre runtime stack: [`docs/ETAPA7_AMBIENTES_EXECUCAO.md`](docs/ETAPA7_AMBIENTES_EXECUCAO.md)

---

## 👥 Equipe

Este projeto foi desenvolvido por:

- **Lucas Farias** ([@Kl4uz](https://github.com/Kl4uz)) - Pipeline e Integração
- **Lalisa** - Front-end (Léxico, Sintático, AST)
- **Ester Araiz** - Análise Semântica e Tabela de Símbolos
- **Laura** - Código Intermediário e Otimizações
- **Henrique Noronha** - Geração de Assembly e Runtime

### Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 🔗 Links Úteis

- 📚 [Documentação Completa](docs/)
- 🐛 [Reportar Bug](https://github.com/Kl4uz/compilador-python/issues)
- 💡 [Sugerir Feature](https://github.com/Kl4uz/compilador-python/issues/new)
- 📖 [Wiki do Projeto](https://github.com/Kl4uz/compilador-python/wiki)

---

## 📚 Referências

- **Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D.** (2006). *Compilers: Principles, Techniques, and Tools* (2nd ed.). Pearson.
- **Cooper, K. D., & Torczon, L.** (2011). *Engineering a Compiler* (2nd ed.). Morgan Kaufmann.
- **Appel, A. W.** (2004). *Modern Compiler Implementation in Java* (2nd ed.). Cambridge University Press.

---

<div align="center">

**⭐ Se este projeto foi útil, considere dar uma estrela no repositório! ⭐**

Desenvolvido com ❤️ para a disciplina de Compiladores

[⬆ Voltar ao topo](#-mini-compilador-em-python)

</div>