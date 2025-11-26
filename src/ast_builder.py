"""
Construtor de Árvore de Sintaxe Abstrata (AST)
Fornece classes e métodos para construir e manipular a AST
"""

from typing import List, Optional, Any, Dict


class ASTNode:
    """
    Nó da Árvore de Sintaxe Abstrata
    Representa um elemento sintático do programa
    """
    def __init__(self, node_type: str, value: Any = None, **attributes):
        self.type = node_type
        self.value = value
        self.attributes = attributes  # Metadados (tipo, escopo, etc)
        self.children: List[ASTNode] = []
    
    def add_child(self, child: 'ASTNode') -> 'ASTNode':
        """Adiciona um filho ao nó"""
        if child is not None:
            self.children.append(child)
        return self
    
    def add_children(self, children: List['ASTNode']) -> 'ASTNode':
        """Adiciona múltiplos filhos ao nó"""
        for child in children:
            self.add_child(child)
        return self
    
    def __repr__(self):
        attrs = f", {self.attributes}" if self.attributes else ""
        val = f" ({self.value})" if self.value is not None else ""
        return f"ASTNode({self.type}{val}{attrs})"


class ASTBuilder:
    """
    Construtor de AST
    Fornece métodos para criar nós da AST de forma padronizada
    """
    
    @staticmethod
    def create_program_node(declarations: List[ASTNode]) -> ASTNode:
        """Cria um nó de programa"""
        node = ASTNode("program")
        node.add_children(declarations)
        return node
    
    @staticmethod
    def create_function_node(name: str, parameters: List[ASTNode], 
                           body: List[ASTNode], return_type: str = "int") -> ASTNode:
        """Cria um nó de função"""
        node = ASTNode("function", value=name, return_type=return_type)
        # Parâmetros como filhos
        for param in parameters:
            node.add_child(param)
        # Corpo da função
        for stmt in body:
            node.add_child(stmt)
        return node
    
    @staticmethod
    def create_parameter_node(name: str, param_type: str = "int") -> ASTNode:
        """Cria um nó de parâmetro"""
        return ASTNode("parameter", value=name, param_type=param_type)
    
    @staticmethod
    def create_variable_declaration_node(name: str, var_type: str = "int", 
                                       initializer: Optional[ASTNode] = None) -> ASTNode:
        """Cria um nó de declaração de variável"""
        node = ASTNode("variable_declaration", value=name, var_type=var_type)
        if initializer:
            node.add_child(initializer)
        return node
    
    @staticmethod
    def create_assignment_node(variable: str, expression: ASTNode) -> ASTNode:
        """Cria um nó de atribuição"""
        node = ASTNode("assignment", value=variable)
        node.add_child(expression)
        return node
    
    @staticmethod
    def create_binary_operation_node(operator: str, left: ASTNode, 
                                    right: ASTNode) -> ASTNode:
        """Cria um nó de operação binária"""
        node = ASTNode("binary_operation", value=operator, operator=operator)
        node.add_child(left)
        node.add_child(right)
        return node
    
    @staticmethod
    def create_unary_operation_node(operator: str, operand: ASTNode) -> ASTNode:
        """Cria um nó de operação unária"""
        node = ASTNode("unary_operation", value=operator, operator=operator)
        node.add_child(operand)
        return node
    
    @staticmethod
    def create_number_node(value: int) -> ASTNode:
        """Cria um nó de número literal"""
        return ASTNode("number", value=value, literal_type="int")
    
    @staticmethod
    def create_identifier_node(name: str) -> ASTNode:
        """Cria um nó de identificador"""
        return ASTNode("identifier", value=name)
    
    @staticmethod
    def create_function_call_node(name: str, arguments: List[ASTNode]) -> ASTNode:
        """Cria um nó de chamada de função"""
        node = ASTNode("function_call", value=name)
        node.add_children(arguments)
        return node
    
    @staticmethod
    def create_return_node(expression: Optional[ASTNode] = None) -> ASTNode:
        """Cria um nó de retorno"""
        node = ASTNode("return")
        if expression:
            node.add_child(expression)
        return node
    
    @staticmethod
    def create_print_node(expression: ASTNode) -> ASTNode:
        """Cria um nó de print"""
        node = ASTNode("print")
        node.add_child(expression)
        return node
    
    @staticmethod
    def create_if_node(condition: ASTNode, then_body: List[ASTNode], 
                      else_body: Optional[List[ASTNode]] = None) -> ASTNode:
        """Cria um nó de if"""
        node = ASTNode("if")
        node.add_child(condition)
        # Corpo then
        then_node = ASTNode("then")
        then_node.add_children(then_body)
        node.add_child(then_node)
        # Corpo else (se houver)
        if else_body:
            else_node = ASTNode("else")
            else_node.add_children(else_body)
            node.add_child(else_node)
        return node
    
    @staticmethod
    def create_while_node(condition: ASTNode, body: List[ASTNode]) -> ASTNode:
        """Cria um nó de while"""
        node = ASTNode("while")
        node.add_child(condition)
        body_node = ASTNode("body")
        body_node.add_children(body)
        node.add_child(body_node)
        return node


