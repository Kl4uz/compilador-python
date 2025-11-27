"""
AST - Abstract Syntax Tree
Define estrutura e construtor de AST a partir do Parse Tree
"""

class ASTNode:
    """Nó base da AST"""
    def __init__(self, node_type, **attrs):
        self.node_type = node_type
        self.__dict__.update(attrs)
    
    def __repr__(self):
        attrs = {k: v for k, v in self.__dict__.items() if k != 'node_type'}
        return f"{self.node_type}({attrs})"

class ProgramNode(ASTNode):
    """Nó raiz do programa"""
    def __init__(self, declarations):
        super().__init__('program', declarations=declarations)

class FunctionNode(ASTNode):
    """Nó de declaração de função"""
    def __init__(self, name, params, body):
        super().__init__('function', name=name, params=params, body=body)

class ParameterNode(ASTNode):
    """Nó de parâmetro de função"""
    def __init__(self, name, param_type):
        super().__init__('parameter', name=name, param_type=param_type)

class DeclAssignNode(ASTNode):
    """Nó de declaração com atribuição"""
    def __init__(self, name, value):
        super().__init__('decl_assign', name=name, value=value)

class AssignNode(ASTNode):
    """Nó de atribuição"""
    def __init__(self, name, value):
        super().__init__('assign', name=name, value=value)

class ReturnNode(ASTNode):
    """Nó de retorno"""
    def __init__(self, value):
        super().__init__('return', value=value)

class PrintNode(ASTNode):
    """Nó de impressão"""
    def __init__(self, value):
        super().__init__('print', value=value)

class BinOpNode(ASTNode):
    """Nó de operação binária"""
    def __init__(self, op, left, right):
        super().__init__('binop', op=op, left=left, right=right)

class NumberNode(ASTNode):
    """Nó de número literal"""
    def __init__(self, value):
        super().__init__('number', value=value)

class IdNode(ASTNode):
    """Nó de identificador"""
    def __init__(self, name):
        super().__init__('id', name=name)

class CallNode(ASTNode):
    """Nó de chamada de função"""
    def __init__(self, name, args):
        super().__init__('call', name=name, args=args)
class IfNode(ASTNode):
    def __init__(self, condition, then_block, else_block):
        super().__init__('if', condition=condition, then_block=then_block, else_block=else_block)

class WhileNode(ASTNode):
    def __init__(self, condition, body):
        super().__init__('while', condition=condition, body=body)

class BlockNode(ASTNode):
    def __init__(self, statements):
        super().__init__('block', statements=statements)

class ForNode(ASTNode):
    def __init__(self, init, condition, increment, body):
        super().__init__('for', init=init, condition=condition, increment=increment, body=body)




