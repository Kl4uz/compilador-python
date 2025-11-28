"""
Gerador de Código Intermediário (IR)
Gera código TAC (Three-Address Code) a partir da AST
"""

from typing import List, Optional, Union
from .ast_builder import ASTNode, tuple_to_ast
from .symbol_table import SymbolTable


class IRInstruction:
    """Representa uma instrução de código intermediário"""
    def __init__(self, op: str, arg1=None, arg2=None, result=None):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result
    
    def __repr__(self):
        if self.op == 'print':
            return f"PRINT {self.arg1}"
        elif self.op == '=':
            return f"{self.result} = {self.arg1}"
        elif self.op == 'FUNCTION':
            return f"FUNCTION {self.arg1}:"
        elif self.op == 'BEGIN_FUNC':
            return "BEGIN_FUNC"
        elif self.op == 'END_FUNC':
            return "END_FUNC"
        elif self.op == 'PARAM':
            return f"PARAM {self.arg1}"
        elif self.op == 'ARG':
            return f"ARG {self.arg1}"
        elif self.op == 'CALL':
            return f"{self.result} = CALL {self.arg1}, {self.arg2}"
        elif self.op == 'RETURN':
            if self.arg1:
                return f"RETURN {self.arg1}"
            return "RETURN"
        else:
            return f"{self.result} = {self.arg1} {self.op} {self.arg2}"


class IRGenerator:
    """
    Gerador de Código Intermediário
    Converte AST em código TAC (Three-Address Code)
    """
    
    def __init__(self, symbol_table: Optional[SymbolTable] = None):
        self.instructions: List[IRInstruction] = []
        self.symbol_table = symbol_table or SymbolTable()
        self.temp_count = 0
        self.label_count = 0
    
    def new_temp(self) -> str:
        """Gera um novo nome de variável temporária"""
        self.temp_count += 1
        return f't{self.temp_count}'
    
    def new_label(self) -> str:
        """Gera um novo label"""
        self.label_count += 1
        return f'L{self.label_count}'
    
    def emit(self, op: str, arg1=None, arg2=None, result=None):
        """Emite uma instrução IR"""
        self.instructions.append(IRInstruction(op, arg1, arg2, result))
    
    def generate(self, ast: Union[ASTNode, tuple]) -> List[IRInstruction]:
        """
        Gera código IR a partir da AST
        Aceita tanto ASTNode quanto tupla (formato legado)
        """
        # Converte tupla para ASTNode se necessário
        if isinstance(ast, tuple):
            ast = tuple_to_ast(ast)
        
        self.instructions = []
        self.temp_count = 0
        self.label_count = 0
        
        self._generate_node(ast)
        return self.instructions
    
    def _generate_node(self, node: ASTNode) -> Optional[str]:
        """Gera código IR para um nó da AST"""
        if node is None:
            return None
        
        node_type = node.type
        
        if node_type == "program":
            for child in node.children:
                self._generate_node(child)
            return None
        
        elif node_type == "function":
            func_name = node.value
            self.emit("FUNCTION", arg1=func_name)
            self.emit("BEGIN_FUNC")
            
            # Entra no escopo da função
            self.symbol_table.enter_scope(func_name)
            
            # Processa parâmetros
            for child in node.children:
                if child.type == "parameter":
                    param_name = child.value
                    param_type = child.attributes.get("param_type", "int")
                    self.symbol_table.insert(param_name, param_type, is_param=True)
                    self.emit("PARAM", arg1=param_name)
            
            # Processa corpo da função
            for child in node.children:
                if child.type != "parameter":
                    self._generate_node(child)
            
            self.emit("END_FUNC")
            # Linha em branco será tratada no print_ir
            
            # Sai do escopo
            self.symbol_table.exit_scope()
            return None
        
        elif node_type == "assignment":
            var_name = node.value
            expr_result = self._generate_node(node.children[0]) if node.children else None
            self.emit("=", arg1=expr_result, result=var_name)
            
            # Adiciona à tabela de símbolos se não existir
            if not self.symbol_table.lookup(var_name):
                self.symbol_table.insert(var_name, "int")
            
            return var_name
        
        elif node_type == "variable_declaration":
            var_name = node.value
            var_type = node.attributes.get("var_type", "int")
            
            # Se tem inicializador
            if node.children:
                expr_result = self._generate_node(node.children[0])
                self.emit("=", arg1=expr_result, result=var_name)
            
            # Adiciona à tabela de símbolos
            if not self.symbol_table.lookup_local(var_name):
                self.symbol_table.insert(var_name, var_type)
            
            return var_name
        
        elif node_type == "binary_operation":
            operator = node.value
            left_result = self._generate_node(node.children[0])
            right_result = self._generate_node(node.children[1])
            temp = self.new_temp()
            self.emit(operator, arg1=left_result, arg2=right_result, result=temp)
            return temp
        
        elif node_type == "unary_operation":
            operator = node.value
            operand_result = self._generate_node(node.children[0])
            temp = self.new_temp()
            self.emit(operator, arg1=operand_result, result=temp)
            return temp
        
        elif node_type == "number":
            return str(node.value)
        
        elif node_type == "identifier":
            var_name = node.value
            # Verifica se variável existe
            if not self.symbol_table.lookup(var_name):
                print(f"Warning: Variável '{var_name}' usada antes de ser declarada")
            return var_name
        
        elif node_type == "function_call":
            func_name = node.value
            args = []
            
            # Gera código para argumentos
            for arg_node in node.children:
                arg_result = self._generate_node(arg_node)
                args.append(arg_result)
                self.emit("ARG", arg1=arg_result)
            
            # Emite chamada
            temp = self.new_temp()
            self.emit("CALL", arg1=func_name, arg2=len(args), result=temp)
            return temp
        
        elif node_type == "return":
            if node.children:
                expr_result = self._generate_node(node.children[0])
                self.emit("RETURN", arg1=expr_result)
            else:
                self.emit("RETURN")
            return None
        
        elif node_type == "print":
            expr_result = self._generate_node(node.children[0]) if node.children else None
            self.emit("print", arg1=expr_result)
            return None
        
        elif node_type == "if":
            condition_result = self._generate_node(node.children[0])
            then_label = self.new_label()
            else_label = self.new_label()
            end_label = self.new_label()
            
            # TODO: Implementar geração de código para if/else
            # Por enquanto, apenas processa o corpo then
            if len(node.children) > 1 and node.children[1].type == "then":
                for stmt in node.children[1].children:
                    self._generate_node(stmt)
            
            return None
        
        elif node_type == "while":
            # TODO: Implementar geração de código para while
            condition_result = self._generate_node(node.children[0])
            if len(node.children) > 1 and node.children[1].type == "body":
                for stmt in node.children[1].children:
                    self._generate_node(stmt)
            return None
        
        else:
            # Fallback: processa filhos recursivamente
            for child in node.children:
                self._generate_node(child)
            return None
    
    def print_ir(self):
        """Imprime o código IR gerado"""
        print("\n=== CÓDIGO INTERMEDIÁRIO (TAC) ===")
        for instr in self.instructions:
            if instr.op == "END_FUNC":
                print(instr)
                print()  # Linha em branco após função
            elif instr.op and (instr.op != "=" or instr.result):
                print(instr)
        print("===================================\n")
    
    def get_ir_string(self) -> str:
        """Retorna o código IR como string"""
        lines = []
        for instr in self.instructions:
            if instr.op == "END_FUNC":
                lines.append(str(instr))
                lines.append("")  # Linha em branco após função
            elif instr.op and (instr.op != "=" or instr.result):
                lines.append(str(instr))
        return "\n".join(lines)


