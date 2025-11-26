"""
Analisador Léxico - Fase 1 do Compilador
Converte código fonte em tokens
"""
import ply.lex as lex

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

# Palavras reservadas
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

# Regras de tokens simples
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

# Regra para identificadores
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Regra para números
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Regra para contar linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Caracteres ignorados
t_ignore = ' \t'

# Tratamento de erros
def t_error(t):
    print(f"[ERRO LÉXICO] Caractere ilegal '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)

# Constrói o lexer
lexer = lex.lex()

def tokenize(source_code):
    """
    Função principal que tokeniza o código fonte
    Retorna lista de tokens para o parser
    """
    lexer.input(source_code)
    tokens_list = []
    
    for tok in lexer:
        tokens_list.append(tok)
    
    return tokens_list

# Para testes
if __name__ == "__main__":
    test_code = """
    int x = 10 + 20;
    print(x);
    """
    
    print("=== TESTE DO LEXER ===")
    print("Código:")
    print(test_code)
    print("\nTokens:")
    
    tokens = tokenize(test_code)
    for tok in tokens:
        print(f"{tok.type:12} {tok.value}")
