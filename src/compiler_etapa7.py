"""
Sistema Completo de Compilação - Etapa 7
Compilador + Gerador de TAC + Interpretador Integrado
"""

from lexer import lexer
from symbol_table import SymbolTable
from runtime import ActivationRecord, RuntimeStack
import ply.yacc as yacc

# Importa tokens do lexer
from lexer import tokens

# Precedência dos operadores
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'EQUALS'),
)

# Contador para variáveis temporárias
temp_count = 0

def new_temp():
    global temp_count
    temp_count += 1
    return f't{temp_count}'

# ===== GRAMÁTICA =====

def p_program(p):
    '''program : func_list'''
    p[0] = ('program', p[1])

def p_func_list(p):
    '''func_list : func_list function
                 | function'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_function(p):
    '''function : INT ID LPAREN params RPAREN LBRACE stmts RBRACE
                | INT ID LPAREN RPAREN LBRACE stmts RBRACE'''
    if len(p) == 9:
        p[0] = ('func', p[2], p[4], p[7])
    else:
        p[0] = ('func', p[2], [], p[6])

def p_params(p):
    '''params : params COMMA INT ID
              | INT ID'''
    if len(p) == 5:
        p[0] = p[1] + [p[4]]
    else:
        p[0] = [p[2]]

def p_stmts(p):
    '''stmts : stmts stmt
             | stmt'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_stmt_decl_assign(p):
    '''stmt : INT ID EQUALS expr SEMICOLON'''
    p[0] = ('decl_assign', p[2], p[4])

def p_stmt_assign(p):
    '''stmt : ID EQUALS expr SEMICOLON'''
    p[0] = ('assign', p[1], p[3])

def p_stmt_return(p):
    '''stmt : RETURN expr SEMICOLON
            | RETURN SEMICOLON'''
    if len(p) == 4:
        p[0] = ('return', p[2])
    else:
        p[0] = ('return', None)

def p_stmt_print(p):
    '''stmt : PRINT LPAREN expr RPAREN SEMICOLON'''
    p[0] = ('print', p[3])

def p_expr_binop(p):
    '''expr : expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
            | expr DIVIDE expr'''
    p[0] = (p[2], p[1], p[3])

def p_expr_num(p):
    '''expr : NUMBER'''
    p[0] = ('num', p[1])

def p_expr_id(p):
    '''expr : ID'''
    p[0] = ('id', p[1])

def p_expr_call(p):
    '''expr : ID LPAREN args RPAREN
            | ID LPAREN RPAREN'''
    if len(p) == 5:
        p[0] = ('call', p[1], p[3])
    else:
        p[0] = ('call', p[1], [])

