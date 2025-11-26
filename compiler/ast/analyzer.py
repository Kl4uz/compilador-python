"""
Analisador Semântico - Fase 3 do Compilador
Verifica tipos, escopo, declarações e uso de variáveis
"""
from .ast_builder import *
from .symbol_table import SymbolTable

class SemanticAnalyzer:
    """Analisador semântico com verificação de tipos e escopos"""
    
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors = []
        self.current_function = None
    
    def analyze(self, ast_node):
        """
        Faz análise semântica completa na AST
        Retorna: (success, errors, symbol_table)
        """
        self.errors = []
        self.visit(ast_node)
        
        success = len(self.errors) == 0
        return success, self.errors, self.symbol_table
    
    def error(self, message):
        """Registra erro semântico"""
        self.errors.append(message)
    
    def visit(self, node):
        """Despacha visita para método específico do nó"""
        if node is None:
            return None
        
        method_name = f'visit_{node.node_type}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        """Visitante genérico para nós desconhecidos"""
        self.error(f"Tipo de nó não suportado: {node.node_type}")
        return None
    
    # ===== VISITANTES =====
    
    def visit_program(self, node):
        """Visita programa raiz"""
        for decl in node.declarations:
            self.visit(decl)
    
    def visit_function(self, node):
        """Visita declaração de função"""
        # Verifica se função já existe
        if self.symbol_table.lookup(node.name, current_scope_only=True):
            self.error(f"Função '{node.name}' já declarada")
            return
        
        # Adiciona função à tabela
        self.symbol_table.insert(node.name, 'function', params=node.params)
        
        # Entra no escopo da função
        self.symbol_table.enter_scope(node.name)
        self.current_function = node.name
        
        # Adiciona parâmetros ao escopo
        for param in node.params:
            param_name = param.name
            param_type = param.param_type
            
            if self.symbol_table.lookup(param_name, current_scope_only=True):
                self.error(f"Parâmetro '{param_name}' duplicado na função '{node.name}'")
            else:
                self.symbol_table.insert(param_name, param_type, is_param=True)
        
        # Visita corpo da função
        has_return = False
        for stmt in node.body:
            self.visit(stmt)
            if isinstance(stmt, ReturnNode):
                has_return = True
        
        # Verifica se tem return
        if not has_return:
            self.error(f"Função '{node.name}' deve ter declaração 'return'")
        
        # Sai do escopo
        self.symbol_table.exit_scope()
        self.current_function = None
    
    def visit_decl_assign(self, node):
        """Visita declaração com atribuição"""
        # Verifica se variável já existe no escopo atual
        if self.symbol_table.lookup(node.name, current_scope_only=True):
            self.error(f"Variável '{node.name}' já declarada neste escopo")
            return
        
        # Infere tipo da expressão
        value_type = self.visit(node.value)
        
        # Adiciona variável à tabela
        self.symbol_table.insert(node.name, value_type or 'int')
    
    def visit_assign(self, node):
        """Visita atribuição"""
        # Verifica se variável existe
        symbol = self.symbol_table.lookup(node.name)
        if not symbol:
            self.error(f"Variável '{node.name}' não declarada")
            return
        
        # Verifica tipo da expressão
        value_type = self.visit(node.value)
        if value_type and value_type != symbol['type']:
            self.error(f"Tipo incompatível: '{node.name}' é '{symbol['type']}', mas recebe '{value_type}'")
    
    def visit_return(self, node):
        """Visita retorno"""
        if not self.current_function:
            self.error("'return' fora de função")
            return
        
        if node.value:
            return self.visit(node.value)
        return None
    
    def visit_print(self, node):
        """Visita print"""
        return self.visit(node.value)
    
    def visit_binop(self, node):
        """Visita operação binária"""
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        
        # Verifica compatibilidade de tipos
        if left_type and right_type and left_type != right_type:
            self.error(f"Tipos incompatíveis na operação '{node.op}': {left_type} e {right_type}")
        
        return left_type or right_type or 'int'
    
    def visit_number(self, node):
        """Visita número literal"""
        return 'int'
    
    def visit_id(self, node):
        """Visita identificador"""
        symbol = self.symbol_table.lookup(node.name)
        if not symbol:
            self.error(f"Variável '{node.name}' não declarada")
            return None
        
        return symbol['type']
    
    def visit_call(self, node):
        """Visita chamada de função"""
        # Verifica se função existe
        symbol = self.symbol_table.lookup(node.name)
        if not symbol:
            self.error(f"Função '{node.name}' não declarada")
            return 'int'
        
        if symbol['type'] != 'function':
            self.error(f"'{node.name}' não é uma função")
            return 'int'
        
        # Verifica número de argumentos
        expected_params = len(symbol.get('params', []))
        actual_args = len(node.args)
        
        if expected_params != actual_args:
            self.error(f"Função '{node.name}' espera {expected_params} argumentos, mas recebeu {actual_args}")
        
        # Verifica tipo dos argumentos
        for i, arg in enumerate(node.args):
            arg_type = self.visit(arg)
            if i < expected_params:
                param = symbol['params'][i]
                if arg_type and arg_type != param.param_type:
                    self.error(f"Argumento {i+1} de '{node.name}': esperado '{param.param_type}', recebido '{arg_type}'")
        
        return 'int'  # Assumindo retorno int


# Para testes
if __name__ == "__main__":
    from parser import parse_from_code
    from ast import build_ast
    
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
    
    print("=== TESTE DO ANALISADOR SEMÂNTICO ===")
    print("Código:")
    print(test_code)
    
    parse_tree = parse_from_code(test_code)
    ast = build_ast(parse_tree)
    
    analyzer = SemanticAnalyzer()
    success, errors, symbol_table = analyzer.analyze(ast)
    
    print(f"\nResultado: {'✓ Sem erros' if success else '✗ Com erros'}")
    
    if errors:
        print("\nErros encontrados:")
        for error in errors:
            print(f"  - {error}")
    
    print("\nTabela de Símbolos:")
    symbol_table.print_table()