# Funções auxiliares para compatibilidade com código legado
def generate_tac(ast: Union[ASTNode, tuple]) -> List[tuple]:
    """
    Função legada para gerar TAC
    Retorna lista de tuplas (formato antigo)
    """
    generator = IRGenerator()
    instructions = generator.generate(ast)
    
    # Converte para formato legado
    tac = []
    for instr in instructions:
        if instr.op == "print":
            tac.append(('print', instr.arg1, None, None))
        elif instr.op == "=":
            tac.append(('=', instr.arg1, None, instr.result))
        elif instr.op in ("+", "-", "*", "/"):
            tac.append((instr.op, instr.arg1, instr.arg2, instr.result))
        elif instr.op == "FUNCTION":
            tac.append(('FUNCTION', instr.arg1, None, None))
        elif instr.op == "BEGIN_FUNC":
            tac.append(('BEGIN_FUNC', None, None, None))
        elif instr.op == "END_FUNC":
            tac.append(('END_FUNC', None, None, None))
        elif instr.op == "PARAM":
            tac.append(('PARAM', instr.arg1, None, None))
        elif instr.op == "ARG":
            tac.append(('ARG', instr.arg1, None, None))
        elif instr.op == "CALL":
            tac.append(('CALL', instr.arg1, instr.arg2, instr.result))
        elif instr.op == "RETURN":
            tac.append(('RETURN', instr.arg1, None, None))
    
    return tac


def print_tac(tac: List[tuple]):
    """Função legada para imprimir TAC"""
    for instr in tac:
        if len(instr) == 4:
            op, arg1, arg2, result = instr
            if op == 'print':
                print(f"print {arg1}")
            elif op == '=':
                print(f"{result} = {arg1}")
            elif op == 'FUNCTION':
                print(f"FUNCTION {arg1}:")
            elif op == 'BEGIN_FUNC':
                print("BEGIN_FUNC")
            elif op == 'END_FUNC':
                print("END_FUNC")
            elif op == 'PARAM':
                print(f"PARAM {arg1}")
            elif op == 'ARG':
                print(f"ARG {arg1}")
            elif op == 'CALL':
                print(f"{result} = CALL {arg1}, {arg2}")
            elif op == 'RETURN':
                if arg1:
                    print(f"RETURN {arg1}")
                else:
                    print("RETURN")
            else:
                print(f"{result} = {arg1} {op} {arg2}")

