"""
Script de Teste Completo do Compilador
Testa todos os módulos e o pipeline integrado
"""

import sys
import os

# Adiciona o diretório pai ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from compiler.main import compile


def test_hello_world():
    """Teste 1: Hello World simples"""
    print("\n" + "="*60)
    print("TESTE 1: Hello World")
    print("="*60)
    
    code = """
    int main() {
        int x = 42;
        print(x);
        return 0;
    }
    """
    
    result = compile(code, optimize=True, verbose=False)
    
    assert result['success'], f"Compilação falhou: {result['errors']}"
    assert len(result['tokens']) > 0, "Nenhum token gerado"
    assert result['parse_tree'] is not None, "Parse tree não gerada"
    assert result['ast'] is not None, "AST não construída"
    assert result['ir'] is not None, "IR não gerado"
    assert len(result['assembly']) > 0, "Assembly não gerado"
    
    print("✓ Teste Hello World passou!")
    return True


def test_function_call():
    """Teste 2: Chamada de função"""
    print("\n" + "="*60)
    print("TESTE 2: Chamada de Função")
    print("="*60)
    
    code = """
    int soma(int a, int b) {
        int r = a + b;
        return r;
    }
    
    int main() {
        int x = 5;
        int y = soma(x, 3);
        print(y);
        return 0;
    }
    """
    
    result = compile(code, optimize=True, verbose=False)
    
    assert result['success'], f"Compilação falhou: {result['errors']}"
    
    # Verifica que tem 2 funções
    ast = result['ast']
    assert len(ast.declarations) == 2, "Deveria ter 2 funções"
    
    print("✓ Teste Chamada de Função passou!")
    return True


def test_expressions():
    """Teste 3: Expressões aritméticas"""
    print("\n" + "="*60)
    print("TESTE 3: Expressões Aritméticas")
    print("="*60)
    
    code = """
    int main() {
        int a = 10;
        int b = 5;
        int c = a + b * 2;
        int d = c - a / 2;
        print(d);
        return 0;
    }
    """
    
    result = compile(code, optimize=True, verbose=False)
    
    assert result['success'], f"Compilação falhou: {result['errors']}"
    
    print("✓ Teste Expressões Aritméticas passou!")
    return True


def test_optimizations():
    """Teste 4: Verificação de otimizações"""
    print("\n" + "="*60)
    print("TESTE 4: Otimizações")
    print("="*60)
    
    code = """
    int main() {
        int x = 5 + 3;
        int y = x * 1;
        int z = y + 0;
        print(z);
        return 0;
    }
    """
    
    # Sem otimizações
    result_no_opt = compile(code, optimize=False, verbose=False)
    assert result_no_opt['success']
    
    # Com otimizações
    result_opt = compile(code, optimize=True, verbose=False)
    assert result_opt['success']
    
    # Verifica que código otimizado é menor ou igual
    ir_original = len(result_no_opt['ir'].get_instructions())
    ir_optimized = len(result_opt['optimized_ir'].get_instructions())
    
    print(f"  IR original: {ir_original} instruções")
    print(f"  IR otimizado: {ir_optimized} instruções")
    print(f"  Redução: {ir_original - ir_optimized} instruções")
    
    assert ir_optimized <= ir_original, "Otimização não reduziu código"
    
    print("✓ Teste Otimizações passou!")
    return True


def test_semantic_errors():
    """Teste 5: Detecção de erros semânticos"""
    print("\n" + "="*60)
    print("TESTE 5: Erros Semânticos")
    print("="*60)
    
    # Erro: variável não declarada
    code1 = """
    int main() {
        x = 5;
        return 0;
    }
    """
    
    result1 = compile(code1, verbose=False)
    assert not result1['success'], "Deveria detectar variável não declarada"
    assert len(result1['errors']) > 0, "Deveria ter erros"
    print(f"  ✓ Detectou: {result1['errors'][0]}")
    
    # Erro: função não declarada
    code2 = """
    int main() {
        int x = foo(5);
        return 0;
    }
    """
    
    result2 = compile(code2, verbose=False)
    assert not result2['success'], "Deveria detectar função não declarada"
    assert len(result2['errors']) > 0, "Deveria ter erros"
    print(f"  ✓ Detectou: {result2['errors'][0]}")
    
    # Erro: número errado de argumentos
    code3 = """
    int soma(int a, int b) {
        return a + b;
    }
    
    int main() {
        int x = soma(5);
        return 0;
    }
    """
    
    result3 = compile(code3, verbose=False)
    assert not result3['success'], "Deveria detectar número errado de argumentos"
    assert len(result3['errors']) > 0, "Deveria ter erros"
    print(f"  ✓ Detectou: {result3['errors'][0]}")
    
    print("✓ Teste Erros Semânticos passou!")
    return True


def test_nested_calls():
    """Teste 6: Chamadas de função aninhadas"""
    print("\n" + "="*60)
    print("TESTE 6: Chamadas Aninhadas")
    print("="*60)
    
    code = """
    int dobro(int x) {
        return x + x;
    }
    
    int quadruplo(int x) {
        int d = dobro(x);
        return dobro(d);
    }
    
    int main() {
        int resultado = quadruplo(5);
        print(resultado);
        return 0;
    }
    """
    
    result = compile(code, optimize=True, verbose=False)
    
    assert result['success'], f"Compilação falhou: {result['errors']}"
    
    # Verifica que tem 3 funções
    ast = result['ast']
    assert len(ast.declarations) == 3, "Deveria ter 3 funções"
    
    print("✓ Teste Chamadas Aninhadas passou!")
    return True


def run_all_tests():
    """Executa todos os testes"""
    print("\n" + "#"*60)
    print("# SUITE COMPLETA DE TESTES DO COMPILADOR")
    print("#"*60)
    
    tests = [
        test_hello_world,
        test_function_call,
        test_expressions,
        test_optimizations,
        test_semantic_errors,
        test_nested_calls
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except AssertionError as e:
            print(f"✗ FALHOU: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ ERRO: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "="*60)
    print(f"RESULTADO FINAL: {passed}/{len(tests)} testes passaram")
    if failed == 0:
        print("✓ TODOS OS TESTES PASSARAM!")
    else:
        print(f"✗ {failed} testes falharam")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
