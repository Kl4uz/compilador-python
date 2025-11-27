"""
Peephole Optimization - Otimizações Locais por Padrões
Analisa pequenas "janelas" de instruções buscando padrões conhecidos
"""
from ..ir import IRProgram, TAC
from .optimizer import OptimizationPass


class PeepholeOptimizer(OptimizationPass):
    """
    Peephole: Otimizações por reconhecimento de padrões locais
    
    Padrões implementados:
    1. x+0 → x  (identidade aditiva)
    2. x*1 → x  (identidade multiplicativa)
    3. x*0 → 0  (anulação)
    4. x*2^n → x<<n  (shift optimization - requerido pelo professor)
    5. x-0 → x
    6. x/1 → x
    7. x=x → (remove)
    8. x=y; z=x → z=y (elimina intermediário se x não usado depois)
    """
    def _resolve_const(self, arg, const_map):
        if isinstance(arg, str):
            # Apenas strings podem ser identificadores (chaves) em const_map
            return const_map.get(arg, arg)
        return arg # Retorna o argumento original se não for uma string (e.g., uma lista)
    
    def __init__(self, symbolic_only=False):
        """
        symbolic_only: Se True, não propaga valores de variáveis do usuário
                       Útil para mostrar simplificação algébrica pura
        """
        self.symbolic_only = symbolic_only
    
    
    def apply(self, ir_program):
        """Aplica peephole optimization"""
        new_program = IRProgram()
        instructions = ir_program.get_instructions()
        const_map = {}  # Rastreia valores constantes
        
        # Em modo simbólico, identifica variáveis user
        user_vars = set()
        if self.symbolic_only:
            for instr in instructions:
                if instr.result and not self._is_temp(instr.result):
                    user_vars.add(instr.result)
        
        i = 0
        while i < len(instructions):
            instr = instructions[i]
            
            # Rastreia constantes (mas não de variáveis user em modo simbólico)
            if instr.op == 'assign' and self.is_constant(instr.arg1):
                if not self.symbolic_only or instr.result not in user_vars:
                    const_map[instr.result] = instr.arg1
            
            # Resolve valores através do mapa de constantes
            arg1 = self._resolve_const(instr.arg1, const_map)
            arg2 = self._resolve_const(instr.arg2, const_map)
            
            # Padrão 1: x = x + 0 ou x = 0 + x (identidade aditiva)
            if instr.op == '+':
                if arg2 == '0':
                    new_program.emit('assign', instr.arg1, None, instr.result)
                    i += 1
                    continue
                elif arg1 == '0':
                    new_program.emit('assign', instr.arg2, None, instr.result)
                    i += 1
                    continue
            
            # Padrão 2: x = x * 1 ou x = 1 * x (identidade multiplicativa)
            if instr.op == '*':
                if arg2 == '1':
                    new_program.emit('assign', instr.arg1, None, instr.result)
                    i += 1
                    continue
                elif arg1 == '1':
                    new_program.emit('assign', instr.arg2, None, instr.result)
                    i += 1
                    continue
            
            # Padrão 3: x = x * 0 ou x = 0 * x (anulação)
            if instr.op == '*':
                if arg1 == '0' or arg2 == '0':
                    new_program.emit('assign', '0', None, instr.result)
                    const_map[instr.result] = '0'
                    i += 1
                    continue
            
            # Padrão 3.5: x = a * 2^n => x = a << n (otimização shift - professor)
            # Shift é mais rápido que multiplicação em hardware
            # Exemplos: a*2 → a<<1, a*4 → a<<2, a*8 → a<<3
            if instr.op == '*':
                shift_amount = self.is_power_of_two(instr.arg2)
                if shift_amount is not None:
                    new_program.emit('<<', instr.arg1, str(shift_amount), instr.result)
                    i += 1
                    continue
                shift_amount = self.is_power_of_two(instr.arg1)
                if shift_amount is not None:
                    new_program.emit('<<', instr.arg2, str(shift_amount), instr.result)
                    i += 1
                    continue
            
            # Padrão 4: x = y - 0 (subtração de zero)
            if instr.op == '-' and arg2 == '0':
                new_program.emit('assign', instr.arg1, None, instr.result)
                i += 1
                continue
            
            # Padrão 4.5: x = y / 1 (divisão por 1)
            if instr.op == '/' and arg2 == '1':
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
    
    def _is_temp(self, var):
        """Verifica se é variável temporária (com dígito)"""
        return var and str(var).startswith('t') and str(var)[1:].isdigit()
    
    def is_used_later(self, var, instructions):
        """Verifica se variável é usada nas instruções seguintes"""
        for instr in instructions:
            if instr.arg1 == var or instr.arg2 == var:
                return True
        return False
    
    def is_constant(self, value):
        """Verifica se é uma constante literal"""
        try:
            int(value)
            return True
        except (ValueError, TypeError):
            return False
    
    def is_power_of_two(self, value):
        """
        Verifica se é potência de 2 e retorna o expoente
        Usa truque bit: n é potência de 2 se (n & (n-1)) == 0
        Exemplos: 2→1, 4→2, 8→3, 16→4
        """
        try:
            val = int(value)
            if val > 0 and (val & (val - 1)) == 0:
                shift = 0
                while val > 1:
                    val >>= 1
                    shift += 1
                return shift
        except (ValueError, TypeError):
            pass
        return None


class AlgebraicSimplification(OptimizationPass):
    """
    Simplificação Algébrica - Padrões matemáticos
    Identifica identidades algébricas conhecidas
    """
    
    def apply(self, ir_program):
        """Aplica simplificações algébricas baseadas em propriedades matemáticas"""
        new_program = IRProgram()
        
        for instr in ir_program.get_instructions():
            # Padrão: x = a - a => x = 0 (qualquer coisa menos ela mesma é zero)
            if instr.op == '-' and instr.arg1 == instr.arg2:
                new_program.emit('assign', '0', None, instr.result)
                continue
            
            # Padrão: x = a / a => x = 1 (qualquer coisa dividida por ela mesma é 1)
            # Nota: assumimos a != 0 (análise semântica já verificou)
            if instr.op == '/' and instr.arg1 == instr.arg2:
                new_program.emit('assign', '1', None, instr.result)
                continue
            
            # Nenhum padrão aplicado, mantém instrução
            new_program.add(instr)
        
        return new_program