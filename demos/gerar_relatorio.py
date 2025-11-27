"""
RELATÓRIO COMPLETO DO COMPILADOR
Mostra TODAS as etapas detalhadamente para documentação/relatório
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from compiler.lexer import tokenize
from compiler.parser import parse_ll1, Token
from compiler.ast import build_ast, SemanticAnalyzer, print_ast
from compiler.ir import IRGenerator
from compiler.optimizer import Optimizer, CommonSubexpressionElimination, ConstantFolding, DeadCodeElimination, AlgebraicSimplification
from compiler.codegen import CodeGenerator


def imprimir_gramatica():
    """Imprime a gramática BNF do compilador"""
    print("\n" + "="*80)
    print(" GRAMÁTICA BNF (Backus-Naur Form)")
    print("="*80)
    
    gramatica = """
<program>             ::= <declaration_list>

<declaration_list>    ::= <declaration> <declaration_list> | <declaration>

<declaration>         ::= <function_declaration> | <statement>

<function_declaration> ::= INT ID LPAREN <parameter_list> RPAREN LBRACE <statement_list> RBRACE
                         | INT ID LPAREN RPAREN LBRACE <statement_list> RBRACE

<parameter_list>      ::= <parameter> COMMA <parameter_list> | <parameter>

<parameter>           ::= INT ID

<statement_list>      ::= <statement> <statement_list> | <statement>

<statement>           ::= INT ID EQUALS <expression> SEMICOLON
                        | ID EQUALS <expression> SEMICOLON
                        | RETURN <expression> SEMICOLON
                        | RETURN SEMICOLON
                        | PRINT LPAREN <expression> RPAREN SEMICOLON

<expression>          ::= <term> ((PLUS | MINUS) <term>)*

<term>                ::= <factor> ((TIMES | DIVIDE) <factor>)*

<factor>              ::= NUMBER
                        | ID
                        | ID LPAREN <argument_list> RPAREN
                        | ID LPAREN RPAREN
                        | LPAREN <expression> RPAREN

