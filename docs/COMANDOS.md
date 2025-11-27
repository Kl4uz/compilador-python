# 🎯 Comandos Úteis - Compilador

Lista de comandos prontos para copiar e colar.

## 🚀 Instalação e Setup

```bash
# Clonar repositório
git clone https://github.com/Kl4uz/compilador-python.git
cd compilador-python

# Instalar dependências
pip install ply

# Ou instalar tudo (inclui dev)
pip install -r requirements.txt
```

## ✅ Verificação Rápida

```bash
# Testar tudo
python test_compiler.py

# Demo interativa
python demo_completo.py

# Compilar exemplo
python compiler/main.py tests/hello_world.txt --verbose
```

## 📝 Compilação

```bash
# Compilar arquivo (básico)
python compiler/main.py tests/hello_world.txt

# Compilar com detalhes
python compiler/main.py tests/code.txt --verbose

# Compilar e salvar assembly
python compiler/main.py tests/code.txt -o output.asm

# Compilar sem otimizações
python compiler/main.py tests/code.txt --no-optimize

# Compilar com otimizações e verbose
python compiler/main.py tests/code.txt --verbose
```

## 🧪 Testes Individuais de Módulos

```bash
# Testar lexer
python compiler/lexer.py

# Testar parser
python compiler/parser.py

# Testar AST
python compiler/ast.py

# Testar analyzer
python compiler/analyzer.py

# Testar IR generator
python compiler/ir_generator.py

# Testar optimizer
python compiler/optimizer.py

# Testar peephole
python compiler/peephole.py

# Testar assembly
python compiler/assembly.py

# Testar codegen
python compiler/codegen.py

# Testar main (pipeline completo)
python compiler/main.py
```

## 🔍 Debug e Inspeção

```bash
# Ver apenas tokens
python -c "from compiler.lexer import tokenize; tokens = tokenize('int x = 5;'); print([str(t) for t in tokens])"

# Ver apenas parse tree
python -c "from compiler.parser import parse_from_code; print(parse_from_code('int main(){return 0;}'))"

# Ver IR de um código
python -c "from compiler import compile; compile('int main(){int x=5; return 0;}', verbose=False)['ir'].print_code()"

# Ver erros semânticos
python -c "from compiler import compile; print(compile('int main(){x=5;return 0;}', verbose=False)['errors'])"

# Ver assembly
python -c "from compiler import compile; [print(l) for l in compile('int main(){return 0;}')['assembly']]"
```

## 📊 Comparações

```bash
# Comparar com e sem otimizações
python -c "
from compiler import compile
codigo = 'int main(){int x=5+3;int y=x*1;return 0;}'
sem = compile(codigo, optimize=False)
com = compile(codigo, optimize=True)
print(f'Sem: {len(sem[\"ir\"].get_instructions())} instruções')
print(f'Com: {len(com[\"optimized_ir\"].get_instructions())} instruções')
"
```

## 🎨 Exemplos de Código para Testar

```bash
# Hello World
echo "int main() { int x = 42; print(x); return 0; }" > test.txt
python compiler/main.py test.txt -v

# Com função
echo "int soma(int a, int b) { return a + b; } int main() { int x = soma(5,3); print(x); return 0; }" > test.txt
python compiler/main.py test.txt -v

# Com otimizações
echo "int main() { int x = 5 + 3; int y = x * 1; int z = y + 0; print(z); return 0; }" > test.txt
python compiler/main.py test.txt -v

# Limpar
rm test.txt
```

## 📚 Visualização de Documentação

```bash
# Ver README do compiler
cat compiler/README.md

# Ver guia rápido
cat GUIA_RAPIDO.md

# Ver status
cat STATUS.md

# Ver migração
cat MIGRACAO.md

# Ver resumo
cat RESUMO_REESTRUTURACAO.md
```

## 🔧 Limpeza

```bash
# Remover cache Python
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete

# Remover arquivos gerados PLY
rm -f compiler/parsetab.py compiler/parser.out
rm -f src/parsetab.py src/parser.out

# Remover outputs de teste
rm -f test.txt output.asm *.tac
```

## 🎯 Para Apresentação

