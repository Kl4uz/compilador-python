"""
Analisador Sintático - Parser LL(1) Top-Down
Implementação: Recursive Descent com lookahead de 1 token
Cada não-terminal da gramática = 1 função recursiva
"""

class Token:
    """Representação de um token do léxico"""
    def __init__(self, type, value, lineno=1):
        self.type = type
        self.value = value
        self.lineno = lineno
    
    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.lineno})"


class LL1Parser:
    """
    Parser LL(1) - Recursive Descent
    
    Cada função representa um não-terminal da gramática:
    - program() → declaração*
    - declaration() → int ID = expr ;
    - expression() → term ((+|-) term)*
    - term() → factor ((*|/) factor)*
    - factor() → (expr) | ID | NUMBER
    """
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0] if tokens else None
        self.errors = []
    
    def error(self, msg):
        line = self.current_token.lineno if self.current_token else '?'
        error_msg = f"[ERRO SINTÁTICO] {msg} na linha {line}"
        self.errors.append(error_msg)
        print(error_msg)
    
    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None
    
    def match(self, expected_type):
        if self.current_token and self.current_token.type == expected_type:
            token = self.current_token
            self.advance()
            return token
        else:
            current = self.current_token.type if self.current_token else 'EOF'
            self.error(f"Esperado '{expected_type}', encontrado '{current}'")
            return None
    
    def peek(self):
        return self.current_token.type if self.current_token else None
    
    # ═══════════════════════════════════════════════════════
    # FUNÇÕES DE PARSING - Uma por não-terminal da gramática
    # ═══════════════════════════════════════════════════════
    
    def parse(self):
        """Ponto de entrada do parser - retorna (AST, erros)"""
        try:
            parse_tree = self.program()
            if self.current_token is not None:
                self.error(f"Token inesperado: {self.current_token.type}")
            return parse_tree, self.errors
        except Exception as e:
            self.error(f"Erro durante parsing: {str(e)}")
            return None, self.errors
    
    def program(self):
        declarations = self.declaration_list()
        return ('program', declarations)
    
    def declaration_list(self):
        declarations = []
        while self.peek() in ['INT', 'RETURN', 'PRINT', 'ID']:
            decl = self.declaration()
            if decl:
                declarations.append(decl)
            else:
                break
        return declarations
    
    def declaration(self):
        if self.peek() == 'INT':
            saved_pos = self.pos
            self.advance()
            
            if self.peek() == 'ID':
                self.advance()
                if self.peek() == 'LPAREN':
                    self.pos = saved_pos
                    self.current_token = self.tokens[self.pos]
                    return self.function_declaration()
                else:
                    self.pos = saved_pos
                    self.current_token = self.tokens[self.pos]
                    return self.statement()
            else:
                self.error("Esperado ID após INT")
                return None
        else:
            return self.statement()
    
    def function_declaration(self):
        self.match('INT')
        name_token = self.match('ID')
        name = name_token.value if name_token else 'unknown'
        self.match('LPAREN')
        
        params = []
        if self.peek() != 'RPAREN':
            params = self.parameter_list()
        
        self.match('RPAREN')
        self.match('LBRACE')
        body = self.statement_list()
        self.match('RBRACE')
        
        return ('function', name, params, body)
    
    def parameter_list(self):
        params = []
        param = self.parameter()
        if param:
            params.append(param)
        
        while self.peek() == 'COMMA':
            self.advance()
            param = self.parameter()
            if param:
                params.append(param)
        
        return params
    
    def parameter(self):
        self.match('INT')
        name_token = self.match('ID')
        name = name_token.value if name_token else 'unknown'
        return ('param', name, 'int')
    
    def statement_list(self):
        statements = []
        while self.peek() in ['INT', 'ID', 'RETURN', 'PRINT']:
            stmt = self.statement()
            if stmt:
                statements.append(stmt)
            else:
                break
        return statements
    
    def statement(self):
        lookahead = self.peek()
        
        if lookahead == 'INT':
            self.advance()
            name_token = self.match('ID')
            name = name_token.value if name_token else 'unknown'
            self.match('EQUALS')
            expr = self.expression()
            self.match('SEMICOLON')
            return ('decl_assign', name, expr)
        
        elif lookahead == 'ID':
            name_token = self.match('ID')
            name = name_token.value if name_token else 'unknown'
            self.match('EQUALS')
            expr = self.expression()
            self.match('SEMICOLON')
            return ('assign', name, expr)
        
        elif lookahead == 'RETURN':
            self.advance()
            if self.peek() != 'SEMICOLON':
                expr = self.expression()
                self.match('SEMICOLON')
                return ('return', expr)
            else:
                self.match('SEMICOLON')
                return ('return', None)
        
        elif lookahead == 'PRINT':
            self.advance()
            self.match('LPAREN')
            expr = self.expression()
            self.match('RPAREN')
            self.match('SEMICOLON')
            return ('print', expr)
        
        else:
            self.error(f"Statement inválido: '{lookahead}'")
            return None
    
    def expression(self):
        left = self.term()
        while self.peek() in ['PLUS', 'MINUS']:
            op_token = self.current_token
            op = op_token.value
            self.advance()
            right = self.term()
            left = (op, left, right)
        return left
    
    def term(self):
        left = self.factor()
        while self.peek() in ['TIMES', 'DIVIDE']:
            op_token = self.current_token
            op = op_token.value
            self.advance()
            right = self.factor()
            left = (op, left, right)
        return left
    
    def factor(self):
        lookahead = self.peek()
        
        if lookahead == 'NUMBER':
            token = self.current_token
            self.advance()
            return ('num', token.value)
        
        elif lookahead == 'ID':
            name_token = self.current_token
            name = name_token.value
            self.advance()
            
            if self.peek() == 'LPAREN':
                self.advance()
                args = []
                if self.peek() != 'RPAREN':
                    args = self.argument_list()
                self.match('RPAREN')
                return ('call', name, args)
            else:
                return ('id', name)
        
        elif lookahead == 'LPAREN':
            self.advance()
            expr = self.expression()
            self.match('RPAREN')
            return expr
        
        else:
            self.error(f"Fator inválido: '{lookahead}'")
            return ('num', 0)
    
    def argument_list(self):
        args = []
        arg = self.expression()
        args.append(arg)
        
        while self.peek() == 'COMMA':
            self.advance()
            arg = self.expression()
            args.append(arg)
        
        return args


def parse_ll1(tokens):
    """Parser LL(1) - retorna parse tree e erros"""
    parser = LL1Parser(tokens)
    parse_tree, errors = parser.parse()
    return parse_tree, errors