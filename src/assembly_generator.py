"""
Gerador de Código Assembly
Converte código intermediário (IR) em código assembly simples
"""

from typing import List
from .ir_generator import IRInstruction


class AssemblyGenerator:
    """
    Gerador de código assembly
    Converte instruções IR em código assembly simplificado
    """
    
    def __init__(self, target_arch: str = "x86_64"):
        self.target_arch = target_arch
        self.instructions = []
        self.register_pool = ['rax', 'rbx', 'rcx', 'rdx', 'rsi', 'rdi']
        self.used_registers = {}
        self.stack_offset = 0
        self.variable_map = {}  # Mapeia variáveis para posições na stack
    
    def generate(self, ir_instructions: List[IRInstruction]) -> List[str]:
        """
        Gera código assembly a partir de instruções IR
        """
        self.instructions = []
        self.used_registers = {}
        self.stack_offset = 0
        self.variable_map = {}
        
        # Cabeçalho do assembly
        self.instructions.append(".section .text")
        self.instructions.append(".global _start")
        self.instructions.append("")
        
        # Processa cada instrução IR
        for ir_instr in ir_instructions:
            self._generate_from_ir(ir_instr)
        
        return self.instructions
    
    def _generate_from_ir(self, instr: IRInstruction):
        """Gera código assembly para uma instrução IR"""
        if instr.op == "FUNCTION":
            func_name = instr.arg1
            self.instructions.append(f"\n{func_name}:")
            self.instructions.append("    push rbp")
            self.instructions.append("    mov rbp, rsp")
            self.stack_offset = 0
        
        elif instr.op == "BEGIN_FUNC":
            # Prologo da função já foi feito em FUNCTION
            pass
        
        elif instr.op == "END_FUNC":
            self.instructions.append("    mov rsp, rbp")
            self.instructions.append("    pop rbp")
            self.instructions.append("    ret")
        
        elif instr.op == "PARAM":
            # Parâmetros são passados via registros ou stack
            # Simplificado: assume que já estão em registros
            param_name = instr.arg1
            reg = self._allocate_register(param_name)
            self.variable_map[param_name] = reg
        
        elif instr.op == "=":
            # Atribuição: result = arg1
            result = instr.result
            arg1 = instr.arg1
            
            # Se arg1 é constante
            try:
                val = int(arg1)
                reg = self._allocate_register(result)
                self.instructions.append(f"    mov {reg}, {val}")
                self.variable_map[result] = reg
            except ValueError:
                # arg1 é variável ou temporário
                src_reg = self._get_register(arg1)
                dst_reg = self._allocate_register(result)
                self.instructions.append(f"    mov {dst_reg}, {src_reg}")
                self.variable_map[result] = dst_reg
        
        elif instr.op in ("+", "-", "*", "/"):
            # Operação binária: result = arg1 op arg2
            result = instr.result
            arg1 = instr.arg1
            arg2 = instr.arg2
            
            # Carrega arg1 em rax
            try:
                val1 = int(arg1)
                self.instructions.append(f"    mov rax, {val1}")
            except ValueError:
                src_reg = self._get_register(arg1)
                self.instructions.append(f"    mov rax, {src_reg}")
            
            # Operação com arg2
            try:
                val2 = int(arg2)
                if instr.op == "+":
                    self.instructions.append(f"    add rax, {val2}")
                elif instr.op == "-":
                    self.instructions.append(f"    sub rax, {val2}")
                elif instr.op == "*":
                    self.instructions.append(f"    mov rbx, {val2}")
                    self.instructions.append(f"    mul rbx")
                elif instr.op == "/":
                    self.instructions.append(f"    mov rbx, {val2}")
                    self.instructions.append(f"    div rbx")
            except ValueError:
                src_reg = self._get_register(arg2)
                if instr.op == "+":
                    self.instructions.append(f"    add rax, {src_reg}")
                elif instr.op == "-":
                    self.instructions.append(f"    sub rax, {src_reg}")
                elif instr.op == "*":
                    self.instructions.append(f"    mul {src_reg}")
                elif instr.op == "/":
                    self.instructions.append(f"    div {src_reg}")
            
            # Armazena resultado
            dst_reg = self._allocate_register(result)
            self.instructions.append(f"    mov {dst_reg}, rax")
            self.variable_map[result] = dst_reg
        
        elif instr.op == "print":
            # Print: usa syscall write (Linux x86_64)
            arg = instr.arg1
            try:
                val = int(arg)
                self.instructions.append(f"    mov rax, {val}")
            except ValueError:
                src_reg = self._get_register(arg)
                self.instructions.append(f"    mov rax, {src_reg}")
            
            # TODO: Implementar syscall write completo
            # Por enquanto, apenas comentário
            self.instructions.append("    ; TODO: syscall write para imprimir rax")
        
        elif instr.op == "RETURN":
            if instr.arg1:
                try:
                    val = int(instr.arg1)
                    self.instructions.append(f"    mov rax, {val}")
                except ValueError:
                    src_reg = self._get_register(instr.arg1)
                    self.instructions.append(f"    mov rax, {src_reg}")
            else:
                self.instructions.append("    mov rax, 0")
        
        elif instr.op == "ARG":
            # Argumento para chamada de função
            # Simplificado: assume que argumentos são passados via stack
            arg = instr.arg1
            try:
                val = int(arg)
                self.instructions.append(f"    push {val}")
            except ValueError:
                src_reg = self._get_register(arg)
                self.instructions.append(f"    push {src_reg}")
        
        elif instr.op == "CALL":
            func_name = instr.arg1
            num_args = instr.arg2
            result = instr.result
            
            # Chama função
            self.instructions.append(f"    call {func_name}")
            
            # Limpa argumentos da stack (se necessário)
            if num_args > 0:
                self.instructions.append(f"    add rsp, {num_args * 8}")  # 8 bytes por arg
            
            # Armazena resultado
            if result:
                dst_reg = self._allocate_register(result)
                self.instructions.append(f"    mov {dst_reg}, rax")
                self.variable_map[result] = dst_reg
    
    def _allocate_register(self, var_name: str) -> str:
        """Aloca um registro para uma variável"""
        if var_name in self.variable_map:
            return self.variable_map[var_name]
        
        # Aloca próximo registro disponível
        for reg in self.register_pool:
            if reg not in self.used_registers:
                self.used_registers[reg] = var_name
                return reg
        
        # Se não há registros disponíveis, usa stack
        self.stack_offset += 8
        return f"[rbp - {self.stack_offset}]"
    
    def _get_register(self, var_name: str) -> str:
        """Retorna o registro associado a uma variável"""
        if var_name in self.variable_map:
            return self.variable_map[var_name]
        
        # Se não encontrado, assume que é um número
        try:
            int(var_name)
            return var_name
        except ValueError:
            return "rax"  # Fallback
    
    def print_assembly(self):
        """Imprime o código assembly gerado"""
        print("\n=== CÓDIGO ASSEMBLY ===")
        for line in self.instructions:
            print(line)
        print("========================\n")
    
    def get_assembly_string(self) -> str:
        """Retorna o código assembly como string"""
        return "\n".join(self.instructions)

