"""
Interpretador/Simulador de Execução
Executa código TAC usando Runtime Stack e Activation Records
Etapa 7 - Ambientes de Execução
"""
from typing import Any
from runtime import ActivationRecord, RuntimeStack

class TACInterpreter:
    """Interpretador para código TAC (Three Address Code)"""
    
    def __init__(self, tac_code):
        self.code = tac_code
        self.pc = 0  # Program Counter
        self.runtime = RuntimeStack()
        self.functions = {}  # Mapeia nome -> índice de início da função
        self.return_value: int | float | None = None
        
        # Indexa as funções
        self._index_functions()
    
    def _index_functions(self):
        """Indexa as posições das funções no código"""
        for i, instr in enumerate(self.code):
            if instr.startswith("FUNCTION "):
                func_name = instr.replace("FUNCTION ", "").replace(":", "").strip()
                self.functions[func_name] = i
    
    def execute(self):
        """Executa o código TAC"""
        print("\n========== EXECUÇÃO DO PROGRAMA ==========\n")
        
        # Começa executando main()
        if 'main' in self.functions:
            self._call_function('main', [])
        else:
            print("Erro: Função 'main' não encontrada")
            return
        
        print("\n========== FIM DA EXECUÇÃO ==========\n")
    
    def _call_function(self, func_name, args):
        """Chama uma função"""
        if func_name not in self.functions:
            raise Exception(f"Erro: Função '{func_name}' não encontrada")
        
        # Cria novo Activation Record
        ar = ActivationRecord(func_name, return_address=self.pc)
        self.runtime.push(ar)
        
        # Posiciona PC no início da função
        self.pc = self.functions[func_name] + 1  # +1 para pular o FUNCTION
        
        # Executa instruções da função
        param_index = 0
        while self.pc < len(self.code):
            instr = self.code[self.pc].strip()
            
            # Pula linhas vazias
            if not instr:
                self.pc += 1
                continue
            
            # BEGIN_FUNC
            if instr == "BEGIN_FUNC":
                self.pc += 1
                continue
            
            # PARAM - define parâmetros
            if instr.startswith("PARAM "):
                param_name = instr.replace("PARAM ", "")
                if param_index < len(args):
                    ar.set_parameter(param_name, args[param_index])
                    param_index += 1
                self.pc += 1
                continue
            
            # END_FUNC - termina função
            if instr == "END_FUNC":
                break
            
            # RETURN
            if instr.startswith("RETURN"):
                parts = instr.split()
                if len(parts) > 1:
                    return_val = self._get_value(parts[1])
                    setattr(ar, "return_value", return_val)
                    self.return_value = return_val
                break
            
            # Atribuição simples: x = valor
            if " = " in instr and "CALL" not in instr and "+" not in instr and "-" not in instr and "*" not in instr and "/" not in instr:
                parts = instr.split(" = ")
                var_name = parts[0]
                value = self._get_value(parts[1])
                self.runtime.set_value(var_name, value)
                self.pc += 1
                continue
            
            # Operações aritméticas: t1 = a + b
            if " = " in instr and any(op in instr for op in [" + ", " - ", " * ", " / "]):
                parts = instr.split(" = ")
                temp_var = parts[0]
                expr = parts[1]
                
                # Detecta operador
                op = None
                for operator in [" + ", " - ", " * ", " / "]:
                    if operator in expr:
                        op = operator.strip()
                        left, right = expr.split(operator)
                        break
                
                left_val = self._get_value(left.strip())
                right_val = self._get_value(right.strip())
                
                # Calcula resultado
                if op == '+':
                    result = left_val + right_val
                elif op == '-':
                    result = left_val - right_val
                elif op == '*':
                    result = left_val * right_val
                elif op == '/':
                    result = left_val / right_val
                
                self.runtime.set_temporary(temp_var, result)
                self.pc += 1
                continue
            
            # PRINT
            if instr.startswith("PRINT "):
                value_name = instr.replace("PRINT ", "")
                value = self._get_value(value_name)
                print(f">>> OUTPUT: {value}")
                self.pc += 1
                continue
            
            # ARG - empilha argumento para chamada
            if instr.startswith("ARG "):
                # Argumentos são processados na chamada
                self.pc += 1
                continue
            
            # CALL: t1 = CALL func, n
            if "CALL " in instr:
                parts = instr.split(" = CALL ")
                result_var = parts[0]
                call_parts = parts[1].split(", ")
                called_func = call_parts[0]
                num_args = int(call_parts[1])
                
                # Coleta argumentos (instruções ARG anteriores)
                args = []
                for i in range(self.pc - num_args, self.pc):
                    arg_instr = self.code[i].strip()
                    if arg_instr.startswith("ARG "):
                        arg_value = self._get_value(arg_instr.replace("ARG ", ""))
                        args.append(arg_value)
                
                # Chama função recursivamente
                saved_pc = self.pc
                self._call_function(called_func, args)
                self.pc = saved_pc
                
                # Armazena valor de retorno
                self.runtime.set_temporary(result_var, self.return_value)
                self.pc += 1
                continue
            
            # Avança PC
            self.pc += 1
        
        # Desempilha AR
        returned_ar = self.runtime.pop()
        self.return_value = returned_ar.return_value
        
        # Imprime estado da pilha
        self.runtime.print_stack()
    
    def _get_value(self, name):
        """Obtém o valor de uma variável ou constante"""
        # Tenta converter para número
        try:
            return int(name)
        except ValueError:
            pass
        
        try:
            return float(name)
        except ValueError:
            pass
        
        # Senão, busca na runtime stack
        return self.runtime.get_value(name)


# Teste
if __name__ == "__main__":
    # Código TAC de exemplo (gerado pelo codegen_full.py)
    tac_code = [
        "FUNCTION soma:",
        "BEGIN_FUNC",
        "PARAM a",
        "PARAM b",
        "t1 = a + b",
        "r = t1",
        "RETURN r",
        "END_FUNC",
        "",
        "FUNCTION main:",
        "BEGIN_FUNC",
        "ARG 2",
        "ARG 3",
        "t2 = CALL soma, 2",
        "x = t2",
        "PRINT x",
        "RETURN 0",
        "END_FUNC"
    ]
    
    print("=== CÓDIGO TAC ===")
    for line in tac_code:
        if line:
            print(line)
    print("==================\n")
    
    # Executa
    interpreter = TACInterpreter(tac_code)
    interpreter.execute()
