"""
Mini-Compilador - Pipeline Integrado
Compilador completo: Léxico -> Sintático -> Semântico -> IR -> Otimizações -> Assembly

Uso:
    from compiler.main import compile
    
    result = compile(codigo_fonte)
    if result['success']:
        print("Compilação bem-sucedida!")
        print(result['assembly'])
"""

import sys
from .lexer import tokenize, lexer
from .parser import parse_ll1, Token
from .ast import build_ast, print_ast
from .ast import SemanticAnalyzer
from .codegen import CodeGenerator


class CompilationError(Exception):
    """Erro de compilação"""
    pass


def compile(source_code, optimize=True, verbose=False):
    """
    **FUNÇÃO PRINCIPAL DO COMPILADOR**
    
    Pipeline completo de compilação:
    1. Análise Léxica (Tokenização)
    2. Análise Sintática (Parse Tree)
    3. Construção da AST
    4. Análise Semântica
    5. Geração de IR (Three-Address Code)
    6. Otimizações (opcional)
    7. Geração de Assembly
    
    Args:
        source_code (str): Código fonte a compilar
        optimize (bool): Se True, aplica otimizações
        verbose (bool): Se True, imprime informações detalhadas
    
    Returns:
        dict: {
            'success': bool,
            'tokens': list,
            'parse_tree': tuple,
            'ast': ASTNode,
            'symbol_table': SymbolTable,
            'ir': IRProgram,
            'optimized_ir': IRProgram,
            'assembly': list[str],
            'errors': list[str]
        }
    """
    result = {
        'success': False,
        'tokens': [],
        'parse_tree': None,
        'ast': None,
        'symbol_table': None,
        'ir': None,
        'optimized_ir': None,
        'assembly': [],
        'errors': []
    }
    
    try:
        # ===== ETAPA 1: ANÁLISE LÉXICA =====
        if verbose:
            print("\n" + "="*50)
            print("ETAPA 1: ANÁLISE LÉXICA")
            print("="*50)
        
        tokens = tokenize(source_code)
        result['tokens'] = tokens
        
        if verbose:
            print(f"✓ {len(tokens)} tokens gerados")
            for tok in tokens[:10]:  # Mostra primeiros 10
                print(f"  {tok}")
            if len(tokens) > 10:
                print(f"  ... e mais {len(tokens) - 10} tokens")
        
        # ===== ETAPA 2: ANÁLISE SINTÁTICA (LL(1) TOP-DOWN) =====
        if verbose:
            print("\n" + "="*50)
            print("ETAPA 2: ANÁLISE SINTÁTICA (LL(1) Top-Down)")
            print("="*50)
        
        # Converte tokens PLY para formato do parser LL(1)
        ll1_tokens = [Token(tok.type, tok.value, tok.lineno) for tok in tokens]
        parse_tree, parse_errors = parse_ll1(ll1_tokens)
        
        if parse_errors:
            result['errors'].extend(parse_errors)
            return result
        
        result['parse_tree'] = parse_tree
        
        if verbose:
            print("✓ Parse Tree gerada com Recursive Descent (LL(1))")
            print(f"  Estrutura: {str(parse_tree)[:100]}...")
        
        # ===== ETAPA 3: CONSTRUÇÃO DA AST =====
        if verbose:
            print("\n" + "="*50)
            print("ETAPA 3: CONSTRUÇÃO DA AST")
            print("="*50)
        
        ast = build_ast(parse_tree)
        result['ast'] = ast
        
        if verbose:
            print("✓ AST construída")
            print_ast(ast)
        
        # ===== ETAPA 4: ANÁLISE SEMÂNTICA =====
        if verbose:
            print("\n" + "="*50)
            print("ETAPA 4: ANÁLISE SEMÂNTICA")
            print("="*50)
        
        analyzer = SemanticAnalyzer()
        success, errors, symbol_table = analyzer.analyze(ast)
        
        result['symbol_table'] = symbol_table
        
        if not success:
            result['errors'] = errors
            if verbose:
                print("✗ Erros semânticos encontrados:")
                for error in errors:
                    print(f"  - {error}")
            return result
        
        if verbose:
            print("✓ Análise semântica concluída sem erros")
            symbol_table.print_table()
        
        # ===== ETAPAS 5-7: GERAÇÃO DE CÓDIGO =====
        if verbose:
            print("\n" + "="*50)
            print("ETAPAS 5-7: GERAÇÃO DE CÓDIGO")
            print("="*50)
        
        codegen = CodeGenerator(symbol_table, enable_optimizations=optimize)
        ir_program, optimized_ir, assembly = codegen.generate(ast)
        
        result['ir'] = ir_program
        result['optimized_ir'] = optimized_ir
        result['assembly'] = assembly
        result['success'] = True
        
        if verbose:
            codegen.print_ir()
            if optimize:
                codegen.print_optimized_ir()
            codegen.print_assembly()
        
        if verbose:
            print("\n" + "="*50)
            print("✓ COMPILAÇÃO CONCLUÍDA COM SUCESSO!")
            print("="*50)
        
        return result
        
    except Exception as e:
        result['errors'].append(str(e))
        if verbose:
            print(f"\n✗ ERRO DE COMPILAÇÃO: {e}")
            import traceback
            traceback.print_exc()
        return result


