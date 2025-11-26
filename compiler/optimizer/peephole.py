"""
Peephole Optimization - Otimizações locais
Melhora código analisando pequenas janelas de instruções
"""
from ..ir import IRProgram, TAC
from .optimizer import OptimizationPass


class PeepholeOptimizer(OptimizationPass):
    """
    Peephole: otimizações em janelas pequenas de código
    Exemplos:
    - x = x + 0 => (remove)
    - x = x * 1 => (remove)
    - x = y; z = x => z = y (elimina intermediário)
    """
    
    def apply(self, ir_program):
        """Aplica peephole optimization"""
        new_program = IRProgram()
        instructions = ir_program.get_instructions()
        
        i = 0
        while i < len(instructions):
            instr = instructions[i]
            
            # Padrão 1: x = x + 0 ou x = 0 + x (identidade aditiva)
            if instr.op == '+':
                if instr.arg2 == '0':
                    # x = a + 0 => x = a
                    new_program.emit('assign', instr.arg1, None, instr.result)
                    i += 1
                    continue
                elif instr.arg1 == '0':
                    # x = 0 + a => x = a
                    new_program.emit('assign', instr.arg2, None, instr.result)
                    i += 1
                    continue
            
            # Padrão 2: x = x * 1 ou x = 1 * x (identidade multiplicativa)
            if instr.op == '*':
                if instr.arg2 == '1':
                    # x = a * 1 => x = a
                    new_program.emit('assign', instr.arg1, None, instr.result)
                    i += 1
                    continue
                elif instr.arg1 == '1':
                    # x = 1 * a => x = a
                    new_program.emit('assign', instr.arg2, None, instr.result)
                    i += 1
                    continue
            
            # Padrão 3: x = x * 0 ou x = 0 * x (anulação)
            if instr.op == '*':
                if instr.arg1 == '0' or instr.arg2 == '0':
                    # x = a * 0 => x = 0
                    new_program.emit('assign', '0', None, instr.result)
                    i += 1
                    continue
            
            # Padrão 4: x = y - 0 (subtração de zero)
            if instr.op == '-' and instr.arg2 == '0':
                # x = a - 0 => x = a
                new_program.emit('assign', instr.arg1, None, instr.result)
                i += 1
                continue
            
            # Padrão 5: Atribuições redundantes (x = x)
            if instr.op == 'assign' and instr.arg1 == instr.result:
                # x = x => (remove)
                i += 1
                continue
            
            # Padrão 6: Chain de atribuições
            # x = y; z = x => z = y (se x não é usado depois)
            if (instr.op == 'assign' and 
                i + 1 < len(instructions) and
                instructions[i + 1].op == 'assign' and
                instructions[i + 1].arg1 == instr.result):
                
                next_instr = instructions[i + 1]
                # Verifica se temp não é usado em outro lugar
                if self.is_temp(instr.result) and not self.is_used_later(instr.result, instructions[i+2:]):
                    # z = y (pula intermediário)
                    new_program.emit('assign', instr.arg1, None, next_instr.result)
                    i += 2
                    continue
            
            # Nenhum padrão aplicado, mantém instrução
            new_program.add(instr)
            i += 1
        
        return new_program
    
    def is_temp(self, var):
        """Verifica se é variável temporária"""
        return isinstance(var, str) and var.startswith('t')
    
    def is_used_later(self, var, instructions):
        """Verifica se variável é usada nas instruções seguintes"""
        for instr in instructions:
            if instr.arg1 == var or instr.arg2 == var:
                return True
        return False


class AlgebraicSimplification(OptimizationPass):
    """Simplificações algébricas"""
    
    def apply(self, ir_program):
        """Aplica simplificações algébricas"""
        new_program = IRProgram()
        
        for instr in ir_program.get_instructions():
            # x = a - a => x = 0
            if instr.op == '-' and instr.arg1 == instr.arg2:
                new_program.emit('assign', '0', None, instr.result)
                continue
            
            # x = a / a => x = 1 (se a != 0)
            if instr.op == '/' and instr.arg1 == instr.arg2:
                new_program.emit('assign', '1', None, instr.result)
                continue
            
            # Mantém instrução original
            new_program.add(instr)
        
        return new_program


# Para testes
if __name__ == "__main__":
    from ir import IRProgram
    
    # Cria programa de teste
    ir = IRProgram()
    
    # Teste 1: x = y + 0
    ir.emit('+', 'y', '0', 't1')
    ir.emit('assign', 't1', None, 'x')
    
    # Teste 2: z = a * 1
    ir.emit('*', 'a', '1', 't2')
    ir.emit('assign', 't2', None, 'z')
    
    # Teste 3: w = b * 0
    ir.emit('*', 'b', '0', 't3')
    ir.emit('assign', 't3', None, 'w')
    
    # Teste 4: r = c - c
    ir.emit('-', 'c', 'c', 't4')
    ir.emit('assign', 't4', None, 'r')
    
    # Teste 5: Chain: t5 = d; s = t5
    ir.emit('assign', 'd', None, 't5')
    ir.emit('assign', 't5', None, 's')
    
    print("=== CÓDIGO ORIGINAL ===")
    ir.print_code()
    
    # Aplica peephole
    peephole = PeepholeOptimizer()
    optimized = peephole.apply(ir)
    
    print("\n=== APÓS PEEPHOLE ===")
    optimized.print_code()
    
    # Aplica simplificação algébrica
    algebraic = AlgebraicSimplification()
    optimized2 = algebraic.apply(optimized)
    
    print("\n=== APÓS SIMPLIFICAÇÃO ALGÉBRICA ===")
    optimized2.print_code()
