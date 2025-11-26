"""
Ambientes de Execução - Etapa 7
Implementação de Activation Records e Runtime Stack
"""

import os
from typing import Any, Dict, List

class ActivationRecord:
    """
    Registro de Ativação (Stack Frame)
    Contém todas as informações necessárias para execução de uma função
    """
    def __init__(self, function_name, return_address=None):
        self.function_name = function_name
        self.parameters = {}          # nome -> valor dos parâmetros formais
        self.local_variables = {}     # nome -> valor das variáveis locais
        self.return_value = Any = None      # valor de retorno da função
        self.dynamic_link = None      # ponteiro para o AR do chamador (pilha)
        self.static_link = None       # ponteiro para o AR do escopo léxico pai
        self.return_address = return_address  # endereço de retorno após chamada
        self.temporaries = {}         # variáveis temporárias (t1, t2, etc)
    
    def set_parameter(self, name, value):
        """Define o valor de um parâmetro"""
        self.parameters[name] = value
    
    def set_local(self, name, value):
        """Define o valor de uma variável local"""
        self.local_variables[name] = value
    
    def get_value(self, name):
        """Busca o valor de uma variável **somente neste AR** (parâmetro, local ou temporária)"""
        if name in self.parameters:
            return self.parameters[name]
        if name in self.local_variables:
            return self.local_variables[name]
        if name in self.temporaries:
            return self.temporaries[name]
        return None
    
    def set_temporary(self, name, value):
        """Define o valor de uma variável temporária"""
        self.temporaries[name] = value
    
    def __repr__(self):
        return (f"AR[{self.function_name}]\n"
                f"  Params: {self.parameters}\n"
                f"  Locals: {self.local_variables}\n"
                f"  Return: {self.return_value: int | float | None = None}\n"
                f"  Temps: {self.temporaries}")


class RuntimeStack:
    """
    Pilha de Execução
    Gerencia os Activation Records durante a execução do programa
    """
    def __init__(self):
        self.stack = []
        self.global_memory = {}  # Memória para variáveis globais
    
    def push(self, activation_record):
        """
        Empilha um novo Activation Record
        Configura o dynamic link para o AR anterior
        """
        if self.stack:
            activation_record.dynamic_link = self.stack[-1]
        self.stack.append(activation_record)
        print(f"[PUSH] Empilhando AR para '{activation_record.function_name}' (profundidade: {len(self.stack)})")
    
    def pop(self):
        """
        Desempilha o Activation Record do topo
        Retorna o AR removido
        """
        if not self.stack:
            raise Exception("Erro: Tentativa de desempilhar de uma pilha vazia")
        
        ar = self.stack.pop()
        print(f"[POP] Desempilhando AR de '{ar.function_name}' (profundidade: {len(self.stack)})")
        return ar
    
    def current_frame(self):
        """Retorna o Activation Record do topo (função atual)"""
        if not self.stack:
            return None
        return self.stack[-1]
    
    def get_value(self, name):
        """
        Busca o valor de uma variável:
         1) AR atual
         2) percorre dynamic_link (chamadores) até encontrar
         3) memória global
        Se não encontrado, lança Exceção.
        """
        # Se for número literal passado por engano (ex.: get_value(3)), retorna direto
        if isinstance(name, (int, float)):
            return name

        # Tenta no AR atual
        current_ar = self.current_frame()
        if current_ar is not None:
            value = current_ar.get_value(name)
            if value is not None:
                return value

            # Percorre os ARs dos chamadores via dynamic_link
            ar = current_ar.dynamic_link
            while ar is not None:
                v = ar.get_value(name)
                if v is not None:
                    return v
                ar = ar.dynamic_link

        # Se não encontrou em nenhum frame, busca na memória global
        if name in self.global_memory:
            return self.global_memory[name]
        
        # Não encontrado
        raise Exception(f"Erro: Variável '{name}' não encontrada")
    
    def set_value(self, name, value):
        """
        Define o valor de uma variável
        No AR atual (se houver) ou na memória global
        Se já existe como parâmetro ou local no AR atual, atualiza.
        Senão, cria como variável local no AR atual.
        """
        current_ar = self.current_frame()
        if current_ar is not None:
            # Se já existe no AR atual, atualiza o local/parâmetro
            if name in current_ar.parameters:
                current_ar.set_parameter(name, value)
                return
            if name in current_ar.local_variables:
                current_ar.set_local(name, value)
                return
            # Senão, cria como local no AR atual
            current_ar.set_local(name, value)
        else:
            # Sem AR, armazena como global
            self.global_memory[name] = value
    
    def set_temporary(self, name, value):
        """Define o valor de uma variável temporária no AR atual"""
        current_ar = self.current_frame()
        if current_ar is not None:
            current_ar.set_temporary(name, value)
        else:
            self.global_memory[name] = value
    
    def print_stack(self):
        """Imprime o estado atual da pilha de execução"""
        print("\n========== RUNTIME STACK ==========")
        print(f"Profundidade: {len(self.stack)}")
        
        if self.global_memory:
            print("\n[MEMÓRIA GLOBAL]")
            for name, value in self.global_memory.items():
                print(f"  {name} = {value}")
        
        if not self.stack:
            print("\n(Pilha vazia)")
        else:
            print(f"\n[TOPO DA PILHA]")
            for i in range(len(self.stack) - 1, -1, -1):
                ar = self.stack[i]
                print(f"\n--- Frame {i}: {ar.function_name} ---")
                if ar.parameters:
                    print(f"  Parâmetros: {ar.parameters}")
                if ar.local_variables:
                    print(f"  Locais: {ar.local_variables}")
                if ar.temporaries:
                    print(f"  Temporárias: {ar.temporaries}")
                if ar.return_value is not None:
                    print(f"  Retorno: {ar.return_value}")
        
        print("\n===================================\n")


