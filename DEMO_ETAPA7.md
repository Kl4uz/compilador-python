## 🚀 Execução Rápida

```bash
cd src
python compiler_etapa7.py
```

## 📊 Output Esperado

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
```

## ✅ Checklist de Verificação

- [x] Lexer reconhece tokens de funções (INT, RETURN, LBRACE, RBRACE)
- [x] Parser gera AST correta para declaração de funções
- [x] Parser gera AST correta para chamada de funções
- [x] Tabela de símbolos gerencia escopos (global, local)
- [x] Activation Record contém todos os campos necessários
- [x] Runtime Stack empilha/desempilha ARs corretamente
- [x] Gerador TAC produz código para funções
- [x] Interpretador executa TAC com runtime stack
- [x] Parâmetros são passados corretamente
- [x] Variáveis locais funcionam
- [x] Valor de retorno é propagado
- [x] Chamadas aninhadas funcionam
- [x] Documentação completa criada

## 🎯 Arquivos Principais

### Implementação:
- `src/symbol_table.py` - Tabela de símbolos
- `src/runtime.py` - AR + Runtime Stack
- `src/compiler_etapa7.py` - Sistema completo
- `src/interpreter.py` - Interpretador TAC

### Documentação:
- `docs/ETAPA7_AMBIENTES_EXECUCAO.md` - Documentação detalhada
- `docs/RESUMO_ETAPA7.md` - Resumo executivo

### Testes:
- `tests/test_functions.txt` - Teste básico
- `tests/test_nested_calls.txt` - Chamadas aninhadas
- `src/test_nested.py` - Script de teste

## 🧪 Outros Testes

### Teste Individual da Tabela de Símbolos:
```bash
python src/symbol_table.py
```

### Teste Individual do Runtime:
```bash
python src/runtime.py
```

### Teste de Chamadas Aninhadas:
```bash
python src/test_nested.py
```

## 📈 Estatísticas

- **Arquivos Criados:** 8 novos arquivos
- **Linhas de Código:** ~1000+ linhas
- **Classes Implementadas:** 6 classes principais
- **Testes Funcionais:** 3 cenários completos
- **Profundidade Máxima da Pilha Testada:** 3 níveis

## 🏆 Resultado

✅ **ETAPA 7 - AMBIENTES DE EXECUÇÃO: IMPLEMENTADA COM SUCESSO!**

Todos os requisitos foram atendidos:
- ✅ Atividade 1: Modelagem do ambiente
- ✅ Atividade 2: Activation Records
- ✅ Atividade 3: Integração com tabela de símbolos

O sistema está **COMPLETO** e **FUNCIONAL**! 🎉
