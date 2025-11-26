"""
Gerador de Código Intermediário com Suporte a Funções
Integrado com Tabela de Símbolos e Ambientes de Execução
"""

import ply.yacc as yacc
from lexer import tokens, lexer
from symbol_table import SymbolTable

# Tabela de símbolos global
symbol_table = SymbolTable()

# Precedência dos operadores
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'EQUALS'),
)

# Contador para variáveis temporárias e labels
temp_count = 0
label_count = 0

def new_temp():
    global temp_count
    temp_count += 1
    return f't{temp_count}'

def new_label():
    global label_count
    label_count += 1
    return f'L{label_count}'

# ===== REGRAS DA GRAMÁTICA =====

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
    '''declaration : function_declaration'''
    p[0] = p[1]

def p_function_declaration(p):
    '''function_declaration : INT ID LPAREN parameter_list RPAREN LBRACE statement_list RBRACE
                            | INT ID LPAREN RPAREN LBRACE statement_list RBRACE'''
    func_name = p[2]
    
    if len(p) == 9:
        params = p[4]
        body = p[7]
    else:
        params = []
        body = p[6]
    
    p[0] = ('function', func_name, params, body)

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
        p[0] = ('call', p[1], p[3])
    else:
        p[0] = ('call', p[1], [])

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
        print(f"Erro de sintaxe em '{p.value}'")
    else:
        print("Erro de sintaxe no final do arquivo")

# ===== GERAÇÃO DE CÓDIGO TAC =====

class TACGenerator:
    def __init__(self):
        self.code = []
        self.symbol_table = SymbolTable()
    
    def generate(self, ast):
        """Gera código TAC a partir da AST"""
        self.traverse(ast)
        return self.code
    
    def emit(self, instruction):
        """Emite uma instrução TAC"""
        self.code.append(instruction)
    
    def traverse(self, node):
        """Percorre a AST recursivamente"""
        if isinstance(node, list):
            for item in node:
                self.traverse(item)
            return None
        
        if not isinstance(node, tuple):
            return None
        
        node_type = node[0]
        
        if node_type == 'program':
            return self.traverse(node[1])
        
        elif node_type == 'function':
            func_name = node[1]
            params = node[2]
            body = node[3]
            
            # Emite label da função
            self.emit(f"FUNCTION {func_name}:")
            
            # Entra no escopo da função
            self.symbol_table.enter_scope(func_name)
            
            # Emite código para começar função
            self.emit("BEGIN_FUNC")
            
            # Processa parâmetros
            for param in params:
                param_name = param[1]
                param_type = param[2]
                self.symbol_table.insert(param_name, param_type, is_param=True)
                self.emit(f"PARAM {param_name}")
            
            # Processa corpo da função
            self.traverse(body)
            
            # Emite código para terminar função
            self.emit("END_FUNC")
            self.emit("")  # Linha em branco
            
            # Sai do escopo da função
            self.symbol_table.exit_scope()
            return None
        
        elif node_type == 'assign':
            var_name = node[1]
            expr = node[2]
            
            # Gera código para a expressão
            result = self.traverse(expr)
            
            # Emite atribuição
            self.emit(f"{var_name} = {result}")
            
            # Adiciona à tabela de símbolos se não existir
            if not self.symbol_table.lookup(var_name):
                self.symbol_table.insert(var_name, 'int')
            
            return var_name
        
        elif node_type == 'return':
            expr = node[1]
            if expr:
                result = self.traverse(expr)
                self.emit(f"RETURN {result}")
            else:
                self.emit("RETURN")
            return None
        
        elif node_type == 'print':
            expr = node[1]
            result = self.traverse(expr)
            self.emit(f"PRINT {result}")
            return None
        
        elif node_type == 'call':
            func_name = node[1]
            args = node[2]
            
            # Emite código para argumentos
            for arg in args:
                arg_result = self.traverse(arg)
                self.emit(f"ARG {arg_result}")
            
            # Emite chamada
            temp = new_temp()
            self.emit(f"{temp} = CALL {func_name}, {len(args)}")
            return temp
        
        elif node_type in ('+', '-', '*', '/'):
            left = self.traverse(node[1])
            right = self.traverse(node[2])
            temp = new_temp()
            self.emit(f"{temp} = {left} {node_type} {right}")
            return temp
        
        elif node_type == 'num':
            return str(node[1])
        
        elif node_type == 'id':
            var_name = node[1]
            # Verifica se variável existe
            if not self.symbol_table.lookup(var_name):
                print(f"Warning: Variável '{var_name}' usada antes de ser declarada")
            return var_name
        
        return None
    
    def print_code(self):
        """Imprime o código TAC gerado"""
        print("\n=== CÓDIGO INTERMEDIÁRIO (TAC) ===")
        for instr in self.code:
            print(instr)
        print("===================================\n")

# Inicializa o parser
parser = yacc.yacc()

# Exemplo de uso
if __name__ == "__main__":
    code = """
int soma(int a, int b) {
    int r = a + b;
    return r;
}

int main() {
    int x = soma(2, 3);
    print(x);
    return 0;
}
"""
    
    print("=== CÓDIGO FONTE ===")
    print(code)
    print("====================\n")
    
    # Parse
    ast = parser.parse(code, lexer=lexer)
    print("AST gerada:", ast)
    print()
    
    # Gera TAC
    generator = TACGenerator()
    tac = generator.generate(ast)
    generator.print_code()
    
    # Imprime tabela de símbolos
    generator.symbol_table.print_table()
