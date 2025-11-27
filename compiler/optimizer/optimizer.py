"""
Optimizer - Pipeline de Otimizações do IR
Implementa 6 tipos de otimizações clássicas de compiladores
"""
from ..ir import IRProgram, TAC

class Optimizer:
    """Gerenciador do pipeline de otimizações"""
    def __init__(self):
        self.optimizations = []
    
    def add_optimization(self, optimization):
        """Adiciona uma otimização ao pipeline"""
        self.optimizations.append(optimization)
    
    def optimize(self, ir_program):
        """Aplica todas otimizações sequencialmente"""
        optimized = ir_program
        for optimization in self.optimizations:
            optimized = optimization.apply(optimized)
        return optimized


class OptimizationPass:
    """Classe base para todas otimizações"""
    def apply(self, ir_program):
        raise NotImplementedError("Subclasses devem implementar apply()")


class ConstantFolding(OptimizationPass):
    """
    Constant Folding - Calcula expressões constantes em tempo de compilação
    Exemplo: t0 = 2 + 3  →  t0 = 5
    """
    
    def __init__(self, symbolic_only=False):
        """
        symbolic_only: Se True, não usa valores das variáveis do usuário (a, b, c)
                       apenas calcula literais puros (2+3→5, 10*2→20)
                       Útil para mostrar simplificação algébrica pura
        """
        self.symbolic_only = symbolic_only
    
    def apply(self, ir_program):
        new_program = IRProgram()
        const_values = {}  # Rastreia valores constantes conhecidos
        user_vars = set()  # Variáveis declaradas pelo usuário
        
        # Identifica variáveis user (não-temporárias)
        for instr in ir_program.get_instructions():
            if instr.result and not self._is_temp(instr.result):
                user_vars.add(instr.result)
        
        for instr in ir_program.get_instructions():
            # Rastreia atribuições de constantes
            if instr.op == 'assign' and self.is_literal(instr.arg1):
                # Em modo simbólico, não propaga valores de variáveis user
                if not self.symbolic_only or instr.result not in user_vars:
                    const_values[instr.result] = instr.arg1
                new_program.add(instr)
                continue
            
            # Operações aritméticas
            if instr.op in ('+', '-', '*', '/', '<<'):
                arg1_val = const_values.get(instr.arg1, instr.arg1)
                arg2_val = const_values.get(instr.arg2, instr.arg2)
                
                if self.is_literal(arg1_val) and self.is_literal(arg2_val):
                    value = self.evaluate(instr.op, arg1_val, arg2_val)
                    new_program.emit('assign', str(value), None, instr.result)
                    const_values[instr.result] = str(value)
                    continue
            
            new_program.add(instr)
        
        return new_program
    
    def _is_temp(self, var):
        return var and str(var).startswith('t') and str(var)[1:].isdigit()
    
    def is_literal(self, value):
        try:
            int(value)
            return True
        except (ValueError, TypeError):
            return False
    
    def evaluate(self, op, arg1, arg2):
        a, b = int(arg1), int(arg2)
        if op == '+': return a + b
        elif op == '-': return a - b
        elif op == '*': return a * b
        elif op == '/': return a // b if b != 0 else 0
        elif op == '<<': return a << b
        else: raise ValueError(f"Operador não suportado: {op}")


