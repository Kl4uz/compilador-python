"""
Analisador Semântico
Verifica tipos, escopos e declarações
"""
from .ast_builder import *
from .symbol_table import SymbolTable

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors = []
        self.current_function = None
    
    def analyze(self, ast_node):
        """Retorna: (success, errors, symbol_table)"""
        self.errors = []
        self.visit(ast_node)
        return len(self.errors) == 0, self.errors, self.symbol_table
    
    def error(self, message):
        self.errors.append(message)
    
    def visit(self, node):
        if node is None:
            return None
        method_name = f'visit_{node.node_type}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        self.error(f"Tipo de nó não suportado: {node.node_type}")
        return None
    
    def visit_program(self, node):
        for decl in node.declarations:
            self.visit(decl)
    
    def visit_function(self, node):
        if self.symbol_table.lookup(node.name, current_scope_only=True):
            self.error(f"Função '{node.name}' já declarada")
            return
        
        self.symbol_table.insert(node.name, 'function', params=node.params)
        self.symbol_table.enter_scope(node.name)
        self.current_function = node.name
        
        for param in node.params:
            if self.symbol_table.lookup(param.name, current_scope_only=True):
                self.error(f"Parâmetro '{param.name}' duplicado")
            else:
                self.symbol_table.insert(param.name, param.param_type, is_param=True)
        
        has_return = False
        for stmt in node.body:
            self.visit(stmt)
            if isinstance(stmt, ReturnNode):
                has_return = True
        
        if not has_return:
            self.error(f"Função '{node.name}' precisa de 'return'")
        
        self.symbol_table.exit_scope()
        self.current_function = None
    
    def visit_decl_assign(self, node):
        if self.symbol_table.lookup(node.name, current_scope_only=True):
            self.error(f"Variável '{node.name}' já declarada")
            return
        value_type = self.visit(node.value)
        self.symbol_table.insert(node.name, value_type or 'int')
    
    def visit_assign(self, node):
        symbol = self.symbol_table.lookup(node.name)
        if not symbol:
            self.error(f"Variável '{node.name}' não declarada")
            return
        value_type = self.visit(node.value)
        if value_type and value_type != symbol['type']:
            self.error(f"Tipo incompatível em '{node.name}'")
    
    def visit_return(self, node):
        if not self.current_function:
            self.error("'return' fora de função")
            return
        if node.value:
            return self.visit(node.value)
        return None
    
    def visit_print(self, node):
        return self.visit(node.value)
    
    def visit_binop(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        if left_type and right_type and left_type != right_type:
            self.error(f"Tipos incompatíveis: {left_type} e {right_type}")
        return left_type or right_type or 'int'
    
    def visit_number(self, node):
        return 'int'
    
    def visit_id(self, node):
        symbol = self.symbol_table.lookup(node.name)
        if not symbol:
            self.error(f"Variável '{node.name}' não declarada")
            return None
        return symbol['type']
    
    def visit_call(self, node):
        symbol = self.symbol_table.lookup(node.name)
        if not symbol:
            self.error(f"Função '{node.name}' não declarada")
            return 'int'
        
        if symbol['type'] != 'function':
            self.error(f"'{node.name}' não é função")
            return 'int'
        
        expected = len(symbol.get('params', []))
        actual = len(node.args)
        if expected != actual:
            self.error(f"'{node.name}' espera {expected} argumentos, recebeu {actual}")
        
        for i, arg in enumerate(node.args):
            arg_type = self.visit(arg)
            if i < expected:
                param = symbol['params'][i]
                if arg_type and arg_type != param.param_type:
                    self.error(f"Argumento {i+1}: esperado '{param.param_type}', recebido '{arg_type}'")
        
        return 'int'
    
    def visit_if(self, node):
        cond_type = self.visit(node.condition)
        if cond_type != 'int':
            self.error("Condição do IF deve ser do tipo int")

        for stmt in node.then_block:
            self.visit(stmt)

        if node.else_block:
            for stmt in node.else_block:
                self.visit(stmt)

    def visit_while(self, node):
        cond_type = self.visit(node.condition)
        if cond_type != 'int':
            self.error("Condição do WHILE deve ser do tipo int")

        for stmt in node.body:
            self.visit(stmt)
    def visit_for(self, node):
        self.visit(node.init)

        cond_type = self.visit(node.condition)
        if cond_type != 'int':
            self.error("Condição do for deve ser int")

        for stmt in node.body:
            self.visit(stmt)

        self.visit(node.increment)

