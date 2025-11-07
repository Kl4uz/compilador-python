"""
Tabela de Símbolos com suporte a Escopos Aninhados
Etapa 7 - Ambientes de Execução
"""

class Symbol:
    """Representa um símbolo na tabela"""
    def __init__(self, name, symbol_type, scope, offset=0, is_param=False):
        self.name = name
        self.type = symbol_type
        self.scope = scope
        self.offset = offset  # Offset no activation record
        self.is_param = is_param
    
    def __repr__(self):
        return f"Symbol({self.name}, {self.type}, scope={self.scope}, offset={self.offset}, param={self.is_param})"


class Scope:
    """Representa um escopo (global ou local de função)"""
    def __init__(self, name, parent=None, level=0):
        self.name = name
        self.parent = parent
        self.level = level
        self.symbols = {}  # nome -> Symbol
        self.offset_counter = 0  # Para calcular offsets das variáveis locais
    
    def insert(self, name, symbol_type, is_param=False):
        """Insere um novo símbolo no escopo atual"""
        if name in self.symbols:
            raise Exception(f"Erro: Variável '{name}' já declarada no escopo '{self.name}'")
        
        symbol = Symbol(name, symbol_type, self.name, self.offset_counter, is_param)
        self.symbols[name] = symbol
        self.offset_counter += 1  # Incrementa o offset para próxima variável
        return symbol
    
    def lookup_local(self, name):
        """Busca um símbolo apenas no escopo atual"""
        return self.symbols.get(name)
    
    def lookup(self, name):
        """Busca um símbolo no escopo atual e nos pais (escopo léxico)"""
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent:
            return self.parent.lookup(name)
        return None
    
    def __repr__(self):
        return f"Scope({self.name}, level={self.level}, symbols={len(self.symbols)})"


class SymbolTable:
    """Tabela de Símbolos com suporte a escopos aninhados"""
    def __init__(self):
        self.global_scope = Scope("global", parent=None, level=0)
        self.current_scope = self.global_scope
        self.scopes_stack = [self.global_scope]
    
    def enter_scope(self, scope_name):
        """Entra em um novo escopo (ex: ao entrar em uma função)"""
        new_scope = Scope(scope_name, parent=self.current_scope, level=len(self.scopes_stack))
        self.scopes_stack.append(new_scope)
        self.current_scope = new_scope
        return new_scope
    
    def exit_scope(self):
        """Sai do escopo atual (ex: ao sair de uma função)"""
        if len(self.scopes_stack) <= 1:
            raise Exception("Erro: Tentativa de sair do escopo global")
        
        self.scopes_stack.pop()
        self.current_scope = self.scopes_stack[-1]
    
    def insert(self, name, symbol_type, is_param=False):
        """Insere um símbolo no escopo atual"""
        return self.current_scope.insert(name, symbol_type, is_param)
    
    def lookup(self, name):
        """Busca um símbolo no escopo atual e nos pais"""
        return self.current_scope.lookup(name)
    
    def lookup_local(self, name):
        """Busca um símbolo apenas no escopo atual"""
        return self.current_scope.lookup_local(name)
    
    def get_current_scope_name(self):
        """Retorna o nome do escopo atual"""
        return self.current_scope.name
    
    def is_global_scope(self):
        """Verifica se está no escopo global"""
        return self.current_scope == self.global_scope
    
    def print_table(self):
        """Imprime toda a tabela de símbolos"""
        print("\n=== TABELA DE SÍMBOLOS ===")
        for scope in self.scopes_stack:
            print(f"\nEscopo: {scope.name} (Nível: {scope.level})")
            if scope.symbols:
                for name, symbol in scope.symbols.items():
                    param_str = " [PARAM]" if symbol.is_param else ""
                    print(f"  {name}: {symbol.type} (offset={symbol.offset}){param_str}")
            else:
                print("  (vazio)")
        print("========================\n")


# Testes
if __name__ == "__main__":
    st = SymbolTable()
    
    # Variáveis globais
    st.insert("global_var", "int")
    
    # Entrando na função soma
    st.enter_scope("soma")
    st.insert("a", "int", is_param=True)
    st.insert("b", "int", is_param=True)
    st.insert("r", "int")
    
    # Testando lookup
    print("Lookup 'a' na função soma:", st.lookup("a"))
    print("Lookup 'global_var' na função soma:", st.lookup("global_var"))
    
    st.exit_scope()
    
    # Entrando na função main
    st.enter_scope("main")
    st.insert("x", "int")
    
    st.print_table()
