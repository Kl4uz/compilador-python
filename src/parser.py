import ply.yacc as yacc
from src.lexer import tokens

# Precedência dos operadores
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'EQUALS'),
)   

def p_program(p):
    '''program : statement_list'''
    p[0] = ('program', p[1])  

def p_stmt_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_stmt_assign(p):
    '''statement : ID EQUALS expression SEMICOLON'''
    p[0] = ('assign', p[1], p[3])

def p_stmt_print(p):
    '''statement : PRINT LPAREN expression RPAREN SEMICOLON'''
    p[0] = ('print', p[3])

def p_expr_term(p):
    '''expression : term'''
    p[0] = p[1]

def p_term_muldiv(p):
    '''term : term TIMES factor
            | term DIVIDE factor'''
    p[0] = (p[2], p[1], p[3])

def p_term_factor(p):
    '''term : factor'''
    p[0] = p[1]

def p_factor_num(p):
    '''factor : NUMBER'''
    p[0] = ('num', p[1])

def p_factor_id(p):
    '''factor : ID'''
    p[0] = ('id', p[1])

def p_factor_expr(p):
    '''factor : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_expr_addsub(p):
    '''expression : expression PLUS term
                  | expression MINUS term'''
    p[0] = (p[2], p[1], p[3])

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()