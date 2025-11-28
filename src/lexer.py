"""
Analisador Léxico
Tokeniza o código fonte em tokens
"""

import ply.lex as lex
from typing import List, Any


# Lista de tokens
tokens = (
    'ID',
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'EQUALS',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'SEMICOLON',
    'COMMA',
)

# Lista de palavras reservadas
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'return': 'RETURN',
    'int': 'INT',
    'print': 'PRINT'
}

# Adiciona as palavras reservadas aos tokens
tokens = tokens + tuple(reserved.values())

# Definições de tokens simples (regex)
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_COMMA = r','


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # Verifica se é palavra reservada
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Caracteres a serem ignorados (espaços e tabs)
t_ignore = ' \t'


def t_error(t):
    """Tratamento de erros léxicos"""
    print(f"Erro léxico: caractere ilegal '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)


# Construção do analisador léxico
lexer = lex.lex()


def tokenize(source_code: str) -> List[Any]:
    """
    Tokeniza o código fonte
    
    Args:
        source_code: Código fonte a ser tokenizado
    
    Returns:
        Lista de tokens
    """
    lexer.input(source_code)
    return list(lexer)
