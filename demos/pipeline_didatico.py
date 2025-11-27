"""
Exemplo Didático - Pipeline Simplificado
Mostra claramente as 7 etapas do compilador conforme professor ensinou
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from compiler.lexer import tokenize
from compiler.parser import parse_ll1, Token
from compiler.ast import build_ast, SemanticAnalyzer
from compiler.ir import IRGenerator
from compiler.optimizer import Optimizer, CommonSubexpressionElimination, ConstantFolding, DeadCodeElimination
from compiler.codegen import CodeGenerator


def compile_program(source_code):
    """
    Pipeline completo do compilador em 7 etapas
    Conforme metodologia ensinada pelo professor
    """
    
    print("="*70)
    print(" PIPELINE DO COMPILADOR - 7 ETAPAS")
    print("="*70)
    
    # ===== 1. ANÁLISE LÉXICA =====
    print("\n[1/7] ANÁLISE LÉXICA - Tokens")
    tokens = tokenize(source_code)
    print(f"      ✓ {len(tokens)} tokens gerados")
    
    # ===== 2. ANÁLISE SINTÁTICA (LL(1) TOP-DOWN) =====
    print("\n[2/7] ANÁLISE SINTÁTICA - Parse Tree (LL(1) Top-Down)")
    ll1_tokens = [Token(tok.type, tok.value, tok.lineno) for tok in tokens]
    parse_tree, errors = parse_ll1(ll1_tokens)
    
    if errors:
        print(f"      ✗ Erros sintáticos encontrados")
        return None
    
    print(f"      ✓ Parse Tree gerada (Recursive Descent)")
    
    # ===== 3. CONSTRUÇÃO DA AST =====
    print("\n[3/7] CONSTRUÇÃO DA AST - Árvore Sintática Abstrata")
    ast = build_ast(parse_tree)
    print(f"      ✓ AST construída")
    
    # ===== 4. ANÁLISE SEMÂNTICA =====
    print("\n[4/7] ANÁLISE SEMÂNTICA - Tabela de Símbolos")
    semantic_analyzer = SemanticAnalyzer()
    success, errors, symbol_table = semantic_analyzer.analyze(ast)
    
    if not success:
        print(f"      ✗ Erros semânticos:")
        for error in errors:
            print(f"         • {error}")
        return None
    
    print(f"      ✓ Análise semântica concluída")
    symbol_table.print_table()
    
    # ===== 5. GERAÇÃO DE IR (CÓDIGO INTERMEDIÁRIO) =====
    print("\n[5/7] GERAÇÃO DE IR - TAC (Three-Address Code)")
    ir_generator = IRGenerator(symbol_table)
    ir = ir_generator.generate(ast)
    print(f"      ✓ {len(ir.get_instructions())} instruções IR geradas")
    ir.print_code()
    
    print("\n      QUÁDRUPLAS (op, arg1, arg2, result):")
    ir.print_quadruples()
    
    # ===== 6. OTIMIZAÇÃO =====
    print("\n[6/7] OTIMIZAÇÃO - CSE, Constant Folding, Dead Code")
    optimizer = Optimizer()
    optimizer.add_optimization(CommonSubexpressionElimination())
    optimizer.add_optimization(ConstantFolding())
    optimizer.add_optimization(DeadCodeElimination())
    
    optimized_ir = optimizer.optimize(ir)
    
    instrucoes_antes = len(ir.get_instructions())
    instrucoes_depois = len(optimized_ir.get_instructions())
    reducao = instrucoes_antes - instrucoes_depois
    
    print(f"      ✓ Otimização concluída")
    if reducao > 0:
        print(f"      ⚡ {reducao} instruções removidas ({reducao/instrucoes_antes*100:.1f}%)")
    
    optimized_ir.print_code()
    
    # ===== 7. GERAÇÃO DE ASSEMBLY =====
    print("\n[7/7] GERAÇÃO DE ASSEMBLY - MIPS-like")
    codegen = CodeGenerator(symbol_table, enable_optimizations=False)
    # Usa IR já otimizado
    from compiler.codegen.assembly import AssemblyGenerator
    asm_generator = AssemblyGenerator()
    assembly = asm_generator.generate(optimized_ir)
    
    print(f"      ✓ {len(assembly)} linhas de assembly geradas")
    print("\n" + "="*70)
    print(" ASSEMBLY FINAL")
    print("="*70)
    for i, linha in enumerate(assembly, 1):
        print(f"  {i:3}: {linha}")
    
    print("\n" + "="*70)
    print(" ✅ COMPILAÇÃO CONCLUÍDA COM SUCESSO!")
    print("="*70)
    
    return {
        'tokens': tokens,
        'parse_tree': parse_tree,
        'ast': ast,
        'symbol_table': symbol_table,
        'ir': ir,
        'optimized_ir': optimized_ir,
        'assembly': assembly
    }


# ===== EXEMPLO DE USO =====
if __name__ == "__main__":
    
    print("\n" + "🎓"*35)
    print("    EXEMPLO DIDÁTICO - PIPELINE COMPLETO DO COMPILADOR")
    print("🎓"*35 + "\n")
    
    # Código de exemplo
    codigo_fonte = """
int main() {
    int a = 5;
    int b = 3;
    int x = a + b;
    int y = a + b;
    return 0;
}
"""
    
    print("CÓDIGO FONTE:")
    print("-"*70)
    print(codigo_fonte)
    print("-"*70)
    
    # Compila
    resultado = compile_program(codigo_fonte)
    
    if resultado:
        print("\n✨ Pipeline executado com sucesso!")
        print(f"\n📊 Resumo:")
        print(f"   • Tokens: {len(resultado['tokens'])}")
        print(f"   • IR: {len(resultado['ir'].get_instructions())} instruções")
        print(f"   • IR Otimizado: {len(resultado['optimized_ir'].get_instructions())} instruções")
        print(f"   • Assembly: {len(resultado['assembly'])} linhas")
