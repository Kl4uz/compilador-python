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
        self.label_count = 0    # ← FALTAVA ISSO!

    # ---------------------------------------------------
    # FERRAMENTAS INTERNAS
    # ---------------------------------------------------
    def new_temp(self):
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp

    def new_label(self, base="L"):
        label = f"{base}{self.label_count}"
        self.label_count += 1
        return label

    def emit(self, op, a1=None, a2=None, res=None):
        """Facilita a escrita de quádruplas"""
        self.ir_program.emit(op, a1, a2, res)

    # ---------------------------------------------------
    # MÉTODO PRINCIPAL
    # ---------------------------------------------------
    def generate(self, ast_node):
        self.visit(ast_node)
        return self.ir_program

    # ---------------------------------------------------
    # VISITADOR GENÉRICO
    # ---------------------------------------------------
    def visit(self, node):
        if node is None:
            return None
        method_name = f'visit_{node.node_type}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise NotImplementedError(f"Visitante não implementado: {node.node_type}")

    # ---------------------------------------------------
    # PROGRAMA E FUNÇÃO
    # ---------------------------------------------------
    def visit_program(self, node):
        for decl in node.declarations:
            self.visit(decl)

    def visit_function(self, node):
        self.emit('begin_func', node.name)

        for stmt in node.body:
            self.visit(stmt)

        self.emit('end_func', node.name)

    # ---------------------------------------------------
    # ATRIBUIÇÃO, DECLARAÇÃO, RETORNO, PRINT
    # ---------------------------------------------------
    def visit_decl_assign(self, node):
        val = self.visit(node.value)
        self.emit('assign', val, None, node.name)

    def visit_assign(self, node):
        val = self.visit(node.value)
        self.emit('assign', val, None, node.name)

    def visit_return(self, node):
        if node.value:
            val = self.visit(node.value)
            self.emit('return', val)
        else:
            self.emit('return')

    def visit_print(self, node):
        val = self.visit(node.value)
        self.emit('print', val)

    # ---------------------------------------------------
    # EXPRESSÕES
    # ---------------------------------------------------
    def visit_binop(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        temp = self.new_temp()
        self.emit(node.op, left, right, temp)
        return temp

    def visit_number(self, node):
        return str(node.value)

    def visit_id(self, node):
        return node.name

    def visit_call(self, node):
        args = []
        for arg in node.args:
            temp = self.visit(arg)
            self.emit('param', temp)
            args.append(temp)

        ret = self.new_temp()
        self.emit('call', node.name, args, ret)
        return ret

    # ---------------------------------------------------
    #  IF / ELSE
    # ---------------------------------------------------
    def visit_if(self, node):
        cond = self.visit(node.condition)

        Ltrue = self.new_label("Ltrue")
        Lfalse = self.new_label("Lfalse")
        Lend = self.new_label("Lend")

        # if cond goto Ltrue
        self.emit("IF_GOTO", cond, None, Ltrue)
        # else goto Lfalse
        self.emit("GOTO", None, None, Lfalse)

        # bloco THEN
        self.emit("LABEL", None, None, Ltrue)
        for stmt in node.then_block:
            self.visit(stmt)

        if node.else_block:
            # pular o else
            self.emit("GOTO", None, None, Lend)

            # bloco ELSE
            self.emit("LABEL", None, None, Lfalse)
            for stmt in node.else_block:
                self.visit(stmt)

            # fim do if-else
            self.emit("LABEL", None, None, Lend)

        else:
            # sem else → false é o fim
            self.emit("LABEL", None, None, Lfalse)

    # ---------------------------------------------------
    # WHILE
    # ---------------------------------------------------
    def visit_while(self, node):
        Lbegin = self.new_label("Lbegin")
        Lend = self.new_label("Lend")

        # início do laço
        self.emit("LABEL", None, None, Lbegin)

        # avalia condição
        cond = self.visit(node.condition)

        # if cond == false goto Lend
        self.emit("IF_FALSE_GOTO", cond, None, Lend)

        # corpo
        for stmt in node.body:
            self.visit(stmt)

        # volta ao início
        self.emit("GOTO", None, None, Lbegin)

        # fim do laço
        self.emit("LABEL", None, None, Lend)
