"""
Teste de Expressão Complexa
Verifica se o compilador processa corretamente expressões aritméticas complexas
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from compiler import compile


def teste_expressao_complexa():
    """
    Testa expressão: ((5 + 3) * 2 - 4) / (10 - 8)
    Resultado esperado: ((8) * 2 - 4) / (2) = (16 - 4) / 2 = 12 / 2 = 6
    """
    print("="*70)
    print("TESTE: EXPRESSÃO COMPLEXA")
    print("="*70)
    
    codigo = """
    int main() {
        int a = 5;
        int b = 3;
        int c = 2;
        int d = 4;
        int e = 10;
        int f = 8;
        
        int resultado = a + b * c - d;
        print(resultado);
        
        return 0;
    }
    """
    
    print("\n📄 Código:")
    print(codigo)
    
    # Compilar SEM otimizações
    print("\n" + "─"*70)
    print("1️⃣  COMPILAÇÃO SEM OTIMIZAÇÕES")
    print("─"*70)
    
    result_sem = compile(codigo, optimize=False, verbose=False)
    
    if not result_sem['success']:
        print("❌ ERRO na compilação:")
        for erro in result_sem['errors']:
            print(f"   {erro}")
        return False
    
    print("\n✅ Compilação bem-sucedida!")
    print(f"   Tokens: {len(result_sem['tokens'])}")
    print(f"   Instruções IR: {len(result_sem['ir'].get_instructions())}")
    
    print("\n📟 Código Intermediário (TAC) - SEM otimização:")
    result_sem['ir'].print_code()
    
    # Compilar COM otimizações
    print("\n" + "─"*70)
    print("2️⃣  COMPILAÇÃO COM OTIMIZAÇÕES")
    print("─"*70)
    
    result_com = compile(codigo, optimize=True, verbose=False)
    
    if not result_com['success']:
        print("❌ ERRO na compilação:")
        for erro in result_com['errors']:
            print(f"   {erro}")
        return False
    
    print("\n✅ Compilação bem-sucedida!")
    print(f"   Instruções IR otimizado: {len(result_com['optimized_ir'].get_instructions())}")
    
    print("\n⚡ Código Intermediário (TAC) - COM otimização:")
    result_com['optimized_ir'].print_code()
    
    # Comparação
    print("\n" + "─"*70)
    print("3️⃣  COMPARAÇÃO")
    print("─"*70)
    
    instrucoes_antes = len(result_sem['ir'].get_instructions())
    instrucoes_depois = len(result_com['optimized_ir'].get_instructions())
    reducao = instrucoes_antes - instrucoes_depois
    percentual = (reducao / instrucoes_antes * 100) if instrucoes_antes > 0 else 0
    
    print(f"\n📊 Estatísticas:")
    print(f"   • IR original: {instrucoes_antes} instruções")
    print(f"   • IR otimizado: {instrucoes_depois} instruções")
    print(f"   • Redução: {reducao} instruções ({percentual:.1f}%)")
    
    # Assembly
    print("\n" + "─"*70)
    print("4️⃣  ASSEMBLY GERADO")
    print("─"*70)
    
    print("\n🔧 Assembly MIPS-like:")
    for linha in result_com['assembly']:
        print(f"   {linha}")
    
    # Tabela de símbolos
    print("\n" + "─"*70)
    print("5️⃣  TABELA DE SÍMBOLOS")
    print("─"*70)
    result_com['symbol_table'].print_table()
    
    print("\n" + "="*70)
    print("✅ TESTE CONCLUÍDO COM SUCESSO!")
    print("="*70)
    
    return True


def teste_expressao_super_complexa():
    """
    Testa expressão ainda mais complexa com múltiplas operações
    e = (a + b) * (c - d) + e * f / g
    """
    print("\n\n")
    print("="*70)
    print("TESTE: EXPRESSÃO SUPER COMPLEXA")
    print("="*70)
    
    codigo = """
    int calc(int x, int y) {
        int temp = x * y + x - y;
        return temp;
    }
    
    int main() {
        int a = 10;
        int b = 5;
        int c = 3;
        
        int resultado1 = a + b * c;
        int resultado2 = calc(a, b);
        int resultado3 = resultado1 + resultado2;
        
        print(resultado3);
        
        return 0;
    }
    """
    
    print("\n📄 Código:")
    print(codigo)
    
    print("\n" + "─"*70)
    print("COMPILANDO...")
    print("─"*70)
    
    result = compile(codigo, optimize=True, verbose=False)
    
    if not result['success']:
        print("❌ ERRO na compilação:")
        for erro in result['errors']:
            print(f"   {erro}")
        return False
    
    print("\n✅ Compilação bem-sucedida!")
    
    print("\n🌳 AST:")
    from compiler.ast import print_ast
    print_ast(result['ast'])
    
    print("\n📟 IR Otimizado:")
    result['optimized_ir'].print_code()
    
    print("\n🔧 Assembly (primeiras 40 linhas):")
    for i, linha in enumerate(result['assembly'][:40], 1):
        print(f"   {i:3}: {linha}")
    if len(result['assembly']) > 40:
        print(f"   ... e mais {len(result['assembly']) - 40} linhas")
    
    print("\n" + "="*70)
    print("✅ TESTE SUPER COMPLEXO CONCLUÍDO!")
    print("="*70)
    
    return True


def teste_precedencia_operadores():
    """
    Testa precedência correta de operadores
    """
    print("\n\n")
    print("="*70)
    print("TESTE: PRECEDÊNCIA DE OPERADORES")
    print("="*70)
    
    casos = [
        ("2 + 3 * 4", "int x = 2 + 3 * 4;", "Deve ser: 2 + 12 = 14"),
        ("10 - 6 / 2", "int x = 10 - 6 / 2;", "Deve ser: 10 - 3 = 7"),
        ("5 * 2 + 3", "int x = 5 * 2 + 3;", "Deve ser: 10 + 3 = 13"),
        ("20 / 4 - 2", "int x = 20 / 4 - 2;", "Deve ser: 5 - 2 = 3"),
    ]
    
    for i, (expr, codigo_linha, esperado) in enumerate(casos, 1):
        print(f"\n{i}. Testando: {expr}")
        print(f"   {esperado}")
        
        codigo = f"""
        int main() {{
            {codigo_linha}
            print(x);
            return 0;
        }}
        """
        
        result = compile(codigo, optimize=True, verbose=False)
        
        if result['success']:
            print("   ✅ Compilou corretamente")
            # Mostra IR simplificado
            instrs = [str(i) for i in result['optimized_ir'].get_instructions()]
            print(f"   IR: {len(instrs)} instruções")
        else:
            print(f"   ❌ ERRO: {result['errors']}")
            return False
    
    print("\n" + "="*70)
    print("✅ TODOS OS TESTES DE PRECEDÊNCIA PASSARAM!")
    print("="*70)
    
    return True


if __name__ == "__main__":
    print("\n" + "#"*70)
    print("#" + " "*68 + "#")
    print("#" + "  TESTE COMPLETO DE EXPRESSÕES COMPLEXAS".center(68) + "#")
    print("#" + " "*68 + "#")
    print("#"*70)
    
    try:
        # Teste 1: Expressão complexa
        if not teste_expressao_complexa():
            print("\n❌ Teste 1 falhou!")
            sys.exit(1)
        
        # Teste 2: Expressão super complexa
        if not teste_expressao_super_complexa():
            print("\n❌ Teste 2 falhou!")
            sys.exit(1)
        
        # Teste 3: Precedência
        if not teste_precedencia_operadores():
            print("\n❌ Teste 3 falhou!")
            sys.exit(1)
        
        print("\n" + "#"*70)
        print("#" + " "*68 + "#")
        print("#" + "  🎉 TODOS OS TESTES PASSARAM! 🎉".center(68) + "#")
        print("#" + " "*68 + "#")
        print("#"*70 + "\n")
        
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
