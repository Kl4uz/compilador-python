"""
IR - Intermediate Representation
Define estrutura do código intermediário (Three-Address Code - TAC)
"""

class TAC:
    """Instrução de Three-Address Code"""
    def __init__(self, op, arg1=None, arg2=None, result=None):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result
    
    def __repr__(self):
        if self.op == 'assign':
            return f"{self.result} = {self.arg1}"
        elif self.op in ('+', '-', '*', '/'):
            return f"{self.result} = {self.arg1} {self.op} {self.arg2}"
        elif self.op == 'call':
            args_str = ', '.join(self.arg2) if self.arg2 else ''
            return f"{self.result} = call {self.arg1}({args_str})"
        elif self.op == 'param':
            return f"param {self.arg1}"
        elif self.op == 'return':
            return f"return {self.arg1}" if self.arg1 else "return"
        elif self.op == 'label':
            return f"{self.arg1}:"
        elif self.op == 'goto':
            return f"goto {self.arg1}"
        elif self.op == 'if':
            return f"if {self.arg1} goto {self.arg2}"
        elif self.op == 'print':
            return f"print {self.arg1}"
        elif self.op == 'begin_func':
            return f"begin_func {self.arg1}"
        elif self.op == 'end_func':
            return f"end_func {self.arg1}"
        else:
            return f"TAC({self.op}, {self.arg1}, {self.arg2}, {self.result})"
    
    def __str__(self):
        return self.__repr__()


class IRProgram:
    """Representa um programa em IR (lista de instruções TAC)"""
    def __init__(self):
        self.instructions = []
    
    def add(self, tac):
        """Adiciona uma instrução TAC"""
        self.instructions.append(tac)
    
    def emit(self, op, arg1=None, arg2=None, result=None):
        """Emite uma nova instrução TAC"""
        tac = TAC(op, arg1, arg2, result)
        self.add(tac)
        return tac
    
    def get_instructions(self):
        """Retorna lista de instruções"""
        return self.instructions
    
    def print_code(self):
        """Imprime o código TAC"""
        print("\n=== CÓDIGO INTERMEDIÁRIO (TAC) ===")
        for i, instr in enumerate(self.instructions):
            print(f"{i:3}: {instr}")
        print("===================================\n")
    
    def print_quadruples(self):
        """
        Imprime código no formato QUÁDRUPLAS conforme professor ensinou
        Formato: (operação, argumento1, argumento2, resultado)
        """
        print("\n=== QUÁDRUPLAS (op, arg1, arg2, result) ===")
        for i, instr in enumerate(self.instructions):
            op = instr.op
            arg1 = instr.arg1 if instr.arg1 is not None else '-'
            arg2 = instr.arg2 if instr.arg2 is not None else '-'
            result = instr.result if instr.result is not None else '-'
            
            # Formata como quádrupla
            print(f"{i:3}: ({op:12}, {str(arg1):10}, {str(arg2):10}, {str(result):10})")
        print("="*60 + "\n")
    
    def __repr__(self):
        return f"IRProgram({len(self.instructions)} instructions)"


# Para testes
if __name__ == "__main__":
    ir = IRProgram()
    
    # Simulando: int x = 5 + 3;
    ir.emit('+', 5, 3, 't1')
    ir.emit('assign', 't1', None, 'x')
    
    # Simulando: y = x * 2;
    ir.emit('*', 'x', 2, 't2')
    ir.emit('assign', 't2', None, 'y')
    
    # Simulando: print(y);
    ir.emit('print', 'y')
    
    # Simulando: return y;
    ir.emit('return', 'y')
    
    ir.print_code()