```bash
# 1. Verificar que tudo funciona
python test_compiler.py && echo "✅ Testes OK"

# 2. Preparar demo
python demo_completo.py

# 3. Compilar exemplo ao vivo
python compiler/main.py tests/hello_world.txt --verbose

# 4. Mostrar erros sendo detectados
python -c "from compiler import compile; r=compile('int main(){x=5;return 0;}'); print('Erro:', r['errors'][0])"

# 5. Mostrar otimizações
python -c "
from compiler import compile
codigo = 'int main(){int x=5+3;return x;}'
print('=== SEM OTIMIZAÇÃO ===')
compile(codigo, optimize=False)['ir'].print_code()
print('\\n=== COM OTIMIZAÇÃO ===')
compile(codigo, optimize=True)['optimized_ir'].print_code()
"
```

## 💻 API Python - Snippets Prontos

```python
# Snippet 1: Compilação básica
from compiler import compile
result = compile("int main() { return 0; }")
print("Sucesso!" if result['success'] else "Erro!")

# Snippet 2: Compilação com análise
from compiler import compile
codigo = """
int main() {
    int x = 10;
    print(x);
    return 0;
}
"""
result = compile(codigo, optimize=True, verbose=True)

# Snippet 3: Detecção de erros
from compiler import compile
codigo_errado = "int main() { x = 5; return 0; }"
result = compile(codigo_errado)
if not result['success']:
    print("Erros:", result['errors'])

# Snippet 4: Análise de tabela de símbolos
from compiler import compile
codigo = "int soma(int a, int b) { return a+b; } int main() { return 0; }"
result = compile(codigo)
result['symbol_table'].print_table()

# Snippet 5: Comparar otimizações
from compiler import compile
codigo = "int main(){int x=5+3;int y=x*1;return y;}"
sem = compile(codigo, optimize=False)
com = compile(codigo, optimize=True)
print(f"Redução: {len(sem['ir'].get_instructions()) - len(com['optimized_ir'].get_instructions())} instruções")
```

## 🎓 Para Estudar

```bash
# Estudar cada fase em ordem
python compiler/lexer.py          # Fase 1
python compiler/parser.py         # Fase 2
python compiler/ast.py            # Fase 3
python compiler/analyzer.py       # Fase 4
python compiler/ir_generator.py   # Fase 5
python compiler/optimizer.py      # Fase 6
python compiler/assembly.py       # Fase 7

# Ler documentação em ordem
cat compiler/README.md            # Arquitetura
cat GUIA_RAPIDO.md                # Referência
cat docs/GUIA_DE_ESTUDOS.md      # Estudo profundo
```

## 🐛 Troubleshooting

```bash
# Problema: Import error
cd compilador-python  # Certifique-se de estar na raiz
python -c "from compiler import compile; print('OK')"

# Problema: PLY not found
pip install ply

# Problema: Conflitos parsetab.py
rm compiler/parsetab.py src/parsetab.py
python compiler/main.py tests/hello_world.txt

# Problema: Python version
python --version  # Deve ser 3.8+

# Problema: Cache corrompido
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
python test_compiler.py
```

## 📦 Git (se necessário)

```bash
# Commit das mudanças
git add compiler/ test_compiler.py demo_completo.py *.md
git commit -m "feat: reestruturação completa - arquitetura modular"

# Push
git push origin main

# Ver status
git status

# Ver diff
git diff
```

## 🎯 Checklist Pré-Entrega

```bash
# Execute todos estes comandos. Se TODOS passarem, está pronto!

echo "1. Testando suite de testes..."
python test_compiler.py

echo "2. Testando hello world..."
python compiler/main.py tests/hello_world.txt

echo "3. Testando código complexo..."
python compiler/main.py tests/test_functions.txt

echo "4. Testando API Python..."
python -c "from compiler import compile; assert compile('int main(){return 0;}')['success']"

echo "5. Verificando estrutura..."
ls compiler/*.py | wc -l  # Deve ser 13

echo "✅ TUDO OK!" || echo "❌ Algum teste falhou"
```

## 📱 Atalhos PowerShell (Windows)

```powershell
# Testar
python test_compiler.py

# Demo
python demo_completo.py

# Compilar
python compiler\main.py tests\hello_world.txt

# Ver módulos
Get-ChildItem compiler\*.py

# Limpar cache
Get-ChildItem -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force

# Testar todos os módulos
Get-ChildItem compiler\*.py | ForEach-Object { python $_.FullName }
```

---

**Dica**: Salve os comandos que usar mais frequentemente!