def p_args(p):
    '''args : args COMMA expr
            | expr'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_expr_paren(p):
    '''expr : LPAREN expr RPAREN'''
    p[0] = p[2]

def p_error(p):
    if p:
        print(f"Erro de sintaxe: '{p.value}' (linha {p.lineno})")
    else:
        print("Erro de sintaxe: fim de arquivo inesperado")

# Cria o parser
parser = yacc.yacc()

# ===== GERADOR DE CÓDIGO TAC =====

class Compiler:
    def __init__(self):
        self.tac = []
        self.symbol_table = SymbolTable()
        global temp_count
        temp_count = 0
    
    def compile(self, ast):
        """Compila a AST e gera código TAC"""
        self._process(ast)
        return self.tac
    
    def _emit(self, instr):
        self.tac.append(instr)
    
    def _process(self, node):
        if isinstance(node, list):
            for item in node:
                self._process(item)
            return None
        
        if not isinstance(node, tuple):
            return None
        
        node_type = node[0]
        
        if node_type == 'program':
            self._process(node[1])
        
        elif node_type == 'func':
            func_name = node[1]
            params = node[2]
            body = node[3]
            
            self._emit(f"FUNCTION {func_name}:")
            self._emit("BEGIN_FUNC")
            
            self.symbol_table.enter_scope(func_name)
            
            for param in params:
                self.symbol_table.insert(param, 'int', is_param=True)
                self._emit(f"PARAM {param}")
            
            self._process(body)
            
            self._emit("END_FUNC")
            self._emit("")
            
            self.symbol_table.exit_scope()
        
        elif node_type in ('decl_assign', 'assign'):
            var = node[1]
            expr = node[2]
            result = self._process(expr)
            self._emit(f"{var} = {result}")
            if not self.symbol_table.lookup(var):
                self.symbol_table.insert(var, 'int')
            return var
        
        elif node_type == 'return':
            if node[1]:
                result = self._process(node[1])
                self._emit(f"RETURN {result}")
            else:
                self._emit("RETURN")
        
        elif node_type == 'print':
            result = self._process(node[1])
            self._emit(f"PRINT {result}")
        
        elif node_type == 'call':
            func = node[1]
            args = node[2]
            for arg in args:
                arg_result = self._process(arg)
                self._emit(f"ARG {arg_result}")
            temp = new_temp()
            self._emit(f"{temp} = CALL {func}, {len(args)}")
            return temp
        
        elif node_type in ('+', '-', '*', '/'):
            left = self._process(node[1])
            right = self._process(node[2])
            temp = new_temp()
            self._emit(f"{temp} = {left} {node_type} {right}")
            return temp
        
        elif node_type == 'num':
            return str(node[1])
        
        elif node_type == 'id':
            return node[1]
        
        return None

# ===== INTERPRETADOR =====

class Interpreter:
    def __init__(self, tac):
        self.code = tac
        self.runtime = RuntimeStack()
        self.functions = {}
        self._index_functions()
    
    def _index_functions(self):
        for i, instr in enumerate(self.code):
            if instr.startswith("FUNCTION "):
                name = instr.split()[1].rstrip(':')
                self.functions[name] = i
    
    def run(self):
        if 'main' in self.functions:
            self._call('main', [])
        else:
            print("Erro: função 'main' não encontrada")
    
    def _call(self, func, args):
        ar = ActivationRecord(func)
        self.runtime.push(ar)
        
        pc = self.functions[func] + 1
        param_idx = 0
        return_val = None
        
        while pc < len(self.code):
            instr = self.code[pc].strip()
            if not instr:
                pc += 1
                continue
            
            if instr == "BEGIN_FUNC":
                pc += 1
                continue
            
            if instr.startswith("PARAM "):
                param = instr.split()[1]
                if param_idx < len(args):
                    ar.set_parameter(param, args[param_idx])
                    param_idx += 1
                pc += 1
                continue
            
            if instr == "END_FUNC":
                break
            
            if instr.startswith("RETURN"):
                parts = instr.split()
                if len(parts) > 1:
                    return_val = self._get_val(parts[1])
                break
            
            if " = " in instr and " CALL " not in instr:
                var, expr = instr.split(" = ", 1)
                if any(op in expr for op in [" + ", " - ", " * ", " / "]):
                    for op in [" + ", " - ", " * ", " / "]:
                        if op in expr:
                            left, right = expr.split(op)
                            l_val = self._get_val(left.strip())
                            r_val = self._get_val(right.strip())
                            if op.strip() == '+':
                                result = l_val + r_val
                            elif op.strip() == '-':
                                result = l_val - r_val
                            elif op.strip() == '*':
                                result = l_val * r_val
                            elif op.strip() == '/':
                                result = l_val / r_val
                            self.runtime.set_temporary(var, result)
                            break
                else:
                    val = self._get_val(expr)
                    self.runtime.set_value(var, val)
                pc += 1
                continue
            
            if instr.startswith("PRINT "):
                val = self._get_val(instr.split()[1])
                print(f">>> OUTPUT: {val}")
                pc += 1
                continue
            
            if instr.startswith("ARG "):
                pc += 1
                continue
            
            if " CALL " in instr:
                var, call_part = instr.split(" = CALL ")
                called_func, num_args_str = call_part.split(", ")
                num_args = int(num_args_str)
                
                call_args = []
                for i in range(pc - num_args, pc):
                    arg_instr = self.code[i].strip()
                    if arg_instr.startswith("ARG "):
                        call_args.append(self._get_val(arg_instr.split()[1]))
                
                result = self._call(called_func, call_args)
                self.runtime.set_temporary(var, result)
                pc += 1
                continue
            
            pc += 1
        
        ar = self.runtime.pop()
        return return_val if return_val is not None else (ar.return_value if ar.return_value is not None else 0)
    
    def _get_val(self, name):
        try:
            return int(name)
        except:
            return self.runtime.get_value(name)

# ===== TESTE =====

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
    
    print("=" * 50)
    print("CÓDIGO FONTE:")
    print("=" * 50)
    print(code)
    
    print("\n" + "=" * 50)
    print("COMPILAÇÃO:")
    print("=" * 50)
    
    ast = parser.parse(code, lexer=lexer)
    print(f"\nAST: {ast}\n")
    
    compiler = Compiler()
    tac = compiler.compile(ast)
    
    print("\n" + "=" * 50)
    print("CÓDIGO INTERMEDIÁRIO (TAC):")
    print("=" * 50)
    for line in tac:
        if line:
            print(line)
    
    print("\n" + "=" * 50)
    print("TABELA DE SÍMBOLOS:")
    print("=" * 50)
    compiler.symbol_table.print_table()
    
    print("\n" + "=" * 50)
    print("EXECUÇÃO:")
    print("=" * 50)
    interpreter = Interpreter(tac)
    interpreter.run()
    
    print("\n" + "=" * 50)
    print("ESTADO FINAL DA PILHA:")
    print("=" * 50)
    interpreter.runtime.print_stack()
