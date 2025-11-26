"""
Compilador Interativo - Interface Principal
Permite compilar expressões de três formas:
1. Via arquivo
2. Via entrada interativa
3. Via argumento de linha de comando
"""

import sys
import os

# Adiciona o diretório ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from compiler import compile


def compilar_expressao(expressao):
    """
    Compila uma expressão simples ou instrução
    Automaticamente envolve em uma função main() se necessário
    """
    expressao = expressao.strip()
    
    # Verifica se já tem estrutura de função completa
    if 'int main' in expressao or ('int ' in expressao and '{' in expressao and '}' in expressao):
        # Já é código completo
        return expressao
    
    # Verifica se é uma instrução (tem ponto e vírgula)
    if ';' in expressao:
        # Se já começa com int, assume que é código completo estruturado
        if expressao.count('int ') > 1 or '\n' in expressao:
            # Múltiplas linhas de código, envolve em main direto
            codigo_completo = f"""
int main() {{
    {expressao}
    return 0;
}}
"""
        else:
            # É uma instrução tipo "int x = a + b * 2;"
            # Extrai variáveis usadas (não declaradas)
            import re
            
            # Procura por IDs que não estão sendo declarados
            # Remove a parte de declaração (int x =)
            parte_expr = expressao
            if expressao.startswith('int '):
                parte_expr = re.sub(r'^int\s+\w+\s*=\s*', '', expressao)
            
            # Encontra todos os identificadores
            variaveis = re.findall(r'\b[a-z_][a-z0-9_]*\b', parte_expr.lower())
            # Remove palavras reservadas e números
            variaveis = [v for v in variaveis if v not in ['int', 'return', 'print', 'if', 'else', 'while']]
            
            # Cria declarações para variáveis não declaradas
            declaracoes = '\n    '.join([f'int {v} = {ord(v) % 10};' for v in set(variaveis)])
            
            codigo_completo = f"""
int main() {{
    {declaracoes}
    {expressao}
    return 0;
}}
"""
    else:
        # É uma expressão simples sem ;
        codigo_completo = f"""
int main() {{
    int resultado = {expressao};
    print(resultado);
    return 0;
}}
"""
    
    return codigo_completo


def mostrar_resultado(result, verbose=True):
    """Mostra o resultado da compilação de forma organizada"""
    
    if not result['success']:
        print("\n❌ ERRO DE COMPILAÇÃO:")
        for erro in result['errors']:
            print(f"   • {erro}")
        return False
    
    print("\n✅ COMPILAÇÃO BEM-SUCEDIDA!\n")
    
    if verbose:
        print("="*70)
        print(" TOKENS GERADOS")
        print("="*70)
        print(f"Total: {len(result['tokens'])} tokens\n")
        for i, tok in enumerate(result['tokens'][:20], 1):
            print(f"  {i:2}. {tok}")
        if len(result['tokens']) > 20:
            print(f"  ... e mais {len(result['tokens']) - 20} tokens")
        
        print("\n" + "="*70)
        print(" TABELA DE SÍMBOLOS")
        print("="*70)
        result['symbol_table'].print_table()
        
        print("\n" + "="*70)
        print(" CÓDIGO INTERMEDIÁRIO (TAC)")
        print("="*70)
        result['ir'].print_code()
        
        print("\n" + "="*70)
        print(" QUÁDRUPLAS (Formato do Professor)")
        print("="*70)
        result['ir'].print_quadruples()
        
        print("\n" + "="*70)
        print(" CÓDIGO INTERMEDIÁRIO OTIMIZADO")
        print("="*70)
        result['optimized_ir'].print_code()
        
        instrucoes_antes = len(result['ir'].get_instructions())
        instrucoes_depois = len(result['optimized_ir'].get_instructions())
        reducao = instrucoes_antes - instrucoes_depois
        
        if reducao > 0:
            print(f"\n⚡ Otimização: {reducao} instruções removidas ({reducao/instrucoes_antes*100:.1f}%)")
        
        print("\n" + "="*70)
        print(" CÓDIGO ASSEMBLY (MIPS-like)")
        print("="*70)
        for i, linha in enumerate(result['assembly'], 1):
            print(f"  {i:3}: {linha}")
    else:
        # Modo resumido
        print(f"📊 Tokens: {len(result['tokens'])}")
        print(f"📊 IR: {len(result['ir'].get_instructions())} instruções")
        print(f"📊 IR Otimizado: {len(result['optimized_ir'].get_instructions())} instruções")
        print(f"📊 Assembly: {len(result['assembly'])} linhas")
        print("\n💡 Use --verbose para ver detalhes completos")
    
    return True


