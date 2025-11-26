"""
CodeGen - Coordenador de Geração de Código
Integra IR generation, otimização e geração de assembly
"""
from ..ir import IRGenerator
from ..optimizer import Optimizer, ConstantFolding, DeadCodeElimination, CopyPropagation, CommonSubexpressionElimination
from ..optimizer import PeepholeOptimizer, AlgebraicSimplification
from .assembly import AssemblyGenerator


class CodeGenerator:
    """
    Coordenador principal de geração de código
    Integra todas as fases de backend do compilador
    """
    
    def __init__(self, symbol_table, enable_optimizations=True):
        self.symbol_table = symbol_table
        self.enable_optimizations = enable_optimizations
        self.ir_program = None
        self.optimized_ir = None
        self.assembly_code = None
    
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
        Aplica pipeline de otimizações conforme professor ensinou
        """
        optimizer = Optimizer()
        
        # Adiciona otimizações em ordem estratégica
        optimizer.add_optimization(CommonSubexpressionElimination())  # CSE primeiro
        optimizer.add_optimization(ConstantFolding())
        optimizer.add_optimization(AlgebraicSimplification())
        optimizer.add_optimization(PeepholeOptimizer())
        optimizer.add_optimization(CopyPropagation())
        optimizer.add_optimization(DeadCodeElimination())
        
        return optimizer.optimize(ir_program)
    
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


# Para testes
if __name__ == "__main__":
    from parser import parse_from_code
    from ast import build_ast
    from analyzer import SemanticAnalyzer
    
    test_code = """
    int soma(int a, int b) {
        int r = a + b;
        return r;
    }
    
    int main() {
        int x = 5;
        int y = soma(x, 3);
        print(y);
        return 0;
    }
    """
    
    print("=== TESTE DO CODEGEN ===")
    print("Código fonte:")
    print(test_code)
    
    # Parse
    parse_tree = parse_from_code(test_code)
    ast = build_ast(parse_tree)
    
    # Análise semântica
    analyzer = SemanticAnalyzer()
    success, errors, symbol_table = analyzer.analyze(ast)
    
    if not success:
        print("\nErros semânticos:")
        for error in errors:
            print(f"  - {error}")
    else:
        # Geração de código
        codegen = CodeGenerator(symbol_table, enable_optimizations=True)
        ir_program, optimized_ir, assembly = codegen.generate(ast)
        
        # Imprime resultados
        codegen.print_ir()
        codegen.print_optimized_ir()
        codegen.print_assembly()