def build_ast(parse_tree):
    """
    Converte Parse Tree em AST
    Recebe: tupla do parser (parse_tree)
    Retorna: ASTNode estruturado
    """
    if not parse_tree:
        return None
    
    node_type = parse_tree[0]
    
    # Programa
    if node_type == 'program':
        declarations = [build_ast(decl) for decl in parse_tree[1]]
        return ProgramNode(declarations)
    
    # Função
    elif node_type == 'function':
        name = parse_tree[1]
        params = [build_ast(p) for p in parse_tree[2]]
        body = [build_ast(stmt) for stmt in parse_tree[3]]
        return FunctionNode(name, params, body)
    
    # Parâmetro
    elif node_type == 'param':
        return ParameterNode(parse_tree[1], parse_tree[2])
    
    # Declaração com atribuição
    elif node_type == 'decl_assign':
        return DeclAssignNode(parse_tree[1], build_ast(parse_tree[2]))
    
    # Atribuição
    elif node_type == 'assign':
        return AssignNode(parse_tree[1], build_ast(parse_tree[2]))
    
    # Retorno
    elif node_type == 'return':
        value = build_ast(parse_tree[1]) if parse_tree[1] else None
        return ReturnNode(value)

    elif node_type == 'if':
        cond = build_ast(parse_tree[1])
        then_block = [build_ast(s) for s in parse_tree[2]]
        else_raw = parse_tree[3]
        else_block = [build_ast(s) for s in else_raw] if else_raw else None
        return IfNode(cond, then_block, else_block)

    elif node_type == 'while':
        cond = build_ast(parse_tree[1])
        body = [build_ast(s) for s in parse_tree[2]]
        return WhileNode(cond, body)

    
    # Print
    elif node_type == 'print':
        return PrintNode(build_ast(parse_tree[1]))
    
    # Operações binárias
    elif node_type in ('+', '-', '*', '/', '<', '>', '<=', '>=', '==', '!='):
        return BinOpNode(node_type, build_ast(parse_tree[1]), build_ast(parse_tree[2]))
    
    # Número
    elif node_type == 'num':
        return NumberNode(parse_tree[1])
    
    # Identificador
    elif node_type == 'id':
        return IdNode(parse_tree[1])
    
    # Chamada de função
    elif node_type == 'call':
        args = [build_ast(arg) for arg in parse_tree[2]]
        return CallNode(parse_tree[1], args)
    
    elif node_type in ('LT','GT','LE','GE','EQ','NE'):
        return BinOpNode(node_type, build_ast(parse_tree[1]), build_ast(parse_tree[2]))
    
    elif node_type == 'for':
        init = build_ast(parse_tree[1])
        cond = build_ast(parse_tree[2])
        inc = build_ast(parse_tree[3])
        body = [build_ast(s) for s in parse_tree[4]]
        return ForNode(init, cond, inc, body)
    
    else:
        raise ValueError(f"Tipo de nó desconhecido: {node_type}")


def print_ast(node, indent=0):
    """Imprime AST de forma legível"""
    prefix = "  " * indent
    
    if isinstance(node, ProgramNode):
        print(f"{prefix}PROGRAM")
        for decl in node.declarations:
            print_ast(decl, indent + 1)
    
    elif isinstance(node, FunctionNode):
        print(f"{prefix}FUNCTION {node.name}")
        if node.params:
            print(f"{prefix}  PARAMS:")
            for param in node.params:
                print_ast(param, indent + 2)
        print(f"{prefix}  BODY:")
        for stmt in node.body:
            print_ast(stmt, indent + 2)
    
    elif isinstance(node, ParameterNode):
        print(f"{prefix}{node.param_type} {node.name}")
    
    elif isinstance(node, DeclAssignNode):
        print(f"{prefix}DECL_ASSIGN {node.name} =")
        print_ast(node.value, indent + 1)
    
    elif isinstance(node, AssignNode):
        print(f"{prefix}ASSIGN {node.name} =")
        print_ast(node.value, indent + 1)
    
    elif isinstance(node, ReturnNode):
        print(f"{prefix}RETURN")
        if node.value:
            print_ast(node.value, indent + 1)
    
    elif isinstance(node, PrintNode):
        print(f"{prefix}PRINT")
        print_ast(node.value, indent + 1)
    
    elif isinstance(node, BinOpNode):
        print(f"{prefix}{node.op}")
        print_ast(node.left, indent + 1)
        print_ast(node.right, indent + 1)
    
    elif isinstance(node, NumberNode):
        print(f"{prefix}{node.value}")
    
    elif isinstance(node, IdNode):
        print(f"{prefix}id:{node.name}")
    
    elif isinstance(node, CallNode):
        print(f"{prefix}CALL {node.name}")
        for arg in node.args:
            print_ast(arg, indent + 1)


# Para testes
if __name__ == "__main__":
    from parser import parse_from_code
    
    test_code = """
    int soma(int a, int b) {
        int r = a + b;
        return r;
    }
    """
    
    print("=== TESTE DA AST ===")
    print("Código:")
    print(test_code)
    
    parse_tree = parse_from_code(test_code)
    print("\nParse Tree:")
    print(parse_tree)
    
    ast = build_ast(parse_tree)
    print("\nAST estruturada:")
    print_ast(ast)
