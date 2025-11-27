# 📋 Gerador de Relatório Completo

Este script gera um **relatório completo e detalhado** de todas as 7 etapas do compilador, ideal para **documentação acadêmica** e **apresentações**.

## 🎯 O que o Relatório Mostra?

### ✅ Gramática BNF
- Gramática completa da linguagem
- Tipo de parser (LL(1) Top-Down)
- Características do Recursive Descent

### ✅ [1/7] Análise Léxica
- Expressões Regulares (ERs) usadas
- Palavras reservadas
- Tabela completa de tokens com tipo, valor e linha

### ✅ [2/7] Análise Sintática
- Método LL(1) Top-Down explicado
- Parse Tree hierárquica completa
- Lookahead de 1 token

### ✅ [3/7] Árvore Sintática Abstrata (AST)
- Diferença entre Parse Tree e AST
- Classes de nós da AST
- Estrutura hierárquica da AST

### ✅ [4/7] Análise Semântica
- Verificações realizadas
- Tabela de símbolos com escopos
- Validação de tipos e declarações

### ✅ [5/7] Código Intermediário (IR)
- TAC (Three-Address Code)
- Quádruplas (formato alternativo)
- Tipos de instruções
- Variáveis temporárias

### ✅ [6/7] Otimizações
- CSE (Common Subexpression Elimination)
- Constant Folding
- Algebraic Simplification
- Peephole Optimization
- Copy Propagation
- Dead Code Elimination
- Comparação antes/depois

### ✅ [7/7] Código Assembly
- Arquitetura MIPS-like
- Registradores usados
- Instruções assembly
- Código final completo

## 🚀 Como Usar

### Opção 1: Executar Exemplo Padrão

```bash
python demos/gerar_relatorio.py
```

Isso compila o código de exemplo já incluído no script.

### Opção 2: Personalizar o Código

Edite o arquivo `gerar_relatorio.py` e modifique a variável `codigo`:

```python
codigo = """
int main() {
    int x = 10;
    int y = 20;
    int z = x + y * 2;
    return z;
}
"""
```

### Opção 3: Salvar Relatório em Arquivo

```bash
python demos/gerar_relatorio.py > relatorio.txt
```

Ou:

```bash
python demos/gerar_relatorio.py > relatorio_compilador.md
```

## 📊 Exemplo de Saída

```
🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓
    RELATÓRIO COMPLETO DO COMPILADOR
🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓

CÓDIGO FONTE A SER COMPILADO:
=====================================
int main() {
    int a = 5;
    int b = 3;
    int x = a + b;
    return 0;
}
=====================================

[Gramática BNF completa...]
[Tokens detalhados...]
[Parse Tree hierárquica...]
[AST estruturada...]
[Análise semântica...]
[IR com TAC e Quádruplas...]
[Otimizações aplicadas...]
[Assembly final...]

📊 Estatísticas:
   • Tokens gerados:           28
   • Instruções IR originais:  7
   • Instruções IR otimizadas: 7
   • Linhas de assembly:       15
```

## 💡 Dicas para Relatório Acadêmico

### 1. Salvar em Arquivo
```bash
python demos/gerar_relatorio.py > meu_relatorio.txt
```

### 2. Testar com Diferentes Códigos
Modifique a variável `codigo` para testar:
- Expressões simples
- Funções com parâmetros
- Chamadas de função
- Otimizações (CSE com expressões duplicadas)

### 3. Exemplos para Demonstrar Otimizações

**CSE (Common Subexpression Elimination):**
```python
codigo = """
int main() {
    int a = 5;
    int b = 3;
    int x = a + b;
    int y = a + b;  // <- Duplicada!
    return 0;
}
"""
```

**Constant Folding:**
```python
codigo = """
int main() {
    int x = 5 + 3;  // <- Avaliado em tempo de compilação
    return x;
}
"""
```

**Algebraic Simplification:**
```python
codigo = """
int main() {
    int x = 10;
    int y = x * 1;  // <- Simplifica para y = x
    int z = x + 0;  // <- Simplifica para z = x
    return z;
}
"""
```

## 📋 Checklist para Relatório

- [ ] Executar `gerar_relatorio.py`
- [ ] Salvar saída em arquivo `.txt` ou `.md`
- [ ] Verificar que todas as 7 etapas aparecem
- [ ] Confirmar que gramática BNF está completa
- [ ] Verificar tabela de tokens
- [ ] Confirmar Parse Tree hierárquica
- [ ] Validar AST estruturada
- [ ] Confirmar análise semântica
- [ ] Verificar TAC e Quádruplas
- [ ] Confirmar otimizações aplicadas
- [ ] Validar assembly final

## 🎓 Para Apresentação

O relatório mostra claramente:
1. ✅ **Metodologia**: LL(1) Top-Down com Recursive Descent
2. ✅ **Gramática formal**: BNF completa
3. ✅ **Todas as 7 etapas**: Léxico → Sintático → AST → Semântica → IR → Otimização → Assembly
4. ✅ **Detalhamento técnico**: ERs, lookahead, TAC, quádruplas
5. ✅ **Resultados**: Estatísticas e código final

---

**Relatório completo e profissional para documentação acadêmica! 📚✨**