def compile_file(filepath, optimize=True, verbose=False):
    """
    Compila um arquivo de código fonte
    
    Args:
        filepath (str): Caminho do arquivo
        optimize (bool): Se True, aplica otimizações
        verbose (bool): Se True, imprime informações detalhadas
    
    Returns:
        dict: Resultado da compilação (mesmo formato de compile())
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        if verbose:
            print(f"Compilando arquivo: {filepath}")
            print(f"Tamanho: {len(source_code)} caracteres")
        
        return compile(source_code, optimize, verbose)
        
    except FileNotFoundError:
        return {
            'success': False,
            'errors': [f"Arquivo não encontrado: {filepath}"]
        }
    except Exception as e:
        return {
            'success': False,
            'errors': [f"Erro ao ler arquivo: {e}"]
        }


def main():
    """
    Função main para uso via linha de comando
    
    Uso: python main.py <arquivo.txt> [--no-optimize] [--verbose]
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Mini-Compilador')
    parser.add_argument('file', help='Arquivo de código fonte')
    parser.add_argument('--no-optimize', action='store_true', help='Desabilita otimizações')
    parser.add_argument('--verbose', '-v', action='store_true', help='Modo verboso')
    parser.add_argument('--output', '-o', help='Arquivo de saída para assembly')
    
    args = parser.parse_args()
    
    # Compila arquivo
    result = compile_file(
        args.file,
        optimize=not args.no_optimize,
        verbose=args.verbose
    )
    
    # Verifica resultado
    if result['success']:
        print(f"\n✓ Compilação de '{args.file}' concluída com sucesso!")
        
        # Salva assembly se especificado
        if args.output:
            with open(args.output, 'w') as f:
                for line in result['assembly']:
                    f.write(line + '\n')
            print(f"Assembly salvo em: {args.output}")
        else:
            print("\nCódigo Assembly:")
            for line in result['assembly']:
                print(line)
        
        return 0
    else:
        print(f"\n✗ Compilação de '{args.file}' falhou!")
        print("\nErros:")
        for error in result['errors']:
            print(f"  - {error}")
        return 1


# ===== TESTES RÁPIDOS =====
if __name__ == "__main__":
    # Se executado com argumentos, usa CLI
    if len(sys.argv) > 1:
        sys.exit(main())
    
    # Senão, roda teste embutido
    print("=== TESTE RÁPIDO DO COMPILADOR ===\n")
    
    test_code = """
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
    
    print("Código fonte:")
    print(test_code)
    
    result = compile(test_code, optimize=True, verbose=True)
    
    if result['success']:
        print("\n✓ Teste concluído com sucesso!")
    else:
        print("\n✗ Teste falhou!")
        for error in result['errors']:
            print(f"  - {error}")
