"""
Demonstração Completa do Compilador
Mostra todas as fases do pipeline com exemplos práticos
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from compiler import compile


def demo_basico():
    """Demonstração 1: Hello World básico"""
    print("\n" + "="*70)
    print(" DEMO 1: HELLO WORLD BÁSICO")
    print("="*70)
    
    codigo = """
    int main() {
        int mensagem = 42;
        print(mensagem);
        return 0;
    }
    """
    
    print("📄 Código Fonte:")
    print(codigo)
    
    result = compile(codigo, optimize=True, verbose=False)
    
    if result['success']:
        print("\n✅ COMPILAÇÃO BEM-SUCEDIDA!\n")
        
        print(f"📊 Estatísticas:")
        print(f"   • Tokens: {len(result['tokens'])}")
        print(f"   • IR original: {len(result['ir'].get_instructions())} instruções")
        print(f"   • IR otimizado: {len(result['optimized_ir'].get_instructions())} instruções")
        print(f"   • Assembly: {len(result['assembly'])} linhas")
        
        print("\n📝 Assembly gerado:")
        for linha in result['assembly'][:15]:  # Primeiras 15 linhas
            print(f"   {linha}")
        if len(result['assembly']) > 15:
            print(f"   ... e mais {len(result['assembly']) - 15} linhas")
    else:
        print("❌ FALHA NA COMPILAÇÃO")
        for erro in result['errors']:
            print(f"   • {erro}")


def demo_funcoes():
    """Demonstração 2: Funções e chamadas"""
    print("\n" + "="*70)
    print(" DEMO 2: FUNÇÕES E CHAMADAS")
    print("="*70)
    
    codigo = """
    int soma(int a, int b) {
        int resultado = a + b;
        return resultado;
    }
    
    int main() {
        int x = 5;
        int y = 3;
        int z = soma(x, y);
        print(z);
        return 0;
    }
    """
    
    print("📄 Código Fonte:")
    print(codigo)
    
    result = compile(codigo, optimize=True, verbose=False)
    
    if result['success']:
        print("\n✅ COMPILAÇÃO BEM-SUCEDIDA!\n")
        
        print("🔍 Análise Semântica:")
        result['symbol_table'].print_table()
        
        print("\n📟 Código Intermediário (TAC) - Original:")
        result['ir'].print_code()
        
        print("\n⚡ Código Intermediário (TAC) - Otimizado:")
        result['optimized_ir'].print_code()


def demo_otimizacoes():
    """Demonstração 3: Poder das otimizações"""
    print("\n" + "="*70)
    print(" DEMO 3: OTIMIZAÇÕES EM AÇÃO")
    print("="*70)
    
    codigo = """
    int main() {
        int x = 5 + 3;
        int y = x * 1;
        int z = y + 0;
        int w = z - 0;
        print(w);
        return 0;
    }
    """
    
    print("📄 Código Fonte (com operações redundantes):")
    print(codigo)
    
    # Sem otimizações
    result_sem = compile(codigo, optimize=False, verbose=False)
    
    # Com otimizações
    result_com = compile(codigo, optimize=True, verbose=False)
    
    if result_sem['success'] and result_com['success']:
        print("\n📊 COMPARAÇÃO:\n")
        
        print("❌ SEM OTIMIZAÇÕES:")
        print(f"   • IR: {len(result_sem['ir'].get_instructions())} instruções")
        result_sem['ir'].print_code()
        
        print("\n✅ COM OTIMIZAÇÕES:")
        print(f"   • IR: {len(result_com['optimized_ir'].get_instructions())} instruções")
        result_com['optimized_ir'].print_code()
        
        reducao = len(result_sem['ir'].get_instructions()) - len(result_com['optimized_ir'].get_instructions())
        percentual = (reducao / len(result_sem['ir'].get_instructions())) * 100
        
        print(f"\n⚡ RESULTADO:")
        print(f"   • Redução: {reducao} instruções ({percentual:.1f}%)")
        print(f"   • Otimizações aplicadas:")
        print(f"      - Constant folding (5 + 3 → 8)")
        print(f"      - Identidades (x * 1 → x, x + 0 → x)")
        print(f"      - Copy propagation")
        print(f"      - Peephole optimization")


def demo_erros():
    """Demonstração 4: Detecção de erros"""
    print("\n" + "="*70)
    print(" DEMO 4: DETECÇÃO DE ERROS SEMÂNTICOS")
    print("="*70)
    
    erros = [
        ("Variável não declarada", """
        int main() {
            x = 5;
            return 0;
        }
        """),
        
        ("Função não declarada", """
        int main() {
            int x = foo(5);
            return 0;
        }
        """),
        
        ("Número errado de argumentos", """
        int soma(int a, int b) {
            return a + b;
        }
        
        int main() {
            int x = soma(5);
            return 0;
        }
        """),
        
        ("Função sem return", """
        int calcular(int x) {
            int y = x + 1;
        }
        
        int main() {
            return 0;
        }
        """)
    ]
    
    for titulo, codigo in erros:
        print(f"\n❌ Erro: {titulo}")
        print("   Código:")
        for linha in codigo.strip().split('\n'):
            print(f"      {linha}")
        
        result = compile(codigo, verbose=False)
        
        if not result['success']:
            print(f"   ✓ Detectado: {result['errors'][0]}")


def demo_complexo():
    """Demonstração 5: Exemplo complexo com chamadas aninhadas"""
    print("\n" + "="*70)
    print(" DEMO 5: EXEMPLO COMPLEXO - CHAMADAS ANINHADAS")
    print("="*70)
    
    codigo = """
    int dobro(int x) {
        return x + x;
    }
    
    int quadruplo(int x) {
        int temp = dobro(x);
        return dobro(temp);
    }
    
    int main() {
        int num = 5;
        int resultado = quadruplo(num);
        print(resultado);
        return 0;
    }
    """
    
    print("📄 Código Fonte:")
    print(codigo)
    
    result = compile(codigo, optimize=True, verbose=False)
    
    if result['success']:
        print("\n✅ COMPILAÇÃO BEM-SUCEDIDA!\n")
        
        print("🌳 AST (estrutura):")
        from compiler.ast import print_ast
        print_ast(result['ast'])
        
        print("\n📟 Código Intermediário (Otimizado):")
        result['optimized_ir'].print_code()
        
        print("\n📝 Assembly (primeiras 30 linhas):")
        for linha in result['assembly'][:30]:
            print(f"   {linha}")
        if len(result['assembly']) > 30:
            print(f"   ... e mais {len(result['assembly']) - 30} linhas")


def demo_completo():
    """Demonstração 6: Pipeline completo passo a passo"""
    print("\n" + "="*70)
    print(" DEMO 6: PIPELINE COMPLETO - PASSO A PASSO")
    print("="*70)
    
    codigo = """
    int main() {
        int x = 10;
        int y = x + 5;
        print(y);
        return 0;
    }
    """
    
    print("📄 Código Fonte:")
    print(codigo)
    
    result = compile(codigo, optimize=True, verbose=False)
    
    if result['success']:
        print("\n" + "─"*70)
        print("ETAPA 1: ANÁLISE LÉXICA")
        print("─"*70)
        print("Tokens gerados:")
        for tok in result['tokens'][:15]:
            print(f"   {tok}")
        if len(result['tokens']) > 15:
            print(f"   ... e mais {len(result['tokens']) - 15} tokens")
        
        print("\n" + "─"*70)
        print("ETAPA 2: ANÁLISE SINTÁTICA")
        print("─"*70)
        print("Parse Tree:")
        print(f"   {str(result['parse_tree'])[:200]}...")
        
        print("\n" + "─"*70)
        print("ETAPA 3: CONSTRUÇÃO DA AST")
        print("─"*70)
        from compiler.ast import print_ast
        print_ast(result['ast'])
        
        print("\n" + "─"*70)
        print("ETAPA 4: ANÁLISE SEMÂNTICA")
        print("─"*70)
        result['symbol_table'].print_table()
        
        print("\n" + "─"*70)
        print("ETAPA 5: GERAÇÃO DE IR (TAC)")
        print("─"*70)
        result['ir'].print_code()
        
        print("\n" + "─"*70)
        print("ETAPA 6: OTIMIZAÇÕES")
        print("─"*70)
        result['optimized_ir'].print_code()
        
        print("\n" + "─"*70)
        print("ETAPA 7: GERAÇÃO DE ASSEMBLY")
        print("─"*70)
        for linha in result['assembly']:
            print(f"   {linha}")
        
        print("\n✅ PIPELINE COMPLETO EXECUTADO COM SUCESSO!")


def main():
    """Executa todas as demonstrações"""
    print("\n" + "#"*70)
    print("#" + " "*68 + "#")
    print("#" + "  DEMONSTRAÇÃO COMPLETA DO COMPILADOR MODULAR".center(68) + "#")
    print("#" + " "*68 + "#")
    print("#"*70)
    
    demos = [
        ("Básico", demo_basico),
        ("Funções", demo_funcoes),
        ("Otimizações", demo_otimizacoes),
        ("Erros", demo_erros),
        ("Complexo", demo_complexo),
        ("Pipeline Completo", demo_completo)
    ]
    
    print("\n📚 Demonstrações disponíveis:")
    for i, (nome, _) in enumerate(demos, 1):
        print(f"   {i}. {nome}")
    print("   0. Executar todas")
    
    try:
        escolha = input("\nEscolha uma demonstração (0-6): ").strip()
        
        if escolha == '0':
            for nome, demo_func in demos:
                demo_func()
                input("\nPressione Enter para continuar...")
        elif escolha.isdigit() and 1 <= int(escolha) <= len(demos):
            demos[int(escolha) - 1][1]()
        else:
            print("Escolha inválida!")
    except KeyboardInterrupt:
        print("\n\nDemonstração cancelada.")
    
    print("\n" + "="*70)
    print(" FIM DA DEMONSTRAÇÃO")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
