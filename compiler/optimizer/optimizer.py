"""
Optimizer - Framework de Otimização
Coordena diferentes passes de otimização no código IR
"""
from ..ir import IRProgram, TAC


class Optimizer:
    """Framework de otimização para código IR"""
    
    def __init__(self):
        self.optimizations = []
    
    def add_optimization(self, optimization):
        """Adiciona um passe de otimização"""
        self.optimizations.append(optimization)
    
    def optimize(self, ir_program):
        """
        Aplica todas as otimizações no programa IR
        Retorna: IRProgram otimizado
        """
        optimized = ir_program
        
        for optimization in self.optimizations:
            print(f"Aplicando: {optimization.__class__.__name__}")
            optimized = optimization.apply(optimized)
        
        return optimized


class OptimizationPass:
    """Classe base para passes de otimização"""
    
    def apply(self, ir_program):
        """
        Aplica a otimização
        Deve retornar um novo IRProgram
        """
        raise NotImplementedError("Subclasse deve implementar apply()")


class ConstantFolding(OptimizationPass):
    """Otimização: constant folding (avalia operações em tempo de compilação)"""
    
    def apply(self, ir_program):
        """Aplica constant folding"""
        new_program = IRProgram()
        
        for instr in ir_program.get_instructions():
            # Se é operação aritmética com dois literais
            if instr.op in ('+', '-', '*', '/'):
                if self.is_literal(instr.arg1) and self.is_literal(instr.arg2):
                    # Avalia em tempo de compilação
                    value = self.evaluate(instr.op, instr.arg1, instr.arg2)
                    # Substitui por atribuição direta
                    new_program.emit('assign', str(value), None, instr.result)
                    continue
            
            # Senão, mantém instrução original
            new_program.add(instr)
        
        return new_program
    
    def is_literal(self, value):
        """Verifica se é literal numérico"""
        try:
            int(value)
            return True
        except (ValueError, TypeError):
            return False
    
    def evaluate(self, op, arg1, arg2):
        """Avalia operação com literais"""
        a = int(arg1)
        b = int(arg2)
        
        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '*':
            return a * b
        elif op == '/':
            return a // b  # Divisão inteira
        else:
            raise ValueError(f"Operador não suportado: {op}")


class DeadCodeElimination(OptimizationPass):
    """Otimização: eliminação de código morto"""
    
    def apply(self, ir_program):
        """Remove código após return"""
        new_program = IRProgram()
        
        in_dead_code = False
        for instr in ir_program.get_instructions():
            # Se encontrou return, marca código seguinte como morto
            if instr.op == 'return':
                new_program.add(instr)
                in_dead_code = True
                continue
            
            # Se encontrou nova função, código volta a ser vivo
            if instr.op in ('begin_func', 'end_func'):
                in_dead_code = False
            
            # Adiciona só se não for código morto
            if not in_dead_code:
                new_program.add(instr)
        
        return new_program


class CommonSubexpressionElimination(OptimizationPass):
    """
    Otimização: Eliminação de Subexpressões Comuns (CSE)
    Conforme professor ensinou: reutiliza resultado de expressões já calculadas
    
    Exemplo:
        t1 = a + b
        t2 = a + b  <- redundante, usa t1
        
    Fica:
        t1 = a + b
        t2 = t1     <- reutiliza
    """
    
    def apply(self, ir_program):
        """Aplica CSE"""
        new_program = IRProgram()
        # Mapa: (op, arg1, arg2) -> variável que contém resultado
        expressions = {}
        
        for instr in ir_program.get_instructions():
            # Operações que podem ser reutilizadas
            if instr.op in ('+', '-', '*', '/'):
                # Cria chave única para expressão
                expr_key = (instr.op, instr.arg1, instr.arg2)
                
                # Se expressão já foi calculada
                if expr_key in expressions:
                    # Reutiliza resultado anterior
                    prev_result = expressions[expr_key]
                    new_program.emit('assign', prev_result, None, instr.result)
                    continue
                else:
                    # Primeira vez que vê essa expressão, registra
                    expressions[expr_key] = instr.result
                    new_program.add(instr)
                    continue
            
            # Limpa mapa se variável é redefinida
            if instr.op == 'assign' or instr.op in ('decl_assign',):
                # Remove expressões que usam essa variável
                to_remove = []
                for expr_key, result in expressions.items():
                    op, arg1, arg2 = expr_key
                    if arg1 == instr.result or arg2 == instr.result or result == instr.result:
                        to_remove.append(expr_key)
                
                for key in to_remove:
                    expressions.pop(key, None)
            
            # Reseta ao entrar em nova função
            if instr.op in ('begin_func', 'end_func'):
                expressions.clear()
            
            # Adiciona instrução normal
            new_program.add(instr)
        
        return new_program


class CopyPropagation(OptimizationPass):
    """Otimização: propagação de cópias"""
    
    def apply(self, ir_program):
        """Propaga cópias simples (x = y => substitui x por y)"""
        new_program = IRProgram()
        copies = {}  # mapa: variável -> valor copiado
        
        for instr in ir_program.get_instructions():
            # Detecta cópias simples
            if instr.op == 'assign' and not self.is_literal(instr.arg1):
                # x = y (cópia simples)
                copies[instr.result] = instr.arg1
                new_program.add(instr)
                continue
            
            # Substitui usos de variáveis copiadas
            new_instr = TAC(instr.op, instr.arg1, instr.arg2, instr.result)
            
            # Só substitui se não for lista (arg2 pode ser lista em 'call')
            if isinstance(new_instr.arg1, str) and new_instr.arg1 in copies:
                new_instr.arg1 = copies[new_instr.arg1]
            
            if isinstance(new_instr.arg2, str) and new_instr.arg2 in copies:
                new_instr.arg2 = copies[new_instr.arg2]
            
            new_program.add(new_instr)
            
            # Se variável é redefinida, remove do mapa de cópias
            if new_instr.result:
                copies.pop(new_instr.result, None)
        
        return new_program
    
    def is_literal(self, value):
        """Verifica se é literal"""
        try:
            int(value)
            return True
        except (ValueError, TypeError):
            return False


# Para testes
if __name__ == "__main__":
    from ir import IRProgram
    
    # Cria programa de teste
    ir = IRProgram()
    
    # Constant folding: 5 + 3 => 8
    ir.emit('+', '5', '3', 't1')
    ir.emit('assign', 't1', None, 'x')
    
    # Copy propagation: y = x
    ir.emit('assign', 'x', None, 'y')
    ir.emit('print', 'y')
    
    # Dead code após return
    ir.emit('return', '0')
    ir.emit('print', 'x')  # código morto
    
    print("=== CÓDIGO ORIGINAL ===")
    ir.print_code()
    
    # Aplica otimizações
    optimizer = Optimizer()
    optimizer.add_optimization(ConstantFolding())
    optimizer.add_optimization(CopyPropagation())
    optimizer.add_optimization(DeadCodeElimination())
    
    optimized = optimizer.optimize(ir)
    
    print("\n=== CÓDIGO OTIMIZADO ===")
    optimized.print_code()
