"""
Tabela de Símbolos - Gerencia Escopos e Declarações
Rastreia variáveis, funções e seus tipos em cada escopo
"""

class Scope:
    """Um escopo (global ou função local)"""
    def __init__(self, name, parent=None, level=0):
        self.name = name
        self.parent = parent
        self.level = level
        self.symbols = {}
        self.offset_counter = 0
    
    def insert(self, name, symbol_type, is_param=False, **extra):
        """Adiciona símbolo ao escopo"""
        if name in self.symbols:
            raise Exception(f"Erro: '{name}' já declarado em '{self.name}'")
        
        self.symbols[name] = {
            'name': name,
            'type': symbol_type,
            'scope': self.name,
            'offset': self.offset_counter,
            'is_param': is_param,
            **extra
        }
        self.offset_counter += 1
        return self.symbols[name]
    
    def lookup(self, name):
        """Busca símbolo aqui ou nos escopos pais"""
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup(name)
        return None


class SymbolTable:
    """Gerenciador de escopos aninhados (global → funções)"""
    def __init__(self):
        self.global_scope = Scope("global")
        self.current_scope = self.global_scope
        self.scopes_stack = [self.global_scope]
    
    def enter_scope(self, scope_name):
        """Cria e entra em novo escopo (ex: função)"""
        new_scope = Scope(scope_name, self.current_scope, len(self.scopes_stack))
        self.scopes_stack.append(new_scope)
        self.current_scope = new_scope
        return new_scope
    
    def exit_scope(self):
        """Volta ao escopo anterior"""
        if len(self.scopes_stack) <= 1:
            raise Exception("Erro: Não pode sair do escopo global")
        self.scopes_stack.pop()
        self.current_scope = self.scopes_stack[-1]
    
    def insert(self, name, symbol_type, is_param=False, **extra):
        """Adiciona símbolo no escopo atual"""
        return self.current_scope.insert(name, symbol_type, is_param, **extra)
    
    def lookup(self, name, current_scope_only=False):
        """Busca símbolo: se current_scope_only=True busca apenas no escopo atual"""
        if current_scope_only:
            return self.current_scope.symbols.get(name)
        return self.current_scope.lookup(name)
    
    def is_global_scope(self):
        """Verifica se está no global"""
        return self.current_scope == self.global_scope
    
    def print_table(self):
        """Exibe todos os escopos e símbolos"""
        print("\n=== TABELA DE SÍMBOLOS ===")
        for scope in self.scopes_stack:
            print(f"\nEscopo: {scope.name} (Nível: {scope.level})")
            if scope.symbols:
                for name, sym in scope.symbols.items():
                    tipo = sym['type']
                    offset = sym['offset']
                    extras = []
                    if sym.get('is_param'):
                        extras.append("[PARAM]")
                    if tipo == 'function':
                        extras.append(f"params={len(sym.get('params', []))}")
                    extras_str = " ".join(extras)
                    print(f"  {name}: {tipo} (offset={offset}) {extras_str}".strip())
            else:
                print("  (vazio)")
        print("========================\n")