class DeadCodeElimination(OptimizationPass):
    """
    Dead Code Elimination - Remove código não utilizado
    Remove apenas temporários (t0, t1) que não são usados
    Mantém SEMPRE declarações de variáveis do usuário (a, b, c, r)
    """
    
    def apply(self, ir_program):
        instructions = ir_program.get_instructions()
        
        # Passo 1: Marca variáveis do usuário (não-temp) como sempre usadas
        used = set()
        for instr in instructions:
            if instr.result and not self._is_temp(instr.result):
                used.add(instr.result)
        
        # Passo 2: Propagação backward - rastreia dependências
        # Se uma variável é usada, seus operandos também são
        changed = True
        while changed:
            changed = False
            for instr in instructions:
                # ...
                    # Marca arg1 como usado
                    if isinstance(instr.arg1, str) and instr.arg1 and not self._is_literal(instr.arg1) and instr.arg1 not in used:
                        used.add(instr.arg1)
                        changed = True
                    # Marca arg2 como usado
                    if isinstance(instr.arg2, str) and instr.arg2 and not self._is_literal(instr.arg2) and instr.arg2 not in used:
                        used.add(instr.arg2)
                        changed = True
        
        # Passo 3: Remove apenas temporários não usados
        new_program = IRProgram()
        for instr in instructions:
            # Sempre mantém: controle de fluxo, variáveis user, temporários usados
            if instr.op in ('begin_func', 'end_func', 'return', 'label', 'goto', 'print'):
                new_program.add(instr)
            elif instr.result and not self._is_temp(instr.result):
                new_program.add(instr)
            elif instr.result and instr.result in used:
                new_program.add(instr)
        
        return new_program
    
    def _is_temp(self, var):
        return str(var).startswith('t') and str(var)[1:].isdigit()
    
    def _is_literal(self, val):
        if isinstance(val, (int, float)):
            return True
        return str(val).lstrip('-').isdigit()


class CommonSubexpressionElimination(OptimizationPass):
    """
    CSE - Elimina Subexpressões Comuns
    Se a mesma expressão (a+b) é calculada 2x, reutiliza o resultado
    Exemplo: t0=a+b; t1=a+b  →  t0=a+b; t1=t0
    """
    
    def apply(self, ir_program):
        new_program = IRProgram()
        expressions = {}  # Mapa: (op, arg1, arg2) → resultado anterior
        
        for instr in ir_program.get_instructions():
            # Procura por operações aritméticas repetidas
            if instr.op in ('+', '-', '*', '/'):
                expr_key = (instr.op, instr.arg1, instr.arg2)
                
                if expr_key in expressions:
                    # Expressão já foi calculada! Apenas copia resultado
                    prev_result = expressions[expr_key]
                    new_program.emit('assign', prev_result, None, instr.result)
                    continue
                else:
                    # Primeira vez que vemos essa expressão
                    expressions[expr_key] = instr.result
                    new_program.add(instr)
                    continue
            
            # Invalidação: se variável muda, remove expressões que a usam
            if instr.op == 'assign':
                to_remove = []
                for expr_key, result in expressions.items():
                    op, arg1, arg2 = expr_key
                    if arg1 == instr.result or arg2 == instr.result or result == instr.result:
                        to_remove.append(expr_key)
                for key in to_remove:
                    expressions.pop(key, None)
            
            # Limpa expressões entre funções
            if instr.op in ('begin_func', 'end_func'):
                expressions.clear()
            
            new_program.add(instr)
        
        return new_program


class CopyPropagation(OptimizationPass):
    """
    Copy Propagation - Propaga cópias diretas
    Exemplo: t0=a; t1=t0+b  →  t0=a; t1=a+b (usa 'a' diretamente)
    """
    
    def apply(self, ir_program):
        new_program = IRProgram()
        copies = {}  # Rastreia quem é cópia de quem
        
        for instr in ir_program.get_instructions():
            # Detecta cópias: x = y (onde y não é literal)
            if instr.op == 'assign' and not self.is_literal(instr.arg1):
                copies[instr.result] = instr.arg1
                new_program.add(instr)
                continue
            
            # Substitui cópias pelos valores originais
            new_instr = TAC(instr.op, instr.arg1, instr.arg2, instr.result)
            
            if isinstance(new_instr.arg1, str) and new_instr.arg1 in copies:
                new_instr.arg1 = copies[new_instr.arg1]
            
            if isinstance(new_instr.arg2, str) and new_instr.arg2 in copies:
                new_instr.arg2 = copies[new_instr.arg2]
            
            new_program.add(new_instr)
            
            # Invalida cópia se variável é reatribuída
            if new_instr.result:
                copies.pop(new_instr.result, None)
        
        return new_program
    
    def is_literal(self, value):
        try:
            int(value)
            return True
        except (ValueError, TypeError):
            return False