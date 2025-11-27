"""
Compilador Modular - Mini-Compilador Python

Pipeline completo de compilação:
    Código Fonte → Tokens → Parse Tree → AST → 
    Análise Semântica → IR → Otimizações → Assembly

Uso básico:
    from compiler import compile
    
    result = compile(codigo_fonte)
    if result['success']:
        print(result['assembly'])
"""

from .main import compile, compile_file

__version__ = "1.0.0"
__author__ = "Projeto Compilador"

__all__ = ['compile', 'compile_file']