# Função de alto-nível que simula a soma usando o RuntimeStack
def simulate_soma(runtime, a, b):
    """Simula: soma(a,b) dentro de main, retorna o resultado"""
    # empilha soma
    soma_ar = ActivationRecord("soma", return_address="main+ret")
    soma_ar.set_parameter("a", a)
    soma_ar.set_parameter("b", b)
    runtime.push(soma_ar)

    # executa r = a + b usando runtime
    aval = runtime.get_value("a")
    bval = runtime.get_value("b")
    r = aval + bval
    # guarda r como variável local em soma
    runtime.set_value("r", r)
    runtime.print_stack()

    # retorno de soma
    popped = runtime.pop()
    popped.return_value = r
    print(f"[soma] retornando valor: {popped.return_value}")
    return popped.return_value


# Testes
if __name__ == "__main__":
    print("=== TESTE: Simulação de Chamada de Função ===\n")
    
    # Cria a runtime stack
    runtime = RuntimeStack()
    
    # Simula variáveis globais
    runtime.global_memory['global_var'] = 100
    
    print("1. Estado inicial:")
    runtime.print_stack()
    
    # Simula chamada de main()
    print("2. Chamando main()...")
    main_ar = ActivationRecord("main")
    runtime.push(main_ar)
    runtime.print_stack()
    
    # Simula chamada de soma(2, 3) dentro de main
    print("3. Chamando soma(2, 3) dentro de main...")
    soma_ar = ActivationRecord("soma", return_address="main+5")
    soma_ar.set_parameter("a", 2)
    soma_ar.set_parameter("b", 3)
    runtime.push(soma_ar)
    runtime.print_stack()
    
    # Executa soma: r = a + b
    print("4. Executando r = a + b dentro de soma...")
    a = runtime.get_value("a")
    b = runtime.get_value("b")
    r = a + b
    runtime.set_value("r", r)
    runtime.print_stack()
    
    # Return de soma
    print("5. Retornando de soma()...")
    soma_ar = runtime.pop()
    soma_ar.return_value = r
    print(f"Valor retornado: {soma_ar.return_value}")
    
    # Atribui o resultado em main
    print("6. Atribuindo resultado em x dentro de main...")
    runtime.set_value("x", soma_ar.return_value)
    runtime.print_stack()
    
    # Return de main
    print("7. Retornando de main()...")
    runtime.pop()
    runtime.print_stack()
    
    print("=== FIM DO TESTE ===")
