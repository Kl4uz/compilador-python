"""
Analisador Léxico - Tokenização
Converte código-fonte em stream de tokens usando PLY (Python Lex-Yacc)
Primeira fase do compilador: texto → tokens
"""
import ply.lex as lex

# Lista de tipos de tokens reconhecidos
tokens = (
    'ID', 'NUMBER',                              # Identificadores e números
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS',  # Operadores
    'LT', 'GT', 'LE', 'GE', 'EQ', 'NE',        # Operadores relacionais
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',     # Delimitadores
    'SEMICOLON', 'COMMA',                        # Pontuação
)

# Palavras reservadas da linguagem
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'return': 'RETURN',
    'int': 'INT',
    'print': 'PRINT'
}

# Adiciona palavras reservadas aos tokens
tokens = tokens + tuple(reserved.values())

# ═══════════════════════════════════════════════════════
# REGRAS DE TOKENIZAÇÃO (Expressões Regulares)
# ═══════════════════════════════════════════════════════

# Tokens simples - padrões de 1 caractere
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_EQUALS    = r'='
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBRACE    = r'\{'
t_RBRACE    = r'\}'
t_SEMICOLON = r';'
t_COMMA     = r','
t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='
t_LT = r'<'
t_GT = r'>'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'  # Identificadores e palavras reservadas
    t.type = reserved.get(t.value, 'ID')  # Verifica se é palavra reservada
    return t

def t_NUMBER(t):
    r'\d+'  # Números inteiros
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'  # Rastreia quebras de linha para relatório de erros
    t.lexer.lineno += len(t.value)

# Ignora espaços e tabs
t_ignore = ' \t'

def t_error(t):
    """Trata caracteres ilegais"""
    print(f"[ERRO LÉXICO] Caractere ilegal '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)

# Cria lexer (força recriação a cada import)
lexer = lex.lex()

def tokenize(source_code):
    """Tokeniza código fonte e retorna lista de tokens"""
    # Recria lexer para evitar problemas de cache
    local_lexer = lex.lex()
    local_lexer.input(source_code)
    return list(local_lexer)