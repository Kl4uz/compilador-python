import ply.yacc as yacc
from src.lexer import tokens

# Precedência dos operadores
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'EQUALS'),
)   

def p_program(p):
    '''program : declaration_list'''
    p[0] = ('program', p[1])

def p_declaration_list(p):
    '''declaration_list : declaration_list declaration
                        | declaration'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_declaration(p):
    '''declaration : function_declaration
                   | statement'''
    p[0] = p[1]

def p_function_declaration(p):
    '''function_declaration : INT ID LPAREN parameter_list RPAREN LBRACE statement_list RBRACE
                            | INT ID LPAREN RPAREN LBRACE statement_list RBRACE'''
    if len(p) == 9:
        p[0] = ('function', p[2], p[4], p[7])  # nome, parametros, corpo
    else:
        p[0] = ('function', p[2], [], p[6])    # nome, sem parametros, corpo

def p_parameter_list(p):
    '''parameter_list : parameter_list COMMA parameter
                      | parameter'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_parameter(p):
    '''parameter : INT ID'''
    p[0] = ('param', p[2], 'int')  

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

def p_stmt_return(p):
    '''statement : RETURN expression SEMICOLON
                 | RETURN SEMICOLON'''
    if len(p) == 4:
        p[0] = ('return', p[2])
    else:
        p[0] = ('return', None)

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

def p_factor_call(p):
    '''factor : ID LPAREN argument_list RPAREN
              | ID LPAREN RPAREN'''
    if len(p) == 5:
        p[0] = ('call', p[1], p[3])  # nome da função, argumentos
    else:
        p[0] = ('call', p[1], [])    # nome da função, sem argumentos

def p_argument_list(p):
    '''argument_list : argument_list COMMA expression
                     | expression'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

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

# Função para pretty-print da AST (recursiva)
def print_ast(node, indent=0):
    if node is None:
        return
    print('  ' * indent + f"{node.type}" + (f" ({node.value})" if node.value else ""))
    for child in node.children:
        print_ast(child, indent + 1)