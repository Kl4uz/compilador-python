"""
CodeGen - Orquestrador do Backend do Compilador
Coordena: IR Generation → Optimizations → Assembly Generation
"""
from ..ir import IRGenerator
from ..optimizer import Optimizer, ConstantFolding, DeadCodeElimination, CopyPropagation, CommonSubexpressionElimination
from ..optimizer import PeepholeOptimizer, AlgebraicSimplification
from .assembly import AssemblyGenerator


class CodeGenerator:
    """
    Gerenciador do Pipeline de Geração de Código
    
    Responsabilidades:
    1. Gerar IR (Three-Address Code) da AST
    2. Aplicar otimizações (6 tipos)
    3. Gerar código assembly genérico
    """
    
    def __init__(self, symbol_table, enable_optimizations=True):
        self.symbol_table = symbol_table
        self.enable_optimizations = enable_optimizations
        self.ir_program = None            # IR original não otimizado
        self.algebraic_ir = None          # IR após simplificação algébrica pura
        self.optimized_ir = None          # IR totalmente otimizado
        self.assembly_code = None         # Código assembly final
    
    def generate(self, ast):
        """
        Pipeline completo de geração de código:
        AST -> IR -> Otimizações -> Assembly
        
        Retorna: (ir_program, optimized_ir, assembly_code)
        """
        # 1. Geração de IR
        print("\n[1/4] Gerando código intermediário (IR)...")
        ir_generator = IRGenerator(self.symbol_table)
        self.ir_program = ir_generator.generate(ast)
        
        # 2. Otimizações (se habilitadas)
        if self.enable_optimizations:
            print("[2/4] Aplicando otimizações...")
            self.optimized_ir = self.optimize(self.ir_program)
        else:
            print("[2/4] Otimizações desabilitadas")
            self.optimized_ir = self.ir_program
        
        # 3. Geração de Assembly
        print("[3/4] Gerando código assembly...")
        asm_generator = AssemblyGenerator()
        self.assembly_code = asm_generator.generate(self.optimized_ir)
        
        print("[4/4] Geração de código concluída ✓")
        
        return self.ir_program, self.optimized_ir, self.assembly_code
    
    def optimize(self, ir_program):
        """
        Pipeline de Otimizações em 2 Fases
        
        FASE 1 (Algébrica): Simplificação SIMBÓLICA - não usa valores numéricos
                           Mostra padrões matemáticos puros (a+b calculado 2x, c-c→0)
        
        FASE 2 (Completa): Multi-pass até convergir (max 5 passadas)
                          Usa valores conhecidos para constant folding
        """
        # Detecta se todas variáveis user são 0 (modo simbólico completo)
        all_vars_zero = self._check_all_vars_zero(ir_program)
        
        # ═══ FASE 1: SIMPLIFICAÇÃO ALGÉBRICA SIMBÓLICA ═══
        # Para fins educacionais: mostra otimização sem "colar" valores
        algebraic_opt = Optimizer()
        algebraic_opt.add_optimization(AlgebraicSimplification())  # c-c→0, f/f→1
        algebraic_opt.add_optimization(PeepholeOptimizer(symbolic_only=True))  # a+0→a, a*2→a<<1
        algebraic_opt.add_optimization(CopyPropagation())          # t1=a; t2=t1 → t2=a
        algebraic_opt.add_optimization(CommonSubexpressionElimination())  # Detecta (a+b) duplicado
        algebraic_opt.add_optimization(DeadCodeElimination())      # Remove temporários mortos
        self.algebraic_ir = algebraic_opt.optimize(ir_program)
        
        # ═══ FASE 2: OTIMIZAÇÕES COMPLETAS (MULTI-PASS) ═══
        # Repete até convergir (nenhuma instrução removida)
        current = ir_program
        max_passes = 5
        
        for pass_num in range(max_passes):
            optimizer = Optimizer()
            
            # Ordem de otimizações segue teoria clássica de compiladores
            optimizer.add_optimization(AlgebraicSimplification())    # Padrões matemáticos
            optimizer.add_optimization(ConstantFolding(symbolic_only=all_vars_zero))  # Calcula constantes
            optimizer.add_optimization(PeepholeOptimizer())          # Padrões locais + shift
            optimizer.add_optimization(CommonSubexpressionElimination())  # Elimina duplicatas
            optimizer.add_optimization(CopyPropagation())            # Propaga cópias
            optimizer.add_optimization(DeadCodeElimination())        # Remove código morto
            
            optimized = optimizer.optimize(current)
            
            # Convergência: se nada mudou, para
            if len(optimized.get_instructions()) == len(current.get_instructions()):
                break
            
            current = optimized
        
        return current
    
    def _check_all_vars_zero(self, ir_program):
        """
        Detecta modo simbólico: todas variáveis user = 0?
        Se sim, ConstantFolding não deve propagar (queremos ver álgebra pura)
        """
        for instr in ir_program.get_instructions():
            if instr.op == 'assign':
                # Variável user (não temp) com valor != 0
                if instr.result and not instr.result.startswith('t'):
                    if instr.arg1 != '0' and instr.arg1 != 0:
                        return False
        return True
    
    def print_ir(self):
        """Imprime IR original"""
        if self.ir_program:
            print("\n=== CÓDIGO INTERMEDIÁRIO (IR) ===")
            self.ir_program.print_code()
    
    def print_optimized_ir(self):
        """Imprime IR otimizado"""
        if self.optimized_ir:
            print("\n=== CÓDIGO INTERMEDIÁRIO OTIMIZADO ===")
            self.optimized_ir.print_code()
    
    def print_assembly(self):
        """Imprime código assembly"""
        if self.assembly_code:
            print("\n=== CÓDIGO ASSEMBLY ===")
            for line in self.assembly_code:
                print(line)
            print("=======================\n")
    
    def save_ir(self, filename):
        """Salva IR em arquivo"""
        with open(filename, 'w') as f:
            for instr in self.ir_program.get_instructions():
                f.write(str(instr) + '\n')
        print(f"IR salvo em: {filename}")
    
    def save_assembly(self, filename):
        """Salva assembly em arquivo"""
        with open(filename, 'w') as f:
            for line in self.assembly_code:
                f.write(line + '\n')
        print(f"Assembly salvo em: {filename}")