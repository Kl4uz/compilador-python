"""
Analisador Semântico
Realiza verificação de tipos, escopos e outras análises semânticas
"""

from typing import List, Optional
from .ast_builder import ASTNode
from .symbol_table import SymbolTable, Symbol


class SemanticAnalyzer:
    """
    Analisador Semântico
    Verifica tipos, escopos, declarações, etc.
    """
    
    def __init__(self, symbol_table: SymbolTable):
        self.symbol_table = symbol_table
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.current_function: Optional[str] = None
    
    def analyze(self, ast: ASTNode) -> bool:
        """
        Realiza análise semântica completa da AST
        Retorna True se não houver erros, False caso contrário
        """
        if ast is None:
            self.errors.append("AST vazia")
            return False
        
        self.errors = []
        self.warnings = []
        
        self._analyze_node(ast)
        
        return len(self.errors) == 0
    
    def _analyze_node(self, node: ASTNode):
        """Analisa um nó da AST recursivamente"""
        if node is None:
            return
        
        node_type = node.type
        
        if node_type == "program":
            self._analyze_program(node)
        elif node_type == "function":
            self._analyze_function(node)
        elif node_type == "parameter":
            self._analyze_parameter(node)
        elif node_type == "variable_declaration":
            self._analyze_variable_declaration(node)
        elif node_type == "assignment":
            self._analyze_assignment(node)
        elif node_type == "binary_operation":
            self._analyze_binary_operation(node)
        elif node_type == "function_call":
            self._analyze_function_call(node)
        elif node_type == "return":
            self._analyze_return(node)
        elif node_type == "print":
            self._analyze_print(node)
        elif node_type == "if":
            self._analyze_if(node)
        elif node_type == "while":
            self._analyze_while(node)
        else:
            # Analisa filhos recursivamente
            for child in node.children:
                self._analyze_node(child)
    
    def _analyze_program(self, node: ASTNode):
        """Analisa o nó de programa"""
        # Verifica se há função main
        has_main = False
        for child in node.children:
            if child.type == "function" and child.value == "main":
                has_main = True
                break
        
        if not has_main:
            self.warnings.append("Função 'main' não encontrada")
        
        # Analisa todas as declarações
        for child in node.children:
            self._analyze_node(child)
    
    def _analyze_function(self, node: ASTNode):
        """Analisa uma declaração de função"""
        func_name = node.value
        
        # Verifica se função já foi declarada
        existing = self.symbol_table.lookup(func_name)
        if existing and existing.scope == self.symbol_table.get_current_scope_name():
            self.errors.append(f"Função '{func_name}' já declarada")
            return
        
        # Entra no escopo da função
        self.symbol_table.enter_scope(func_name)
        self.current_function = func_name
        
        # Analisa parâmetros
        params = []
        for child in node.children:
            if child.type == "parameter":
                self._analyze_parameter(child)
                params.append(child.value)
        
        # Verifica parâmetros duplicados
        if len(params) != len(set(params)):
            self.errors.append(f"Parâmetros duplicados na função '{func_name}'")
        
        # Analisa corpo da função
        for child in node.children:
            if child.type != "parameter":
                self._analyze_node(child)
        
        # Sai do escopo
        self.symbol_table.exit_scope()
        self.current_function = None
    
    def _analyze_parameter(self, node: ASTNode):
        """Analisa um parâmetro de função"""
        param_name = node.value
        param_type = node.attributes.get("param_type", "int")
        
        # Insere na tabela de símbolos
        try:
            self.symbol_table.insert(param_name, param_type, is_param=True)
        except Exception as e:
            self.errors.append(str(e))
    
    def _analyze_variable_declaration(self, node: ASTNode):
        """Analisa uma declaração de variável"""
        var_name = node.value
        var_type = node.attributes.get("var_type", "int")
        
        # Verifica se variável já foi declarada no escopo atual
        existing = self.symbol_table.lookup_local(var_name)
        if existing:
            self.errors.append(f"Variável '{var_name}' já declarada no escopo atual")
            return
        
        # Insere na tabela de símbolos
        try:
            self.symbol_table.insert(var_name, var_type)
        except Exception as e:
            self.errors.append(str(e))
        
        # Analisa inicializador se houver
        if node.children:
            init_expr = node.children[0]
            init_type = self._infer_type(init_expr)
            
            if init_type != var_type and init_type != "unknown":
                self.warnings.append(
                    f"Tipo do inicializador ({init_type}) não corresponde ao tipo da variável ({var_type})"
                )
    
    def _analyze_assignment(self, node: ASTNode):
        """Analisa uma atribuição"""
        var_name = node.value
        
        # Verifica se variável foi declarada
        symbol = self.symbol_table.lookup(var_name)
        if not symbol:
            self.errors.append(f"Variável '{var_name}' não foi declarada")
            return
        
        # Analisa expressão
        if node.children:
            expr = node.children[0]
            expr_type = self._infer_type(expr)
            
            if expr_type != symbol.type and expr_type != "unknown":
                self.warnings.append(
                    f"Tipo da expressão ({expr_type}) não corresponde ao tipo da variável ({symbol.type})"
                )
    
    def _analyze_binary_operation(self, node: ASTNode):
        """Analisa uma operação binária"""
        operator = node.value
        
        if len(node.children) < 2:
            self.errors.append(f"Operação binária '{operator}' requer dois operandos")
            return
        
        left = node.children[0]
        right = node.children[1]
        
        left_type = self._infer_type(left)
        right_type = self._infer_type(right)
        
        # Verifica tipos compatíveis
        if left_type != right_type and left_type != "unknown" and right_type != "unknown":
            self.warnings.append(
                f"Tipos incompatíveis na operação '{operator}': {left_type} e {right_type}"
            )
        
        # Verifica divisão por zero (constante)
        if operator == "/":
            if right.type == "number" and right.value == 0:
                self.errors.append("Divisão por zero detectada")
    
    def _analyze_function_call(self, node: ASTNode):
        """Analisa uma chamada de função"""
        func_name = node.value
        
        # Verifica se função existe
        symbol = self.symbol_table.lookup(func_name)
        if not symbol:
            self.errors.append(f"Função '{func_name}' não foi declarada")
            return
        
        # Analisa argumentos
        args = node.children
        # TODO: Verificar número e tipos de argumentos
        for arg in args:
            self._analyze_node(arg)
    
    def _analyze_return(self, node: ASTNode):
        """Analisa um retorno"""
        if not self.current_function:
            self.errors.append("Return fora de função")
            return
        
        # Analisa expressão de retorno se houver
        if node.children:
            self._analyze_node(node.children[0])
    
    def _analyze_print(self, node: ASTNode):
        """Analisa um print"""
        if node.children:
            self._analyze_node(node.children[0])
    
    def _analyze_if(self, node: ASTNode):
        """Analisa um if"""
        if not node.children:
            self.errors.append("If sem condição")
            return
        
        # Analisa condição
        condition = node.children[0]
        cond_type = self._infer_type(condition)
        
        if cond_type not in ("int", "unknown"):
            self.warnings.append(f"Condição do if deve ser do tipo int, encontrado: {cond_type}")
        
        # Analisa corpos
        for child in node.children[1:]:
            self._analyze_node(child)
    
    def _analyze_while(self, node: ASTNode):
        """Analisa um while"""
        if not node.children:
            self.errors.append("While sem condição")
            return
        
        # Analisa condição
        condition = node.children[0]
        cond_type = self._infer_type(condition)
        
        if cond_type not in ("int", "unknown"):
            self.warnings.append(f"Condição do while deve ser do tipo int, encontrado: {cond_type}")
        
        # Analisa corpo
        if len(node.children) > 1:
            self._analyze_node(node.children[1])
    
    def _infer_type(self, node: ASTNode) -> str:
        """
        Infere o tipo de uma expressão
        Retorna o tipo inferido ou "unknown" se não for possível determinar
        """
        if node is None:
            return "unknown"
        
        node_type = node.type
        
        if node_type == "number":
            return "int"
        elif node_type == "identifier":
            var_name = node.value
            symbol = self.symbol_table.lookup(var_name)
            if symbol:
                return symbol.type
            return "unknown"
        elif node_type == "binary_operation":
            operator = node.value
            if len(node.children) >= 2:
                left_type = self._infer_type(node.children[0])
                right_type = self._infer_type(node.children[1])
                
                # Operações aritméticas retornam int se ambos operandos são int
                if operator in ("+", "-", "*", "/"):
                    if left_type == "int" and right_type == "int":
                        return "int"
                
                # Operações de comparação retornam int (boolean como int)
                elif operator in ("==", "!=", "<", ">", "<=", ">="):
                    return "int"
            
            return "unknown"
        elif node_type == "function_call":
            func_name = node.value
            symbol = self.symbol_table.lookup(func_name)
            if symbol:
                # Assume que funções retornam int por padrão
                return "int"
            return "unknown"
        else:
            return "unknown"

