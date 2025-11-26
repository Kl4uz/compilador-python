"""
Gerador de IR (Código Intermediário)
Converte AST em TAC (Three-Address Code)
"""
from ..ast.ast_builder import *
from .ir import IRProgram

class IRGenerator:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.ir_program = IRProgram()
        self.temp_counter = 0
    
    def new_temp(self):
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp
    
    def generate(self, ast_node):
        self.visit(ast_node)
        return self.ir_program
    
    def visit(self, node):
        if node is None:
            return None
        method_name = f'visit_{node.node_type}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        raise NotImplementedError(f"Visitante não implementado: {node.node_type}")
    
    def visit_program(self, node):
        for decl in node.declarations:
            self.visit(decl)
    
    def visit_function(self, node):
        self.ir_program.emit('begin_func', node.name)
        for stmt in node.body:
            self.visit(stmt)
        self.ir_program.emit('end_func', node.name)
    
    def visit_decl_assign(self, node):
        value_result = self.visit(node.value)
        self.ir_program.emit('assign', value_result, None, node.name)
    
    def visit_assign(self, node):
        value_result = self.visit(node.value)
        self.ir_program.emit('assign', value_result, None, node.name)
    
    def visit_return(self, node):
        if node.value:
            result = self.visit(node.value)
            self.ir_program.emit('return', result)
        else:
            self.ir_program.emit('return')
    
    def visit_print(self, node):
        result = self.visit(node.value)
        self.ir_program.emit('print', result)
    
    def visit_binop(self, node):
        left_result = self.visit(node.left)
        right_result = self.visit(node.right)
        temp = self.new_temp()
        self.ir_program.emit(node.op, left_result, right_result, temp)
        return temp
    
    def visit_number(self, node):
        return str(node.value)
    
    def visit_id(self, node):
        return node.name
    
    def visit_call(self, node):
        arg_results = []
        for arg in node.args:
            arg_result = self.visit(arg)
            self.ir_program.emit('param', arg_result)
            arg_results.append(arg_result)
        
        temp = self.new_temp()
        self.ir_program.emit('call', node.name, arg_results, temp)
        return temp