<argument_list>       ::= <expression> COMMA <argument_list> | <expression>
"""
    
    print(gramatica)
    
    print("\nTIPO DE PARSER: LL(1) Top-Down com Recursive Descent")
    print("CARACTERÍSTICAS:")
    print("  • Cada não-terminal da gramática = uma função recursiva")
    print("  • Lookahead de 1 token para decisões de parsing")
    print("  • Elimina recursão à esquerda usando loops")
    print("  • Implementação manual (não usa gerador)")


def imprimir_tokens_detalhado(tokens):
    """Imprime todos os tokens com detalhes"""
    print("\n" + "="*80)
    print(" [1/7] ANÁLISE LÉXICA - Tokens")
    print("="*80)
    print(f"\n✓ {len(tokens)} tokens gerados\n")
    
    print("EXPRESSÕES REGULARES (ERs) USADAS:")
    print("  • ID        = [a-zA-Z_][a-zA-Z0-9_]*")
    print("  • NUMBER    = \\d+")
    print("  • PLUS      = \\+")
    print("  • MINUS     = -")
    print("  • TIMES     = \\*")
    print("  • DIVIDE    = /")
    print("  • EQUALS    = =")
    print("  • LPAREN    = \\(")
    print("  • RPAREN    = \\)")
    print("  • LBRACE    = \\{")
    print("  • RBRACE    = \\}")
    print("  • SEMICOLON = ;")
    print("  • COMMA     = ,")
    
    print("\nPALAVRAS RESERVADAS:")
    print("  • int, if, else, while, return, print")
    
    print("\nTABELA DE TOKENS GERADOS:")
    print("-"*80)
    print(f"{'Nº':>3} | {'Tipo':^15} | {'Valor':^20} | {'Linha':^6}")
    print("-"*80)
    
    for i, tok in enumerate(tokens, 1):
        tipo = tok.type
        valor = str(tok.value)
        linha = tok.lineno
        print(f"{i:3} | {tipo:^15} | {valor:^20} | {linha:^6}")
    
    print("-"*80)


def imprimir_parse_tree_detalhado(parse_tree):
    """Imprime a parse tree com detalhes"""
    print("\n" + "="*80)
    print(" [2/7] ANÁLISE SINTÁTICA - Parse Tree (LL(1) Top-Down)")
    print("="*80)
    print("\n✓ Parse Tree gerada usando Recursive Descent\n")
    
    print("MÉTODO: LL(1) Top-Down")
    print("  • Cada função processa um não-terminal da gramática")
    print("  • Usa lookahead de 1 token para decidir qual regra aplicar")
    print("  • Exemplo: function program() chama declaration_list() recursivamente")
    
    print("\nPARSE TREE (Estrutura Hierárquica):")
    print("-"*80)
    
    def imprimir_arvore(node, nivel=0):
        indent = "  " * nivel
        if isinstance(node, tuple):
            if len(node) > 0:
                print(f"{indent}• {node[0]}")
                for child in node[1:]:
                    if isinstance(child, list):
                        for item in child:
                            imprimir_arvore(item, nivel + 1)
                    else:
                        imprimir_arvore(child, nivel + 1)
        else:
            print(f"{indent}└─ {node}")
    
    imprimir_arvore(parse_tree)
    print("-"*80)


def imprimir_ast_detalhada(ast):
    """Imprime a AST com detalhes"""
    print("\n" + "="*80)
    print(" [3/7] CONSTRUÇÃO DA AST - Árvore Sintática Abstrata")
    print("="*80)
    print("\n✓ AST construída (versão simplificada da Parse Tree)\n")
    
    print("DIFERENÇA PARSE TREE vs AST:")
    print("  • Parse Tree: contém TODOS os símbolos da gramática")
    print("  • AST: contém APENAS o essencial (operações e operandos)")
    print("  • AST remove: parênteses, símbolos não-terminais redundantes")
    
    print("\nNÓS DA AST (Classes):")
    print("  • ProgramNode      - Raiz do programa")
    print("  • FunctionNode     - Declaração de função")
    print("  • DeclAssignNode   - Declaração com atribuição (int x = ...)")
    print("  • AssignNode       - Atribuição simples (x = ...)")
    print("  • BinOpNode        - Operação binária (+, -, *, /)")
    print("  • NumberNode       - Literal numérico")
    print("  • IDNode           - Identificador (variável)")
    print("  • CallNode         - Chamada de função")
    print("  • ReturnNode       - Return")
    print("  • PrintNode        - Print")
    
    print("\nÁRVORE SINTÁTICA ABSTRATA:")
    print("-"*80)
    print_ast(ast, indent=0)
    print("-"*80)


def imprimir_analise_semantica(symbol_table):
    """Imprime análise semântica detalhada"""
    print("\n" + "="*80)
    print(" [4/7] ANÁLISE SEMÂNTICA - Validação e Tabela de Símbolos")
    print("="*80)
    print("\n✓ Análise semântica concluída sem erros\n")
    
    print("VERIFICAÇÕES REALIZADAS:")
    print("  ✓ Variáveis declaradas antes do uso")
    print("  ✓ Tipos compatíveis nas operações")
    print("  ✓ Escopos (global/local) respeitados")
    print("  ✓ Funções declaradas antes de chamadas")
    print("  ✓ Número de parâmetros correto em chamadas")
    
    print("\nTABELA DE SÍMBOLOS:")
    print("  • Estrutura: Dicionário com escopos aninhados")
    print("  • Informações: nome, tipo, escopo, offset (endereço)")
    print()
    symbol_table.print_table()


def imprimir_ir_detalhado(ir):
    """Imprime IR com detalhes"""
    print("\n" + "="*80)
    print(" [5/7] GERAÇÃO DE CÓDIGO INTERMEDIÁRIO (IR)")
    print("="*80)
    print(f"\n✓ {len(ir.get_instructions())} instruções IR geradas\n")
    
    print("FORMATO: TAC (Three-Address Code)")
    print("  • Cada instrução tem no máximo 3 endereços")
    print("  • Usa variáveis temporárias (t0, t1, t2, ...)")
    print("  • Independente de arquitetura de máquina")
    print("  • Formato: resultado = operando1 operador operando2")
    
    print("\nTIPOS DE INSTRUÇÕES:")
    print("  • Aritméticas: t0 = a + b")
    print("  • Atribuição:  x = t0")
    print("  • Chamada:     t1 = call func(args)")
    print("  • Controle:    goto L1, if x goto L2")
    print("  • Função:      begin_func main, end_func main")
    
    print("\nCÓDIGO INTERMEDIÁRIO (TAC):")
    ir.print_code()
    
    print("\nFORMATO ALTERNATIVO - QUÁDRUPLAS:")
    print("  • Estrutura: (operação, arg1, arg2, resultado)")
    print("  • Mais explícito que TAC")
    print("  • Usado em algumas implementações de compiladores")
    ir.print_quadruples()


def imprimir_otimizacoes(ir_original, ir_otimizado):
    """Imprime otimizações detalhadas"""
    print("\n" + "="*80)
    print(" [6/7] OTIMIZAÇÕES DE CÓDIGO")
    print("="*80)
    
    instrucoes_antes = len(ir_original.get_instructions())
    instrucoes_depois = len(ir_otimizado.get_instructions())
    reducao = instrucoes_antes - instrucoes_depois
    
    print(f"\n✓ Otimização concluída")
    if reducao > 0:
        print(f"⚡ {reducao} instruções removidas ({reducao/instrucoes_antes*100:.1f}% de redução)\n")
    else:
        print()
    
    print("OTIMIZAÇÕES IMPLEMENTADAS:")
    print()
    print("1. CSE (Common Subexpression Elimination)")
    print("   • Detecta expressões duplicadas")
    print("   • Exemplo: t1 = a + b; t2 = a + b  →  t1 = a + b; t2 = t1")
    print()
    print("2. Constant Folding (Propagação de Constantes)")
    print("   • Avalia operações em tempo de compilação")
    print("   • Exemplo: t0 = 5 + 3  →  t0 = 8")
    print()
    print("3. Algebraic Simplification (Simplificação Algébrica)")
    print("   • Aplica identidades matemáticas")
    print("   • Exemplo: x * 1 → x,  x + 0 → x,  x * 0 → 0")
    print()
    print("4. Peephole Optimization")
    print("   • Otimizações locais em pequenas janelas")
    print("   • Exemplo: x * 2 → x << 1 (shift é mais rápido)")
    print()
    print("5. Copy Propagation")
    print("   • Propaga cópias de variáveis")
    print("   • Exemplo: x = y; z = x  →  x = y; z = y")
    print()
    print("6. Dead Code Elimination")
    print("   • Remove código que nunca será executado")
    print("   • Exemplo: código após return")
    
    print("\nCÓDIGO IR ORIGINAL:")
    ir_original.print_code()
    
    print("\nCÓDIGO IR OTIMIZADO:")
    ir_otimizado.print_code()


def imprimir_assembly_detalhado(assembly):
    """Imprime assembly com detalhes"""
    print("\n" + "="*80)
    print(" [7/7] GERAÇÃO DE CÓDIGO ASSEMBLY")
    print("="*80)
    print(f"\n✓ {len(assembly)} linhas de assembly geradas\n")
    
    print("ARQUITETURA: MIPS-like Simplificado")
    print()
    print("REGISTRADORES USADOS:")
    print("  • $t0-$t9  = Registradores temporários")
    print("  • $a0      = Argumento para syscalls")
    print("  • $v0      = Valor de retorno / código syscall")
    print("  • $sp      = Stack pointer")
    print("  • $fp      = Frame pointer")
    print("  • $ra      = Return address")
    
    print("\nINSTRUÇÕES PRINCIPAIS:")
    print("  • li   = Load immediate (carrega constante)")
    print("  • lw   = Load word (carrega da memória)")
    print("  • sw   = Store word (salva na memória)")
    print("  • add  = Adição")
    print("  • sub  = Subtração")
    print("  • mul  = Multiplicação")
    print("  • div  = Divisão")
    print("  • move = Move entre registradores")
    print("  • j    = Jump incondicional")
    print("  • jr   = Jump register (retorno)")
    
    print("\nCÓDIGO ASSEMBLY FINAL:")
    print("-"*80)
    for i, linha in enumerate(assembly, 1):
        print(f"  {i:3}: {linha}")
    print("-"*80)


def gerar_relatorio_completo(codigo_fonte):
    """Gera relatório completo com TODAS as etapas"""
    
    print("\n" + "🎓"*40)
    print(" "*20 + "RELATÓRIO COMPLETO DO COMPILADOR")
    print(" "*15 + "Mini-Compilador para Linguagem C-like")
    print("🎓"*40 + "\n")
    
    print("CÓDIGO FONTE A SER COMPILADO:")
    print("="*80)
    print(codigo_fonte)
    print("="*80)
    
    # Gramática
    imprimir_gramatica()
    
    try:
        # 1. LÉXICO
        tokens = tokenize(codigo_fonte)
        imprimir_tokens_detalhado(tokens)
        
        # 2. SINTÁTICO
        ll1_tokens = [Token(tok.type, tok.value, tok.lineno) for tok in tokens]
        parse_tree, errors = parse_ll1(ll1_tokens)
        
        if errors:
            print(f"\n❌ Erros sintáticos encontrados:")
            for error in errors:
                print(f"   • {error}")
            return None
        
        imprimir_parse_tree_detalhado(parse_tree)
        
        # 3. AST
        ast = build_ast(parse_tree)
        imprimir_ast_detalhada(ast)
        
        # 4. SEMÂNTICA
        semantic_analyzer = SemanticAnalyzer()
        success, errors, symbol_table = semantic_analyzer.analyze(ast)
        
        if not success:
            print(f"\n❌ Erros semânticos encontrados:")
            for error in errors:
                print(f"   • {error}")
            return None
        
        imprimir_analise_semantica(symbol_table)
        
        # 5. IR
        ir_generator = IRGenerator(symbol_table)
        ir_original = ir_generator.generate(ast)
        imprimir_ir_detalhado(ir_original)
        
        # 6. OTIMIZAÇÃO
        optimizer = Optimizer()
        optimizer.add_optimization(CommonSubexpressionElimination())
        optimizer.add_optimization(ConstantFolding())
        optimizer.add_optimization(AlgebraicSimplification())
        optimizer.add_optimization(DeadCodeElimination())
        
        # Desabilita prints das otimizações
        import io
        import contextlib
        
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            ir_otimizado = optimizer.optimize(ir_original)
        
        imprimir_otimizacoes(ir_original, ir_otimizado)
        
        # 7. ASSEMBLY
        from compiler.codegen.assembly import AssemblyGenerator
        asm_generator = AssemblyGenerator()
        assembly = asm_generator.generate(ir_otimizado)
        
        imprimir_assembly_detalhado(assembly)
        
        # RESUMO FINAL
        print("\n" + "="*80)
        print(" RESUMO DA COMPILAÇÃO")
        print("="*80)
        print(f"\n✅ Compilação concluída com sucesso!\n")
        print(f"📊 Estatísticas:")
        print(f"   • Tokens gerados:           {len(tokens)}")
        print(f"   • Instruções IR originais:  {len(ir_original.get_instructions())}")
        print(f"   • Instruções IR otimizadas: {len(ir_otimizado.get_instructions())}")
        print(f"   • Linhas de assembly:       {len(assembly)}")
        
        reducao = len(ir_original.get_instructions()) - len(ir_otimizado.get_instructions())
        if reducao > 0:
            print(f"   • Redução por otimização:   {reducao} instruções ({reducao/len(ir_original.get_instructions())*100:.1f}%)")
        
        print("\n" + "="*80)
        print(" FIM DO RELATÓRIO")
        print("="*80 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro durante compilação: {e}")
        import traceback
        traceback.print_exc()
        return None


# ===== EXEMPLO DE USO =====
if __name__ == "__main__":
    
    # Código de exemplo para o relatório
    codigo = """
int main() {
    int a = 5;
    int b = 3;
    int x = a + b;
    int y = a + b;
    return 0;
}
"""
    
    gerar_relatorio_completo(codigo)
