import ply.yacc as yacc
from lexer import tokens

# Tabela de símbolos global
symbol_table = {}

# Precedência dos operadores
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'EQUALS'),
)

# Função auxiliar para inferir tipos
def infer_type(node):
    if node[0] == 'num':
        return 'int'
    elif node[0] == 'id':
        return symbol_table.get(node[1], {}).get('type', 'unknown')
    elif node[0] in ('+', '-', '*', '/'):
        left_type = infer_type(node[1])
        right_type = infer_type(node[2])
        if left_type == 'int' and right_type == 'int':
            return 'int'
        return 'unknown'
    return 'unknown'

# Contador para variáveis temporárias
temp_count = 0

def new_temp():
    global temp_count
    temp_count += 1
    return f't{temp_count}'

# Função para gerar código TAC
def generate_tac(ast):
    tac = []
    
    def traverse(node):
        nonlocal tac
        if isinstance(node, list):
            for item in node:
                traverse(item)
            return
        if not isinstance(node, tuple):
            return
        
        node_type = node[0]
        
        if node_type == 'program':
            traverse(node[1])  # Processar statement_list
        elif node_type == 'assign':
            var_name = node[1]
            expr_result = traverse(node[2])
            tac.append(('=', expr_result, None, var_name))
            symbol_table[var_name] = {'type': infer_type(node[2]), 'scope': 'global'}
            return var_name
        elif node_type == 'print':
            expr_result = traverse(node[1])
            tac.append(('print', expr_result, None, None))
            return None
        elif node_type in ('+', '-', '*', '/'):
            left_result = traverse(node[1])
            right_result = traverse(node[2])
            temp = new_temp()
            tac.append((node_type, left_result, right_result, temp))
            return temp
        elif node_type == 'num':
            return node[1]  # Retorna o valor numérico diretamente
        elif node_type == 'id':
            var_name = node[1]
            if var_name not in symbol_table:
                print(f"Warning: Variable '{var_name}' used before assignment")
            return var_name
        return None

    traverse(ast)
    return tac

# Regras do parser
def p_program(p):
    '''program : statement_list'''
    p[0] = ('program', p[1], {'scope': 'global'})

def p_stmt_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_stmt_assign(p):
    '''statement : ID EQUALS expression SEMICOLON'''
    var_name = p[1]
    expr = p[3]
    expr_type = infer_type(expr)
    symbol_table[var_name] = {'type': expr_type, 'scope': 'global'}
    p[0] = ('assign', var_name, expr, {'type': expr_type, 'scope': 'global'})

def p_stmt_print(p):
    '''statement : PRINT LPAREN expression RPAREN SEMICOLON'''
    expr = p[3]
    expr_type = infer_type(expr)
    p[0] = ('print', expr, {'type': expr_type, 'scope': 'global'})

def p_expr_term(p):
    '''expression : term'''
    p[0] = p[1]

def p_term_muldiv(p):
    '''term : term TIMES factor
            | term DIVIDE factor'''
    left_type = infer_type(p[1])
    right_type = infer_type(p[3])
    result_type = 'int' if left_type == 'int' and right_type == 'int' else 'unknown'
    p[0] = (p[2], p[1], p[3], {'type': result_type})

def p_term_factor(p):
    '''term : factor'''
    p[0] = p[1]

def p_factor_num(p):
    '''factor : NUMBER'''
    p[0] = ('num', p[1], {'type': 'int'})

def p_factor_id(p):
    '''factor : ID'''
    var_name = p[1]
    var_type = symbol_table.get(var_name, {}).get('type', 'unknown')
    if var_type == 'unknown':
        print(f"Warning: Variable '{var_name}' used before assignment")
    p[0] = ('id', var_name, {'type': var_type, 'scope': 'global'})

def p_factor_expr(p):
    '''factor : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_expr_addsub(p):
    '''expression : expression PLUS term
                  | expression MINUS term'''
    left_type = infer_type(p[1])
    right_type = infer_type(p[3])
    result_type = 'int' if left_type == 'int' and right_type == 'int' else 'unknown'
    p[0] = (p[2], p[1], p[3], {'type': result_type})

def p_error(p):
    if p:
        print(f"Erro de sintaxe em '{p.value}'")
    else:
        print("Erro de sintaxe no final do arquivo")

# Função para pretty-print do TAC
def print_tac(tac):
    for instr in tac:
        op, arg1, arg2, result = instr
        if op == 'print':
            print(f"print {arg1}")
        elif op == '=':
            print(f"{result} = {arg1}")
        else:
            print(f"{result} = {arg1} {op} {arg2}")

# Inicializa o parser
parser = yacc.yacc()

# Exemplo de uso
if __name__ == "__main__":
    with open("../tests/code.txt") as f:
        code = f.read()
    ast = parser.parse(code)
    tac = generate_tac(ast)
    print("Código TAC gerado:")
    print_tac(tac)