def modo_interativo():
    """Modo interativo: usuário digita expressões"""
    print("\n" + "="*70)
    print(" COMPILADOR INTERATIVO")
    print("="*70)
    print("\nDigite uma expressão ou código para compilar.")
    print("Exemplos:")
    print("  • 5 + 3 * 2")
    print("  • (10 - 5) * 4 / 2")
    print("  • int x = 5 + 3;")
    print("\nComandos especiais:")
    print("  • 'sair' ou 'exit' para sair")
    print("  • 'arquivo <nome>' para compilar arquivo")
    print("  • 'verbose on/off' para ligar/desligar modo detalhado")
    print("="*70)
    
    verbose = True
    
    while True:
        try:
            print("\n>>> ", end="")
            entrada = input().strip()
            
            if not entrada:
                continue
            
            # Comandos especiais
            if entrada.lower() in ['sair', 'exit', 'quit']:
                print("\n👋 Até logo!")
                break
            
            if entrada.lower().startswith('verbose'):
                if 'on' in entrada.lower():
                    verbose = True
                    print("✓ Modo verbose ativado")
                else:
                    verbose = False
                    print("✓ Modo verbose desativado")
                continue
            
            if entrada.lower().startswith('arquivo'):
                partes = entrada.split()
                if len(partes) < 2:
                    print("❌ Uso: arquivo <nome_do_arquivo>")
                    continue
                
                arquivo = partes[1]
                if not os.path.exists(arquivo):
                    print(f"❌ Arquivo '{arquivo}' não encontrado")
                    continue
                
                with open(arquivo, 'r', encoding='utf-8') as f:
                    codigo = f.read()
                
                print(f"\n📄 Compilando arquivo: {arquivo}")
                print("─"*70)
                print(codigo)
                print("─"*70)
                
                result = compile(codigo, optimize=True, verbose=False)
                mostrar_resultado(result, verbose)
                continue
            
            # Compilar expressão
            codigo = compilar_expressao(entrada)
            
            print("\n📝 Código gerado:")
            print("─"*70)
            print(codigo)
            print("─"*70)
            
            result = compile(codigo, optimize=True, verbose=False)
            mostrar_resultado(result, verbose)
            
        except KeyboardInterrupt:
            print("\n\n👋 Até logo!")
            break
        except Exception as e:
            print(f"\n❌ Erro: {e}")
            import traceback
            traceback.print_exc()


def compilar_arquivo(arquivo, verbose=True, output=None):
    """Compila um arquivo"""
    
    if not os.path.exists(arquivo):
        print(f"❌ Arquivo '{arquivo}' não encontrado")
        return False
    
    with open(arquivo, 'r', encoding='utf-8') as f:
        codigo = f.read().strip()
    
    print(f"\n📄 Compilando: {arquivo}")
    print("="*70)
    print("CÓDIGO FONTE ORIGINAL:")
    print("="*70)
    print(codigo)
    print("="*70)
    
    # Se não tem estrutura de função, trata como expressão
    codigo_completo = compilar_expressao(codigo)
    
    if codigo_completo != codigo:
        print("\n📝 Código processado:")
        print("─"*70)
        print(codigo_completo)
        print("─"*70)
    
    result = compile(codigo_completo, optimize=True, verbose=False)
    
    sucesso = mostrar_resultado(result, verbose)
    
    # Salvar assembly se especificado
    if sucesso and output:
        with open(output, 'w', encoding='utf-8') as f:
            for linha in result['assembly']:
                f.write(linha + '\n')
        print(f"\n💾 Assembly salvo em: {output}")
    
    return sucesso


def main():
    """Função principal"""
    
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Mini-Compilador - Compile expressões e código',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:

  # Modo interativo
  python run.py
  
  # Compilar expressão direta
  python run.py -e "5 + 3 * 2"
  
  # Compilar arquivo
  python run.py -f tests/hello_world.txt
  
  # Compilar e salvar assembly
  python run.py -f tests/code.txt -o output.asm
  
  # Modo resumido (sem detalhes)
  python run.py -f tests/code.txt --quiet
"""
    )
    
    parser.add_argument('-e', '--expressao', help='Expressão para compilar')
    parser.add_argument('-f', '--file', help='Arquivo para compilar')
    parser.add_argument('-o', '--output', help='Arquivo de saída para assembly')
    parser.add_argument('-q', '--quiet', action='store_true', help='Modo resumido (sem verbose)')
    parser.add_argument('-i', '--interactive', action='store_true', help='Modo interativo')
    
    args = parser.parse_args()
    
    verbose = not args.quiet
    
    # Modo interativo
    if args.interactive or (not args.expressao and not args.file):
        modo_interativo()
        return 0
    
    # Compilar expressão
    if args.expressao:
        print("\n📝 Expressão: " + args.expressao)
        codigo = compilar_expressao(args.expressao)
        
        print("\n📄 Código completo:")
        print("─"*70)
        print(codigo)
        print("─"*70)
        
        result = compile(codigo, optimize=True, verbose=False)
        
        if mostrar_resultado(result, verbose):
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    for linha in result['assembly']:
                        f.write(linha + '\n')
                print(f"\n💾 Assembly salvo em: {args.output}")
            return 0
        return 1
    
    # Compilar arquivo
    if args.file:
        if compilar_arquivo(args.file, verbose, args.output):
            return 0
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
