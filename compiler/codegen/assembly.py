"""
Assembly Generator - Geração de Código Assembly
Converte código IR otimizado em assembly MIPS-like simplificado
"""


class AssemblyGenerator:
    """Gerador de código assembly a partir de IR"""
    
    def __init__(self):
        self.code = []
        self.register_map = {}  # mapa: variável/temp -> registrador
        self.next_register = 0
        self.max_registers = 10  # Simplificado: 10 registradores ($t0-$t9)
    
    def allocate_register(self, var):
        """Aloca um registrador para variável"""
        if var in self.register_map:
            return self.register_map[var]
        
        # Aloca novo registrador
        if self.next_register < self.max_registers:
            reg = f"$t{self.next_register}"
            self.next_register += 1
            self.register_map[var] = reg
            return reg
        
        # Se esgotou registradores, reutiliza (simplificado)
        return "$t0"  # Fallback
    
    def get_operand(self, value):
        """Converte operando para formato assembly"""
        # Se é literal, retorna direto
        try:
            int(value)
            return value
        except (ValueError, TypeError):
            pass
        
        # Se é variável/temp, retorna registrador alocado
        if value in self.register_map:
            return self.register_map[value]
        
        # Aloca registrador e carrega variável
        reg = self.allocate_register(value)
        self.emit(f"lw {reg}, {value}")  # load word
        return reg
    
    def emit(self, instruction):
        """Emite uma instrução assembly"""
        self.code.append(instruction)
    
    def generate(self, ir_program):
        """
        Gera código assembly a partir do IR
        Retorna: lista de instruções assembly
        """
        self.code = []
        
        for instr in ir_program.get_instructions():
            self.visit_instruction(instr)
        
        return self.code
    
    def visit_instruction(self, instr):
        """Gera assembly para uma instrução TAC"""
        
        if instr.op == 'begin_func':
            self.emit(f"\n# Função: {instr.arg1}")
            self.emit(f"{instr.arg1}:")
            # Prólogo da função
            self.emit("  addi $sp, $sp, -4")  # reserva espaço na pilha
            self.emit("  sw $fp, 0($sp)")     # salva frame pointer
            self.emit("  move $fp, $sp")      # novo frame pointer
            self.register_map = {}  # Reset registradores por função
            self.next_register = 0
        
        elif instr.op == 'end_func':
            # Epílogo da função
            self.emit("  lw $fp, 0($sp)")     # restaura frame pointer
            self.emit("  addi $sp, $sp, 4")   # libera espaço
            self.emit("  jr $ra")              # retorna
        
        elif instr.op == 'assign':
            # result = arg1
            dest_reg = self.allocate_register(instr.result)
            
            # Se arg1 é literal
            try:
                value = int(instr.arg1)
                self.emit(f"  li {dest_reg}, {value}")  # load immediate
            except (ValueError, TypeError):
                # Se arg1 é variável
                src_reg = self.get_operand(instr.arg1)
                self.emit(f"  move {dest_reg}, {src_reg}")
            
            # Salva na memória se não é temp
            if not instr.result.startswith('t'):
                self.emit(f"  sw {dest_reg}, {instr.result}")
        
        elif instr.op == '+':
            # result = arg1 + arg2
            dest_reg = self.allocate_register(instr.result)
            arg1_reg = self.get_operand(instr.arg1)
            
            # Se arg2 é literal
            try:
                value = int(instr.arg2)
                self.emit(f"  addi {dest_reg}, {arg1_reg}, {value}")
            except (ValueError, TypeError):
                # Se arg2 é variável
                arg2_reg = self.get_operand(instr.arg2)
                self.emit(f"  add {dest_reg}, {arg1_reg}, {arg2_reg}")
        
        elif instr.op == '-':
            # result = arg1 - arg2
            dest_reg = self.allocate_register(instr.result)
            arg1_reg = self.get_operand(instr.arg1)
            arg2_reg = self.get_operand(instr.arg2)
            self.emit(f"  sub {dest_reg}, {arg1_reg}, {arg2_reg}")
        
        elif instr.op == '*':
            # result = arg1 * arg2
            dest_reg = self.allocate_register(instr.result)
            arg1_reg = self.get_operand(instr.arg1)
            arg2_reg = self.get_operand(instr.arg2)
            self.emit(f"  mul {dest_reg}, {arg1_reg}, {arg2_reg}")
        
        elif instr.op == '/':
            # result = arg1 / arg2
            dest_reg = self.allocate_register(instr.result)
            arg1_reg = self.get_operand(instr.arg1)
            arg2_reg = self.get_operand(instr.arg2)
            self.emit(f"  div {arg1_reg}, {arg2_reg}")  # resultado em $lo
            self.emit(f"  mflo {dest_reg}")              # move de $lo
        
        elif instr.op == 'return':
            # return arg1
            if instr.arg1:
                ret_reg = self.get_operand(instr.arg1)
                self.emit(f"  move $v0, {ret_reg}")  # move para registrador de retorno
        
        elif instr.op == 'print':
            # print arg1
            arg_reg = self.get_operand(instr.arg1)
            self.emit(f"  move $a0, {arg_reg}")   # move para registrador de argumento
            self.emit("  li $v0, 1")               # syscall print_int
            self.emit("  syscall")
        
        elif instr.op == 'param':
            # Empilha parâmetro
            param_reg = self.get_operand(instr.arg1)
            self.emit(f"  addi $sp, $sp, -4")
            self.emit(f"  sw {param_reg}, 0($sp)")
        
        elif instr.op == 'call':
            # Chama função
            self.emit(f"  jal {instr.arg1}")  # jump and link
            # Resultado em $v0
            if instr.result:
                dest_reg = self.allocate_register(instr.result)
                self.emit(f"  move {dest_reg}, $v0")
            # Limpa parâmetros da pilha
            num_params = len(instr.arg2) if instr.arg2 else 0
            if num_params > 0:
                self.emit(f"  addi $sp, $sp, {num_params * 4}")
        
        else:
            self.emit(f"  # Instrução não implementada: {instr}")
    
    def print_code(self):
        """Imprime código assembly"""
        print("\n=== CÓDIGO ASSEMBLY ===")
        for line in self.code:
            print(line)
        print("=======================\n")


# Para testes
if __name__ == "__main__":
    from ir import IRProgram
    
    # Cria programa IR de teste
    ir = IRProgram()
    
    ir.emit('begin_func', 'soma')
    ir.emit('+', 'a', 'b', 't1')
    ir.emit('assign', 't1', None, 'r')
    ir.emit('return', 'r')
    ir.emit('end_func', 'soma')
    
    ir.emit('begin_func', 'main')
    ir.emit('assign', '5', None, 'x')
    ir.emit('param', 'x')
    ir.emit('param', '3')
    ir.emit('call', 'soma', ['x', '3'], 't2')
    ir.emit('assign', 't2', None, 'y')
    ir.emit('print', 'y')
    ir.emit('return', '0')
    ir.emit('end_func', 'main')
    
    print("=== CÓDIGO IR ===")
    ir.print_code()
    
    # Gera assembly
    asm_gen = AssemblyGenerator()
    asm_code = asm_gen.generate(ir)
    
    asm_gen.print_code()
