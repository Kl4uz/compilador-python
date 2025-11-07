import ply.lex as lex

#Lista de tokens 
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
    'PRINT'
)

# lista de palavras reservadas

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

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
t_SEMICOLON = r';'
t_COMMA = r','

# um identificador é uma letra seguida de letras, dígitos ou underscores
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')    # Check for reserved words
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t                

# Define uma regra para contar linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value) 

# uma string de caracteres a serem ignorados (espaços e tabs)
t_ignore  = ' \t'

# Erro de caractere
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Construção do analisador léxico
lexer = lex.lex()
