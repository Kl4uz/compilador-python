"""
Pipeline Principal do Compilador
Orquestra todas as fases de compilação: lexer -> parser -> semantic -> IR -> optimizer -> assembly
"""

from typing import Optional, Dict, Any
from .lexer import lexer
from .parser import parser
from .semantic import SemanticAnalyzer
from .ir_generator import IRGenerator
from .optimizer import Optimizer
from .assembly_generator import AssemblyGenerator
from .symbol_table import SymbolTable
from .ast_builder import ASTNode, tuple_to_ast


class CompilationError(Exception):
    """Exceção para erros de compilação"""
    def __init__(self, phase: str, message: str):
        self.phase = phase
        self.message = message
        super().__init__(f"[{phase}] {message}")


class Compiler:
    """
    Pipeline principal do compilador
    Executa todas as fases de compilação em sequência
    """
    
    def __init__(self, optimize: bool = True, generate_assembly: bool = False):
        self.optimize = optimize
        self.generate_assembly = generate_assembly
        self.symbol_table = SymbolTable()
        self.ast: Optional[ASTNode] = None
        self.ir_instructions = []
        self.optimized_ir = []
        self.assembly_code = []
        self.errors = []
        self.warnings = []
    
    def compile(self, source_code: str) -> Dict[str, Any]:
        """
        Compila o código fonte
        Retorna um dicionário com os resultados de cada fase
        """
        self.errors = []
        self.warnings = []
        
        try:
            # Fase 1: Análise Léxica
            tokens = self._lexical_analysis(source_code)
            if self.errors:
                return self._build_result()
            
            # Fase 2: Análise Sintática
            ast_tuple = self._syntactic_analysis(source_code)
            if self.errors:
                return self._build_result()
            
            # Converte tupla para ASTNode
            self.ast = tuple_to_ast(ast_tuple) if ast_tuple else None
            
            # Fase 3: Análise Semântica
            self._semantic_analysis()
            if self.errors:
                return self._build_result()
            
            # Fase 4: Geração de Código Intermediário
            self._ir_generation()
            if self.errors:
                return self._build_result()
            
            # Fase 5: Otimização (opcional)
            if self.optimize:
                self._optimization()
            
            # Fase 6: Geração de Assembly (opcional)
            if self.generate_assembly:
                self._assembly_generation()
            
            return self._build_result()
        
        except CompilationError as e:
            self.errors.append(str(e))
            return self._build_result()
        except Exception as e:
            self.errors.append(f"Erro inesperado: {str(e)}")
            return self._build_result()
    
    def _lexical_analysis(self, source_code: str) -> list:
        """Fase 1: Análise Léxica"""
        try:
            lexer.input(source_code)
            tokens = list(lexer)
            return tokens
        except Exception as e:
            self.errors.append(f"Erro léxico: {str(e)}")
            return []
    
    def _syntactic_analysis(self, source_code: str) -> Optional[tuple]:
        """Fase 2: Análise Sintática"""
        try:
            ast = parser.parse(source_code, lexer=lexer)
            return ast
        except SyntaxError as e:
            self.errors.append(f"Erro sintático: {str(e)}")
            return None
        except Exception as e:
            self.errors.append(f"Erro no parser: {str(e)}")
            return None
    
    def _semantic_analysis(self):
        """Fase 3: Análise Semântica"""
        try:
            analyzer = SemanticAnalyzer(self.symbol_table)
            analyzer.analyze(self.ast)
            self.errors.extend(analyzer.errors)
            self.warnings.extend(analyzer.warnings)
        except Exception as e:
            self.errors.append(f"Erro semântico: {str(e)}")
    
    def _ir_generation(self):
        """Fase 4: Geração de Código Intermediário"""
        try:
            generator = IRGenerator(self.symbol_table)
            self.ir_instructions = generator.generate(self.ast)
        except Exception as e:
            self.errors.append(f"Erro na geração de IR: {str(e)}")
    
    def _optimization(self):
        """Fase 5: Otimização"""
        try:
            optimizer = Optimizer()
            self.optimized_ir = optimizer.optimize(self.ir_instructions)
            if optimizer.optimizations_applied:
                self.warnings.append(optimizer.get_optimization_report())
        except Exception as e:
            self.warnings.append(f"Erro na otimização: {str(e)}")
            self.optimized_ir = self.ir_instructions
    
    def _assembly_generation(self):
        """Fase 6: Geração de Assembly"""
        try:
            ir_to_use = self.optimized_ir if self.optimize else self.ir_instructions
            generator = AssemblyGenerator()
            self.assembly_code = generator.generate(ir_to_use)
        except Exception as e:
            self.errors.append(f"Erro na geração de assembly: {str(e)}")
    
    def _build_result(self) -> Dict[str, Any]:
        """Constrói o dicionário de resultados"""
        return {
            "success": len(self.errors) == 0,
            "ast": self.ast,
            "ir": self.ir_instructions,
            "optimized_ir": self.optimized_ir if self.optimize else None,
            "assembly": self.assembly_code if self.generate_assembly else None,
            "symbol_table": self.symbol_table,
            "errors": self.errors,
            "warnings": self.warnings
        }
    
    def print_results(self, result: Dict[str, Any]):
        """Imprime os resultados da compilação"""
        print("=" * 60)
        print("RESULTADO DA COMPILAÇÃO")
        print("=" * 60)
        
        if not result["success"]:
            print("\n ERROS ENCONTRADOS:")
            for error in result["errors"]:
                print(f"  - {error}")
        
        if result["warnings"]:
            print("\n AVISOS:")
            for warning in result["warnings"]:
                print(f"  {warning}")
        
        if result["ast"]:
            print("\n AST:")
            from .ast_builder import print_ast
            print_ast(result["ast"])
        
        if result["ir"]:
            print("\n CÓDIGO INTERMEDIÁRIO (IR):")
            generator = IRGenerator()
            generator.instructions = result["ir"]
            generator.print_ir()
        
        if result["optimized_ir"]:
            print("\n⚡ CÓDIGO OTIMIZADO:")
            generator = IRGenerator()
            generator.instructions = result["optimized_ir"]
            generator.print_ir()
        
        if result["assembly"]:
            print("\n CÓDIGO ASSEMBLY:")
            for line in result["assembly"]:
                print(line)
        
        if result["symbol_table"]:
            print("\n TABELA DE SÍMBOLOS:")
            result["symbol_table"].print_table()
        
        print("=" * 60)


