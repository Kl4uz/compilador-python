

class ASTNode:
    def __init__(self, node_type, **kwargs):
        self.type = node_type
        self.atributes = kwargs
        self.children = []

    def add_child(self, child):
        self.children.append(child)
        return self
    
class ASTBuilder:
    """
    Construtor de AST
    Fornece métodos para criar nós da AST
    """
    def create_function_node(self, name, parameters, body):
        node = ASTNode("function", name=name, parameters=parameters)
        for stmt in body:
            node.add_child(stmt)
        return node
    
    def create_variable_node(self, name, var_type):
        return ASTNode("variable", name=name, type=var_type)
    
    def create_assignment_node(self, variable, expression):
        node = ASTNode("assignment")
        node.add_child(variable)
        node.add_child(expression)
        return node
    
    def create_binary_operation_node(self, operator, left, right):
        node = ASTNode("binary_operation", operator=operator)
        node.add_child(left)
        node.add_child(right)
        return node
    
    def create_print_node(self, expression):
        node = ASTNode("print")
        node.add_child(expression)
        return node
    
    def create_call_node(self, function_name, arguments):
        node = ASTNode("call", function_name=function_name)
        for arg in arguments:
            node.add_child(arg)
        return node