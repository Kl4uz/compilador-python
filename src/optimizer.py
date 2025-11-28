"""
Otimizador de Código Intermediário
Aplica otimizações no código IR gerado
"""

from typing import List
from .ir_generator import IRInstruction, IRGenerator


class Optimizer:
    """
    Otimizador de código intermediário
    Aplica várias otimizações no código IR
    """
    
    def __init__(self):
        self.optimizations_applied = []
    
    def optimize(self, instructions: List[IRInstruction]) -> List[IRInstruction]:
        """
        Aplica todas as otimizações disponíveis
        """
        optimized = list(instructions)
        
        # Aplica otimizações em sequência
        optimized = self._remove_dead_code(optimized)
        optimized = self._constant_folding(optimized)
        optimized = self._remove_redundant_assignments(optimized)
        optimized = self._remove_unused_temps(optimized)
        
        return optimized
    
    def _constant_folding(self, instructions: List[IRInstruction]) -> List[IRInstruction]:
        """
        Otimização: Constant Folding
        Avalia expressões constantes em tempo de compilação
        Ex: t1 = 5 + 3 -> t1 = 8
        """
        optimized = []
        constant_map = {}  # Mapeia temporários para valores constantes
        
        for instr in instructions:
            if instr.op in ("+", "-", "*", "/"):
                # Tenta avaliar se ambos os operandos são constantes
                arg1_val = self._get_constant_value(instr.arg1, constant_map)
                arg2_val = self._get_constant_value(instr.arg2, constant_map)
                
                if arg1_val is not None and arg2_val is not None:
                    # Avalia a expressão
                    try:
                        if instr.op == "+":
                            result_val = arg1_val + arg2_val
                        elif instr.op == "-":
                            result_val = arg1_val - arg2_val
                        elif instr.op == "*":
                            result_val = arg1_val * arg2_val
                        elif instr.op == "/":
                            if arg2_val == 0:
                                optimized.append(instr)  # Mantém divisão por zero
                                continue
                            result_val = arg1_val // arg2_val  # Divisão inteira
                        else:
                            optimized.append(instr)
                            continue
                        
                        # Substitui por atribuição de constante
                        constant_map[instr.result] = result_val
                        optimized.append(IRInstruction("=", arg1=str(result_val), result=instr.result))
                        self.optimizations_applied.append(f"Constant folding: {instr.result} = {arg1_val} {instr.op} {arg2_val} -> {result_val}")
                        continue
                    except (ValueError, TypeError):
                        pass
            
            optimized.append(instr)
        
        return optimized
    
    def _get_constant_value(self, value: str, constant_map: dict) -> int:
        """
        Retorna o valor constante de um operando, se disponível
        """
        if value is None:
            return None
        
        # Tenta converter diretamente
        try:
            return int(value)
        except (ValueError, TypeError):
            pass
        
        # Verifica no mapa de constantes
        if value in constant_map:
            return constant_map[value]
        
        return None
    
    def _remove_redundant_assignments(self, instructions: List[IRInstruction]) -> List[IRInstruction]:
        """
        Otimização: Remove atribuições redundantes
        Ex: x = x -> (remove)
        """
        optimized = []
        
        for instr in instructions:
            if instr.op == "=" and instr.arg1 == instr.result:
                # Atribuição redundante: x = x
                self.optimizations_applied.append(f"Removed redundant assignment: {instr.result} = {instr.arg1}")
                continue
            
            optimized.append(instr)
        
        return optimized
    
    def _remove_unused_temps(self, instructions: List[IRInstruction]) -> List[IRInstruction]:
        """
        Otimização: Remove variáveis temporárias não utilizadas
        """
        # Primeiro, identifica quais temporários são usados
        used_temps = set()
        
        for instr in instructions:
            # Verifica se o resultado é usado em outras instruções
            if instr.result and instr.result.startswith('t'):
                # Verifica se é usado posteriormente
                for later_instr in instructions:
                    if later_instr != instr:
                        if (later_instr.arg1 == instr.result or 
                            later_instr.arg2 == instr.result):
                            used_temps.add(instr.result)
                            break
            
            # Também marca como usado se for usado em print, return, etc
            if instr.op in ("print", "RETURN", "ARG"):
                if instr.arg1 and instr.arg1.startswith('t'):
                    used_temps.add(instr.arg1)
        
        # Remove instruções que definem temporários não usados
        optimized = []
        for instr in instructions:
            if (instr.result and instr.result.startswith('t') and 
                instr.result not in used_temps and
                instr.op not in ("FUNCTION", "BEGIN_FUNC", "END_FUNC", "PARAM", "ARG", "CALL", "RETURN")):
                self.optimizations_applied.append(f"Removed unused temp: {instr.result}")
                continue
            
            optimized.append(instr)
        
        return optimized
    
    def _remove_dead_code(self, instructions: List[IRInstruction]) -> List[IRInstruction]:
        """
        Otimização: Remove código morto (após return inalcançável)
        """
        optimized = []
        found_return = False
        
        for instr in instructions:
            if found_return and instr.op not in ("FUNCTION", "BEGIN_FUNC", "END_FUNC"):
                # Código após return na mesma função (simplificado)
                continue
            
            if instr.op == "RETURN":
                found_return = True
            
            if instr.op == "FUNCTION":
                found_return = False  # Nova função
            
            optimized.append(instr)
        
        return optimized
    
    def get_optimization_report(self) -> str:
        """Retorna relatório das otimizações aplicadas"""
        if not self.optimizations_applied:
            return "Nenhuma otimização aplicada."
        
        report = f"Otimizações aplicadas ({len(self.optimizations_applied)}):\n"
        for opt in self.optimizations_applied:
            report += f"  - {opt}\n"
        return report

