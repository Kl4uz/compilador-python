"""
Analisador Sintático LL(1) Top-Down
Usa Recursive Descent Parser conforme metodologia do professor
Lookahead de 1 token para decisões de parsing
"""


class Token:
    """Classe auxiliar para representar tokens"""
    def __init__(self, type, value, lineno=1):
        self.type = type
        self.value = value
        self.lineno = lineno
    
    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.lineno})"


class LL1Parser:
    """
    Parser LL(1) Top-Down usando Recursive Descent
    Cada não-terminal da gramática vira uma função recursiva
    Usa lookahead de 1 token para decidir qual regra aplicar
    """
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0] if tokens else None
        self.errors = []
    
    def error(self, msg):
        """Registra erro sintático"""
        line = self.current_token.lineno if self.current_token else '?'
        error_msg = f"[ERRO SINTÁTICO LL(1)] {msg} na linha {line}"
        self.errors.append(error_msg)
        print(error_msg)
    
    def advance(self):
        """Avança para próximo token (lookahead)"""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None
    
    def match(self, expected_type):
        """
        Consome token esperado
        Se não corresponder, reporta erro
        """
        if self.current_token and self.current_token.type == expected_type:
            token = self.current_token
            self.advance()
            return token
        else:
            current = self.current_token.type if self.current_token else 'EOF'
            self.error(f"Esperado '{expected_type}', encontrado '{current}'")
            return None
    
    def peek(self):
        """Olha o token atual sem consumir (lookahead)"""
        return self.current_token.type if self.current_token else None
    
    # ===== GRAMÁTICA LL(1) =====
    # Cada função representa um não-terminal
    # Usa lookahead de 1 token para escolher regra
    
    def parse(self):
        """
        Símbolo inicial: program
        program → declaration_list
        """
        try:
            parse_tree = self.program()
            
            if self.current_token is not None:
                self.error(f"Token inesperado após fim do programa: {self.current_token.type}")
            
            return parse_tree, self.errors
        except Exception as e:
            self.error(f"Exceção durante parsing: {str(e)}")
            return None, self.errors
    
    def program(self):
        """program → declaration_list"""
        declarations = self.declaration_list()
        return ('program', declarations)
    
    def declaration_list(self):
        """
        declaration_list → declaration declaration_list'
        declaration_list' → declaration declaration_list' | ε
        
        Eliminando recursão à esquerda para LL(1):
        Usa loop para processar múltiplas declarações
        """
        declarations = []
        
        # Lookahead: enquanto tivermos INT (função ou statement)
        while self.peek() in ['INT', 'RETURN', 'PRINT', 'ID']:
            decl = self.declaration()
            if decl:
                declarations.append(decl)
            else:
                break  # Erro, para de processar
        
        return declarations
    
    def declaration(self):
        """
        declaration → function_declaration | statement
        
        Lookahead: INT ID LPAREN = função
        Lookahead: outros = statement
        """
        # Usa lookahead para decidir
        if self.peek() == 'INT':
            # Precisa olhar mais à frente para distinguir função de statement
            # Se INT ID LPAREN → função
            # Se INT ID EQUALS → statement
            
            # Salva posição para backtrack se necessário
            saved_pos = self.pos
            
            self.advance()  # consome INT
            
            if self.peek() == 'ID':
                self.advance()  # consome ID
                
                if self.peek() == 'LPAREN':
                    # É função! Volta e chama function_declaration
                    self.pos = saved_pos
                    self.current_token = self.tokens[self.pos]
                    return self.function_declaration()
                else:
                    # É statement! Volta e chama statement
                    self.pos = saved_pos
                    self.current_token = self.tokens[self.pos]
                    return self.statement()
            else:
                self.error("Esperado ID após INT")
                return None
        else:
            return self.statement()
    
    def function_declaration(self):
        """
        function_declaration → INT ID LPAREN parameter_list RPAREN LBRACE statement_list RBRACE
                             | INT ID LPAREN RPAREN LBRACE statement_list RBRACE
        """
        self.match('INT')
        name_token = self.match('ID')
        name = name_token.value if name_token else 'unknown'
        
        self.match('LPAREN')
        
        # Lookahead: se RPAREN, sem parâmetros; senão, tem parâmetros
        params = []
        if self.peek() != 'RPAREN':
            params = self.parameter_list()
        
        self.match('RPAREN')
        self.match('LBRACE')
        
        body = self.statement_list()
        
        self.match('RBRACE')
        
        return ('function', name, params, body)
    
    def parameter_list(self):
        """
        parameter_list → parameter parameter_list'
        parameter_list' → COMMA parameter parameter_list' | ε
        """
        params = []
        
        # Primeiro parâmetro
        param = self.parameter()
        if param:
            params.append(param)
        
        # Lookahead: enquanto tiver COMMA, continua
        while self.peek() == 'COMMA':
            self.advance()  # consome COMMA
            param = self.parameter()
            if param:
                params.append(param)
        
        return params
    
    def parameter(self):
        """parameter → INT ID"""
        self.match('INT')
        name_token = self.match('ID')
        name = name_token.value if name_token else 'unknown'
        return ('param', name, 'int')
    
    def statement_list(self):
        """
        statement_list → statement statement_list'
        statement_list' → statement statement_list' | ε
        """
        statements = []
        
        # Lookahead: enquanto tiver início de statement
        while self.peek() in ['INT', 'ID', 'RETURN', 'PRINT']:
            stmt = self.statement()
            if stmt:
                statements.append(stmt)
            else:
                break
        
        return statements
    
    def statement(self):
        """
        statement → INT ID EQUALS expression SEMICOLON  (decl_assign)
                  | ID EQUALS expression SEMICOLON      (assign)
                  | RETURN expression SEMICOLON         (return)
                  | RETURN SEMICOLON                    (return void)
                  | PRINT LPAREN expression RPAREN SEMICOLON
        
        Usa lookahead para decidir qual regra
        """
        lookahead = self.peek()
        
        if lookahead == 'INT':
            # INT ID EQUALS expression SEMICOLON
            self.advance()  # consome INT
            name_token = self.match('ID')
            name = name_token.value if name_token else 'unknown'
            self.match('EQUALS')
            expr = self.expression()
            self.match('SEMICOLON')
            return ('decl_assign', name, expr)
        
        elif lookahead == 'ID':
            # ID EQUALS expression SEMICOLON
            name_token = self.match('ID')
            name = name_token.value if name_token else 'unknown'
            self.match('EQUALS')
            expr = self.expression()
            self.match('SEMICOLON')
            return ('assign', name, expr)
        
        elif lookahead == 'RETURN':
            # RETURN [expression] SEMICOLON
            self.advance()  # consome RETURN
            
            # Lookahead: se não for SEMICOLON, tem expressão
            if self.peek() != 'SEMICOLON':
                expr = self.expression()
                self.match('SEMICOLON')
                return ('return', expr)
            else:
                self.match('SEMICOLON')
                return ('return', None)
        
        elif lookahead == 'PRINT':
            # PRINT LPAREN expression RPAREN SEMICOLON
            self.advance()  # consome PRINT
            self.match('LPAREN')
            expr = self.expression()
            self.match('RPAREN')
            self.match('SEMICOLON')
            return ('print', expr)
        
        else:
            self.error(f"Statement inválido começando com '{lookahead}'")
            return None
    
    def expression(self):
        """
        expression → term expression'
        expression' → PLUS term expression' | MINUS term expression' | ε
        
        Elimina recursão à esquerda para LL(1)
        """
        # Primeiro termo
        left = self.term()
        
        # Lookahead: enquanto tiver + ou -
        while self.peek() in ['PLUS', 'MINUS']:
            op_token = self.current_token
            op = op_token.value
            self.advance()  # consome operador
            
            right = self.term()
            left = (op, left, right)
        
        return left
    
    def term(self):
        """
        term → factor term'
        term' → TIMES factor term' | DIVIDE factor term' | ε
        
        Implementa precedência: * e / têm maior precedência que + e -
        """
        # Primeiro fator
        left = self.factor()
        
        # Lookahead: enquanto tiver * ou /
        while self.peek() in ['TIMES', 'DIVIDE']:
            op_token = self.current_token
            op = op_token.value
            self.advance()  # consome operador
            
            right = self.factor()
            left = (op, left, right)
        
        return left
    
    def factor(self):
        """
        factor → NUMBER
               | ID
               | ID LPAREN argument_list RPAREN  (chamada função)
               | ID LPAREN RPAREN                (chamada sem args)
               | LPAREN expression RPAREN
        
        Usa lookahead para decidir
        """
        lookahead = self.peek()
        
        if lookahead == 'NUMBER':
            token = self.current_token
            self.advance()
            return ('num', token.value)
        
        elif lookahead == 'ID':
            name_token = self.current_token
            name = name_token.value
            self.advance()
            
            # Lookahead: se LPAREN, é chamada de função
            if self.peek() == 'LPAREN':
                self.advance()  # consome LPAREN
                
                # Lookahead: se RPAREN, sem argumentos
                args = []
                if self.peek() != 'RPAREN':
                    args = self.argument_list()
                
                self.match('RPAREN')
                return ('call', name, args)
            else:
                # É só um ID
                return ('id', name)
        
        elif lookahead == 'LPAREN':
            self.advance()  # consome LPAREN
            expr = self.expression()
            self.match('RPAREN')
            return expr
        
        else:
            self.error(f"Fator inválido: '{lookahead}'")
            return ('num', 0)  # Retorna algo para continuar
    
    def argument_list(self):
        """
        argument_list → expression argument_list'
        argument_list' → COMMA expression argument_list' | ε
        """
        args = []
        
        # Primeiro argumento
        arg = self.expression()
        args.append(arg)
        
        # Lookahead: enquanto tiver COMMA
        while self.peek() == 'COMMA':
            self.advance()  # consome COMMA
            arg = self.expression()
            args.append(arg)
        
        return args


def parse_ll1(tokens):
    """
    Função principal do parser LL(1)
    
    Args:
        tokens: Lista de tokens do lexer
    
    Returns:
        parse_tree: Árvore de derivação
        errors: Lista de erros encontrados
    """
    parser = LL1Parser(tokens)
    parse_tree, errors = parser.parse()
    return parse_tree, errors


# Para testes
if __name__ == "__main__":
    # Tokens de exemplo para: int x = 5 + 3;
    test_tokens = [
        Token('INT', 'int', 1),
        Token('ID', 'x', 1),
        Token('EQUALS', '=', 1),
        Token('NUMBER', 5, 1),
        Token('PLUS', '+', 1),
        Token('NUMBER', 3, 1),
        Token('SEMICOLON', ';', 1),
    ]
    
    print("=== TESTE DO PARSER LL(1) ===")
    print("Tokens:", test_tokens)
    
    parse_tree, errors = parse_ll1(test_tokens)
    
    if errors:
        print("\nErros encontrados:")
        for error in errors:
            print(f"  {error}")
    else:
        print("\n✅ Parse bem-sucedido!")
    
    print("\nParse Tree:")
    print(parse_tree)