def compile_file(input_file: str, output_file: Optional[str] = None, 
                 optimize: bool = True, generate_assembly: bool = False) -> Dict[str, Any]:
    """
    Compila um arquivo de código fonte
    
    Args:
        input_file: Caminho do arquivo de entrada
        output_file: Caminho do arquivo de saída (opcional)
        optimize: Se True, aplica otimizações
        generate_assembly: Se True, gera código assembly
    
    Returns:
        Dicionário com resultados da compilação
    """
    with open(input_file, 'r') as f:
        source_code = f.read()
    
    compiler = Compiler(optimize=optimize, generate_assembly=generate_assembly)
    result = compiler.compile(source_code)
    
    if output_file and result["success"]:
        # Salva o código IR
        if result["optimized_ir"]:
            ir_to_save = result["optimized_ir"]
        else:
            ir_to_save = result["ir"]
        
        with open(output_file, 'w') as f:
            generator = IRGenerator()
            generator.instructions = ir_to_save
            f.write(generator.get_ir_string())
    
    return result


if __name__ == "__main__":
    # Exemplo de uso
    code = """
int soma(int a, int b) {
    int r = a + b;
    return r;
}

int main() {
    int x = soma(2, 3);
    print(x);
    return 0;
}
"""
    
    compiler = Compiler(optimize=True, generate_assembly=False)
    result = compiler.compile(code)
    compiler.print_results(result)

