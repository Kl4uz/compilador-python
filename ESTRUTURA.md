# 📁 Estrutura de Pastas - Guia Rápido

## ✅ Estrutura Atual (ORGANIZADA)

```
compilador-python/
│
├── 🎯 compiler/              ← CÓDIGO PRINCIPAL (estrutura modular)
│   ├── lexer.py                 Análise Léxica
│   ├── parser.py                ✅ Parser LL(1) Top-Down
│   ├── main.py                  Pipeline integrado
│   │
│   ├── ast/                     Árvore Sintática Abstrata
│   │   ├── ast_builder.py
│   │   ├── analyzer.py          Análise semântica
│   │   └── symbol_table.py
│   │
│   ├── ir/                      Código Intermediário
│   │   ├── ir.py                ✅ TAC + Quádruplas
│   │   └── ir_generator.py
│   │
│   ├── optimizer/               Otimizações
│   │   ├── optimizer.py         ✅ CSE, CF, DCE, CP
│   │   └── peephole.py
│   │
│   └── codegen/                 Geração de Assembly
│       ├── codegen.py
│       └── assembly.py
│
├── 🚀 run.py             ← INTERFACE PRINCIPAL (use este!)
│   │                        3 modos: -e expressão, -f arquivo, interativo
│
├── 📝 tests/             ← ARQUIVOS DE TESTE (.txt)
│   ├── simples.txt          int x = a + b * 2;
│   ├── teste_cse.txt        Teste de CSE
│   └── exemplo_professor.txt
│
├── 🎮 demos/             ← DEMOS E TESTES AUTOMATIZADOS
│   ├── demo_completo.py     Demo interativa
│   ├── test_compiler.py     Testes unitários
│   └── teste_expressoes.py  Testes de expressões
│
├── 📚 docs_projeto/      ← DOCUMENTAÇÃO COMPLETA
│   ├── GUIA_RAPIDO.md       Como usar
│   ├── COMANDOS.md          Lista de comandos
│   └── README_OLD.md        Doc anterior
│
└── 📦 old/               ← CÓDIGO ANTIGO (não use!)
    └── (implementação anterior com PLY/Yacc LALR)
```

## 🎯 O Que Usar?

### Para compilar código:
```bash
python run.py -f tests/simples.txt
```

### Para testar:
```bash
python run.py -e "5 + 3 * 2"
python demos/teste_expressoes.py
```

### Para entender o código:
- Comece por `compiler/main.py` - pipeline completo
- Veja `compiler/parser_ll1.py` - parser LL(1)
- Veja `compiler/optimizer.py` - otimizações (CSE, etc)

## 🗑️ O Que NÃO Usar?

- ❌ `old/` - código antigo, apenas referência
- ❌ `compiler/parser.py` - removido (era LALR, não LL(1))

## 📝 Resumo

| Pasta | Use? | Motivo |
|-------|------|--------|
| `compiler/` | ✅ SIM | Código principal do compilador |
| `run.py` | ✅ SIM | Interface para usar |
| `tests/` | ✅ SIM | Seus arquivos de teste |
| `demos/` | ✅ SIM | Demos e testes prontos |
| `docs_projeto/` | ✅ SIM | Documentação |
| `old/` | ⚠️ NÃO | Apenas referência |

## 🚀 Comandos Mais Usados

```bash
# Compilar arquivo
python run.py -f tests/simples.txt

# Compilar expressão
python run.py -e "int x = 5 + 3;"

# Modo verbose (ver tudo)
python run.py -f tests/exemplo_professor.txt

# Modo interativo
python run.py
```

---

**Estrutura organizada e pronta para uso! 🎉**
