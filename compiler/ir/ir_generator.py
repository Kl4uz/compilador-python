"""
Gerador de Código Intermediário (IR Generator)
Converte AST em código TAC (Three-Address Code)
"""
from ..ast.ast_builder import *
from .ir import IRProgram, TAC


class IRGenerator:
    """Gerador de código intermediário"""
    
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.ir_program = IRProgram()
        self.temp_counter = 0
        self.label_counter = 0
    
    def new_temp(self):
        """Gera um novo temporário"""
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp
    
    def new_label(self):
        """Gera um novo rótulo"""
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label
    
    def generate(self, ast_node):
        """
        Gera código intermediário a partir da AST
        Retorna: IRProgram
        """
        self.visit(ast_node)
        return self.ir_program
    
    def visit(self, node):
        """Despacha visita para método específico do nó"""
        if node is None:
            return None
        
        method_name = f'visit_{node.node_type}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        """Visitante genérico"""
        raise NotImplementedError(f"Visitante não implementado para: {node.node_type}")
    
    # ===== VISITANTES =====
    
    def visit_program(self, node):
        """Visita programa raiz"""
        for decl in node.declarations:
            self.visit(decl)
    
    def visit_function(self, node):
        """Visita declaração de função"""
        # Marca início da função
        self.ir_program.emit('begin_func', node.name)
        
        # Parâmetros (já estão na tabela de símbolos)
        # Não precisa emitir instruções para params, a runtime vai cuidar
        
        # Corpo da função
        for stmt in node.body:
            self.visit(stmt)
        
        # Marca fim da função
        self.ir_program.emit('end_func', node.name)
    
    def visit_decl_assign(self, node):
        """Visita declaração com atribuição"""
        # Avalia a expressão
        value_result = self.visit(node.value)
        
        # Atribui ao identificador
        self.ir_program.emit('assign', value_result, None, node.name)
    
    def visit_assign(self, node):
        """Visita atribuição"""
        # Avalia a expressão
        value_result = self.visit(node.value)
        
        # Atribui ao identificador
        self.ir_program.emit('assign', value_result, None, node.name)
    
    def visit_return(self, node):
        """Visita retorno"""
        if node.value:
            result = self.visit(node.value)
            self.ir_program.emit('return', result)
        else:
            self.ir_program.emit('return')
    
    def visit_print(self, node):
        """Visita print"""
        result = self.visit(node.value)
        self.ir_program.emit('print', result)
    
    def visit_binop(self, node):
        """Visita operação binária"""
        # Avalia operandos
        left_result = self.visit(node.left)
        right_result = self.visit(node.right)
        
        # Gera temporário para resultado
        temp = self.new_temp()
        
        # Emite operação
        self.ir_program.emit(node.op, left_result, right_result, temp)
        
        return temp
    
    def visit_number(self, node):
        """Visita número literal"""
        return str(node.value)
    
    def visit_id(self, node):
        """Visita identificador"""
        return node.name
    
    def visit_call(self, node):
        """Visita chamada de função"""
        # Emite param para cada argumento
        arg_results = []
        for arg in node.args:
            arg_result = self.visit(arg)
            self.ir_program.emit('param', arg_result)
            arg_results.append(arg_result)
        
        # Gera temporário para resultado da chamada
        temp = self.new_temp()
        
        # Emite call
        self.ir_program.emit('call', node.name, arg_results, temp)
        
        return temp


# Para testes
if __name__ == "__main__":
    from parser import parse_from_code
    from ast import build_ast
    from symbol_table import SymbolTable
    from analyzer import SemanticAnalyzer
    
    test_code = """
    int soma(int a, int b) {
        int r = a + b;
        return r;
    }
    
    int main() {
        int x = 5;
        int y = soma(x, 3);
        print(y);
        return 0;
    }
    """
    
    print("=== TESTE DO GERADOR DE IR ===")
    print("Código:")
    print(test_code)
    
    # Parse
    parse_tree = parse_from_code(test_code)
    ast = build_ast(parse_tree)
    
    # Análise semântica
    analyzer = SemanticAnalyzer()
    success, errors, symbol_table = analyzer.analyze(ast)
    
    if not success:
        print("Erros semânticos encontrados:")
        for error in errors:
            print(f"  - {error}")
    else:
        # Geração de IR
        ir_gen = IRGenerator(symbol_table)
        ir_program = ir_gen.generate(ast)
        
        print("\nCódigo Intermediário (TAC):")
        ir_program.print_code()
