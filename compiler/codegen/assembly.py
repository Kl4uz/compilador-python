"""
Assembly Generator
Converte IR em assembly genérico (LOAD/STORE/ADD/MUL/etc)
"""

class AssemblyGenerator:
    def __init__(self):
        self.code = []
        self.register_map = {}
        self.next_register = 0
        self.max_registers = 10  # R0-R9
    
    def allocate_register(self, var):
        if var in self.register_map:
            return self.register_map[var]
        
        if self.next_register < self.max_registers:
            reg = f"R{self.next_register}"
            self.next_register += 1
            self.register_map[var] = reg
            return reg
        return "R0"
    
    def get_operand(self, value):
        try:
            int(value)
            return value
        except (ValueError, TypeError):
            pass
        
        if value in self.register_map:
            return self.register_map[value]
        
        reg = self.allocate_register(value)
        self.emit(f"  LOAD {reg}, {value}")
        return reg
    
    def emit(self, instruction):
        self.code.append(instruction)
    
    def generate(self, ir_program):
        self.code = []
        for instr in ir_program.get_instructions():
            self.visit_instruction(instr)
        return self.code
    
    def visit_instruction(self, instr):
        if instr.op == 'begin_func':
            self.emit(f"\n{instr.arg1}:")
            self.emit("  ENTER")
            self.register_map = {}
            self.next_register = 0
        
        elif instr.op == 'end_func':
            self.emit("  LEAVE")
            self.emit("  RETURN")
        
        elif instr.op == 'assign':
            dest_reg = self.allocate_register(instr.result)
            try:
                value = int(instr.arg1)
                self.emit(f"  LOAD {dest_reg}, {value}")
            except (ValueError, TypeError):
                src_reg = self.get_operand(instr.arg1)
                self.emit(f"  MOVE {dest_reg}, {src_reg}")
            
            if not instr.result.startswith('t'):
                self.emit(f"  STORE {dest_reg}, {instr.result}")
        
        elif instr.op == '+':
            dest_reg = self.allocate_register(instr.result)
            arg1_reg = self.get_operand(instr.arg1)
            arg2_reg = self.get_operand(instr.arg2)
            self.emit(f"  ADD {dest_reg}, {arg1_reg}, {arg2_reg}")
        
        elif instr.op == '-':
            dest_reg = self.allocate_register(instr.result)
            arg1_reg = self.get_operand(instr.arg1)
            arg2_reg = self.get_operand(instr.arg2)
            self.emit(f"  SUB {dest_reg}, {arg1_reg}, {arg2_reg}")
        
        elif instr.op == '*':
            dest_reg = self.allocate_register(instr.result)
            arg1_reg = self.get_operand(instr.arg1)
            arg2_reg = self.get_operand(instr.arg2)
            self.emit(f"  MUL {dest_reg}, {arg1_reg}, {arg2_reg}")
        
        elif instr.op == '/':
            dest_reg = self.allocate_register(instr.result)
            arg1_reg = self.get_operand(instr.arg1)
            arg2_reg = self.get_operand(instr.arg2)
            self.emit(f"  DIV {dest_reg}, {arg1_reg}, {arg2_reg}")
        
        elif instr.op == '<<':
            dest_reg = self.allocate_register(instr.result)
            arg1_reg = self.get_operand(instr.arg1)
            self.emit(f"  SHL {dest_reg}, {arg1_reg}, {instr.arg2}")
        
        elif instr.op == 'return':
            if instr.arg1:
                ret_reg = self.get_operand(instr.arg1)
                self.emit(f"  RET {ret_reg}")
            else:
                self.emit(f"  RET")
        
        elif instr.op == 'print':
            arg_reg = self.get_operand(instr.arg1)
            self.emit(f"  PRINT {arg_reg}")
        
        elif instr.op == 'param':
            param_reg = self.get_operand(instr.arg1)
            self.emit(f"  PARAM {param_reg}")
        
        elif instr.op == 'call':
            self.emit(f"  CALL {instr.arg1}")
            if instr.result:
                dest_reg = self.allocate_register(instr.result)
                self.emit(f"  GETRET {dest_reg}")
    
    def print_code(self):
        print("\n=== ASSEMBLY ===")
        for line in self.code:
            print(line)
        print("================\n")