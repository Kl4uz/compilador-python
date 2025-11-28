"""
Ponto de Entrada Principal do Compilador
"""

import sys
import argparse
from pathlib import Path
from src.compiler import Compiler, compile_file


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description="Compilador Python - Compila código fonte para código intermediário"
    )
    parser.add_argument(
        "input_file",
        type=str,
        help="Arquivo de entrada com código fonte"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Arquivo de saída para código intermediário"
    )
    parser.add_argument(
        "--no-optimize",
        action="store_true",
        help="Desabilita otimizações"
    )
    parser.add_argument(
        "--assembly",
        action="store_true",
        help="Gera código assembly"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Modo verboso (mostra mais informações)"
    )
    
    args = parser.parse_args()
    
    # Verifica se arquivo existe
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Erro: Arquivo '{args.input_file}' não encontrado")
        sys.exit(1)
    
    # Compila
    try:
        result = compile_file(
            str(input_path),
            args.output,
            optimize=not args.no_optimize,
            generate_assembly=args.assembly
        )
        
        # Cria compilador para imprimir resultados
        compiler = Compiler(
            optimize=not args.no_optimize,
            generate_assembly=args.assembly
        )
        
        if args.verbose or not result["success"]:
            compiler.print_results(result)
        else:
            if result["success"]:
                print("✓ Compilação bem-sucedida!")
                if result["warnings"]:
                    print("\nAvisos:")
                    for warning in result["warnings"]:
                        print(f"  {warning}")
            else:
                print("✗ Erros na compilação:")
                for error in result["errors"]:
                    print(f"  - {error}")
                sys.exit(1)
    
    except Exception as e:
        print(f"Erro inesperado: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()