def print_ast(node: ASTNode, indent: int = 0) -> None:
    """
    Imprime a AST de forma formatada
    """
    if node is None:
        return
    
    indent_str = "  " * indent
    attrs_str = ""
    if node.attributes:
        attrs_str = f" {node.attributes}"
    
    val_str = ""
    if node.value is not None:
        val_str = f" ({node.value})"
    
    print(f"{indent_str}{node.type}{val_str}{attrs_str}")
    
    for child in node.children:
        print_ast(child, indent + 1)


def ast_to_tuple(node: ASTNode) -> tuple:
    """
    Converte um ASTNode para tupla (formato legado)
    Útil para compatibilidade com código existente
    """
    if node is None:
        return None
    
    if node.type == "program":
        return ("program", [ast_to_tuple(child) for child in node.children])
    elif node.type == "function":
        params = [ast_to_tuple(child) for child in node.children 
                 if child.type == "parameter"]
        body = [ast_to_tuple(child) for child in node.children 
               if child.type != "parameter"]
        return ("function", node.value, params, body)
    elif node.type == "parameter":
        return ("param", node.value, node.attributes.get("param_type", "int"))
    elif node.type == "assignment":
        return ("assign", node.value, ast_to_tuple(node.children[0]) if node.children else None)
    elif node.type == "binary_operation":
        return (node.value, ast_to_tuple(node.children[0]), ast_to_tuple(node.children[1]))
    elif node.type == "number":
        return ("num", node.value)
    elif node.type == "identifier":
        return ("id", node.value)
    elif node.type == "function_call":
        args = [ast_to_tuple(child) for child in node.children]
        return ("call", node.value, args)
    elif node.type == "return":
        return ("return", ast_to_tuple(node.children[0]) if node.children else None)
    elif node.type == "print":
        return ("print", ast_to_tuple(node.children[0]) if node.children else None)
    else:
        # Fallback genérico
        return (node.type, node.value, [ast_to_tuple(child) for child in node.children])


def tuple_to_ast(tup: tuple) -> ASTNode:
    """
    Converte uma tupla (formato legado) para ASTNode
    Útil para migração gradual
    """
    if not isinstance(tup, tuple) or len(tup) == 0:
        return ASTNode("invalid")
    
    node_type = tup[0]
    
    if node_type == "program":
        declarations = [tuple_to_ast(item) for item in tup[1]]
        return ASTBuilder.create_program_node(declarations)
    elif node_type == "function":
        name = tup[1]
        params = [tuple_to_ast(p) for p in tup[2]]
        body = [tuple_to_ast(stmt) for stmt in tup[3]]
        return ASTBuilder.create_function_node(name, params, body)
    elif node_type == "param":
        return ASTBuilder.create_parameter_node(tup[1], tup[2] if len(tup) > 2 else "int")
    elif node_type == "var_decl":
        var = tup[1]
        expr = tuple_to_ast(tup[2]) if len(tup) > 2 and tup[2] is not None else None
        return ASTBuilder.create_variable_declaration_node(var, "int", expr)
    elif node_type == "assign":
        var = tup[1]
        expr = tuple_to_ast(tup[2])
        return ASTBuilder.create_assignment_node(var, expr)
    elif node_type in ("+", "-", "*", "/"):
        left = tuple_to_ast(tup[1])
        right = tuple_to_ast(tup[2])
        return ASTBuilder.create_binary_operation_node(node_type, left, right)
    elif node_type == "num":
        return ASTBuilder.create_number_node(tup[1])
    elif node_type == "id":
        return ASTBuilder.create_identifier_node(tup[1])
    elif node_type == "call":
        name = tup[1]
        args = [tuple_to_ast(arg) for arg in tup[2]]
        return ASTBuilder.create_function_call_node(name, args)
    elif node_type == "return":
        expr = tuple_to_ast(tup[1]) if len(tup) > 1 and tup[1] is not None else None
        return ASTBuilder.create_return_node(expr)
    elif node_type == "print":
        expr = tuple_to_ast(tup[1])
        return ASTBuilder.create_print_node(expr)
    else:
        # Fallback genérico
        return ASTNode(node_type, tup[1] if len(tup) > 1 else None)
