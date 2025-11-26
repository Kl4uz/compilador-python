"""
Testes do Pipeline de Compilação
Testa cada fase isoladamente e o pipeline completo
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.compiler import Compiler
from src.lexer import tokenize
from src.parser import parse
from src.semantic import SemanticAnalyzer
from src.ir_generator import IRGenerator
from src.optimizer import Optimizer
from src.symbol_table import SymbolTable
from src.ast_builder import tuple_to_ast


def test_lexer():
    """Testa a fase de análise léxica"""
    print("=" * 60)
    print("TESTE 1: Análise Léxica")
    print("=" * 60)
    
    code = "int x = 5 + 3;"
    tokens = tokenize(code)
    
    print(f"Código: {code}")
    print(f"Tokens gerados: {len(tokens)}")
    for token in tokens:
        print(f"  {token.type}: {token.value}")
    print()


def test_parser():
    """Testa a fase de análise sintática"""
    print("=" * 60)
    print("TESTE 2: Análise Sintática")
    print("=" * 60)
    
    code = """
    int x = 5 + 3;
    print(x);
    """
    
    ast = parse(code)
    print(f"Código:\n{code}")
    print(f"AST gerada: {ast}")
    print()


def test_semantic():
    """Testa a fase de análise semântica"""
    print("=" * 60)
    print("TESTE 3: Análise Semântica")
    print("=" * 60)
    
    code = """
    int soma(int a, int b) {
        int r = 0;
        int r = a + b;
        return r;
    }
    
    int main() {
        int x = 0;
        int x = soma(2, 3);
        return 0;
    }
    """
    
    ast_tuple = parse(code)
    ast = tuple_to_ast(ast_tuple)
    
    symbol_table = SymbolTable()
    analyzer = SemanticAnalyzer(symbol_table)
    success = analyzer.analyze(ast)
    
    print(f"Código:\n{code}")
    print(f"Análise semântica: {'✓ Sucesso' if success else '✗ Erros encontrados'}")
    if analyzer.errors:
        print("Erros:")
        for error in analyzer.errors:
            print(f"  - {error}")
    if analyzer.warnings:
        print("Avisos:")
        for warning in analyzer.warnings:
            print(f"  - {warning}")
    print()


def test_ir_generation():
    """Testa a geração de código intermediário"""
    print("=" * 60)
    print("TESTE 4: Geração de Código Intermediário")
    print("=" * 60)
    
    code = """
    int soma(int a, int b) {
        int r = 0;
        int r = a + b;
        return r;
    }
    
    int main() {
        int x = 0;
        int x = soma(2, 3);
        print(x);
        return 0;
    }
    """
    
    ast_tuple = parse(code)
    ast = tuple_to_ast(ast_tuple)
    
    symbol_table = SymbolTable()
    generator = IRGenerator(symbol_table)
    ir = generator.generate(ast)
    
    print(f"Código:\n{code}")
    print("Código IR gerado:")
    generator.instructions = ir
    generator.print_ir()
    print()


def test_optimizer():
    """Testa o otimizador"""
    print("=" * 60)
    print("TESTE 5: Otimização")
    print("=" * 60)
    
    code = """
    int main() {
        int x = 5 + 3;
        int y = x * 2;
        print(y);
        return 0;
    }
    """
    
    ast_tuple = parse(code)
    ast = tuple_to_ast(ast_tuple)
    
    symbol_table = SymbolTable()
    generator = IRGenerator(symbol_table)
    ir = generator.generate(ast)
    
    optimizer = Optimizer()
    optimized_ir = optimizer.optimize(ir)
    
    print(f"Código:\n{code}")
    print("Código IR original:")
    generator.instructions = ir
    generator.print_ir()
    
    print("Código IR otimizado:")
    generator.instructions = optimized_ir
    generator.print_ir()
    
    print(optimizer.get_optimization_report())
    print()


def test_full_pipeline():
    """Testa o pipeline completo"""
    print("=" * 60)
    print("TESTE 6: Pipeline Completo")
    print("=" * 60)
    
    code = """
    int soma(int a, int b) {
        int r = a + b;
        return r;
    }
    
    int main() {
        int x = soma(2, 3);
        print(x);
        return 0;
    }
    """
    
    compiler = Compiler(optimize=True, generate_assembly=False)
    result = compiler.compile(code)
    
    print(f"Código:\n{code}")
    compiler.print_results(result)
    print()


def test_error_cases():
    """Testa casos de erro"""
    print("=" * 60)
    print("TESTE 7: Casos de Erro")
    print("=" * 60)
    
    # Erro sintático
    print("\n7.1 - Erro Sintático:")
    code1 = "int x = 5 + ;"  # Expressão incompleta
    compiler = Compiler()
    result1 = compiler.compile(code1)
    print(f"Código: {code1}")
    print(f"Sucesso: {result1['success']}")
    if result1['errors']:
        print("Erros encontrados:")
        for error in result1['errors']:
            print(f"  - {error}")
    
    # Erro semântico - variável não declarada
    print("\n7.2 - Variável Não Declarada:")
    code2 = """
    int main() {
        int x = y + 5;  // y não declarada
        return 0;
    }
    """
    compiler = Compiler()
    result2 = compiler.compile(code2)
    print(f"Código:\n{code2}")
    print(f"Sucesso: {result2['success']}")
    if result2['errors']:
        print("Erros encontrados:")
        for error in result2['errors']:
            print(f"  - {error}")
    
    # Divisão por zero
    print("\n7.3 - Divisão por Zero:")
    code3 = """
    int main() {
        int x = 10 / 0;
        return 0;
    }
    """
    compiler = Compiler()
    result3 = compiler.compile(code3)
    print(f"Código:\n{code3}")
    print(f"Sucesso: {result3['success']}")
    if result3['errors']:
        print("Erros encontrados:")
        for error in result3['errors']:
            print(f"  - {error}")
    print()


def main():
    """Executa todos os testes"""
    print("\n" + "=" * 60)
    print("SUITE DE TESTES DO PIPELINE DE COMPILAÇÃO")
    print("=" * 60 + "\n")
    
    try:
        test_lexer()
        test_parser()
        test_semantic()
        test_ir_generation()
        test_optimizer()
        test_full_pipeline()
        test_error_cases()
        
        print("=" * 60)
        print("✓ TODOS OS TESTES CONCLUÍDOS")
        print("=" * 60)
    
    except Exception as e:
        print(f"\n✗ ERRO NOS TESTES: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

