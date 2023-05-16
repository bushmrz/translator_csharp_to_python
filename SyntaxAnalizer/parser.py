class ParseError(BaseException):
    pass


from Token.token_type import TokenType
# from Runtime.Language_.language import Language
from Ast.Nodes.statement import *
from Runtime.Language_.assign_type import AssignType
from Runtime.Language_.error_handler import ErrorHandler


class Parser:

    def __init__(self, tokens, error_handler):
        self.tokens = tokens
        self.current = 0
        self.error_handler = error_handler

    def parse(self):
        statements = []
        iteration_count = 0  # Add this line to count the number of iterations

        while not self.is_at_end():
            if iteration_count >= 100:  # Add this line as a safeguard to prevent infinite loop
                break

            declaration = self.declaration()
            iteration_count += 1  # Add this line to increment the iteration count

            if declaration is not None:
                statements.append(declaration)
        return statements

    def check_type(self, type_token_string):
        type_token_string = type_token_string
        saved_position = self.current
        if not self.is_at_end() and self.advance().type == TokenType.LEFT_BRACKET:
            self.consume(TokenType.RIGHT_BRACKET, "Expect ']' in array type declaration.")
            type_token_string += "[]"
        else:
            self.current = saved_position
        return type_token_string

    def match(self, *types):
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def consume(self, token_type, message):
        if self.check(token_type):
            return self.advance()
        raise self.error(self.peek(), message)

    def check(self, token_type):
        if self.is_at_end():
            return False
        return self.peek().type == token_type

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self):
        return self.peek().type == TokenType.EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def error(self, token, message):
        self.error_handler.error_token(token=token, message=message)
        return ParseError()

    def synchronize(self):
        self.advance()
        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return
            token_type = self.peek().type
            if token_type in (
                    TokenType.CLASS, TokenType.FUN, TokenType.VAR, TokenType.FOR, TokenType.IF, TokenType.WHILE,
                    TokenType.PRINT, TokenType.RETURN):
                return
            self.advance()

    # Node creating methods
    def expression(self):
        return self.assignment()

    def declaration(self):
        try:
            if self.match(TokenType.CLASS):
                return self.class_declaration()
            if self.check(TokenType.FUN):
                return self.function("function")
            if self.check(TokenType.VAR):
                return self.var_declaration()
            return self.statement()
        except ParseError:
            self.synchronize()
            self.advance()  # Add this line to advance the current index even when an error occurs
            return None

    def class_declaration(self):

        name = self.consume(TokenType.IDENTIFIER, "Expect class name.")
        superclass = None
        if self.match(TokenType.COLON):
            self.consume(TokenType.IDENTIFIER, "Expect superclass name.")
            superclass = Variable(name=self.previous())
        self.consume(TokenType.LEFT_BRACE, "Expect '{' before class body.")

        methods = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            methods.append(self.function("method"))

        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after class body.")
        return Class(name=name, superclass=superclass, methods=methods)

    def statement(self):
        if self.match(TokenType.FOR):
            return self.for_statement()
        if self.match(TokenType.IF):
            return self.if_statement()
        if self.match(TokenType.PRINT):
            return self.print_statement()
        if self.match(TokenType.RETURN):
            return self.return_statement()
        if self.match(TokenType.WHILE):
            return self.while_statement()
        # if self.match(TokenType.SEMICOLON):
        #     return self.expression_statement() # i add this
        if self.match(TokenType.LEFT_BRACE):
            return Block(statements=self.block())
        return self.expression_statement()

    def for_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")

        if self.match(TokenType.SEMICOLON):
            initializer = None
        elif self.check(TokenType.VAR):
            initializer = self.var_declaration()
        else:
            initializer = self.expression_statement()

        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")

        increment = None
        if not self.check(TokenType.RIGHT_PAREN):
            increment = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")

        body = self.statement()
        if increment is not None:
            body = Block(statements=[
                body,
                Expression(expression=increment)
            ])

        if condition is None:
            condition = Literal(value=True)
        body = While(condition=condition, body=body)

        if initializer is not None:
            body = Block(statements=[initializer, body])
        return body

    def if_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")

        then_branch = self.statement()
        else_branch = None

        if self.match(TokenType.ELSE):
            else_branch = self.statement()

        return If(condition=condition, then_branch=then_branch, else_branch=else_branch)

    def print_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after WriteLine.")
        value = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after WriteLine.")
        self.consume(TokenType.SEMICOLON, "Expect ';' at the end of WriteLine.")
        return Print(expression=value)

    def return_statement(self):
        keyword = self.previous()
        value = None

        if not self.check(TokenType.SEMICOLON):
            value = self.expression()

        self.consume(TokenType.SEMICOLON, "Expect ';' after return value.")
        return Return(keyword=keyword, value=value)

    def var_declaration(self):
        type_token = self.consume(TokenType.VAR, "Expect variable type modifier.")
        type_lexeme = self.check_type(type_token.lexeme)
        type_ = CType.get_type(type_lexeme)

        if type_ == CType.NONE:
            raise self.error(type_token, "Unexpected variable type modifier.")

        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")
        initializer = None

        if self.match(TokenType.EQUAL):
            initializer = self.expression()

        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Var(name=name, type=type_, initializer=initializer)

    def while_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
        body = self.statement()

        return While(condition=condition, body=body)

    def expression_statement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return Expression(expression=expr)

    def function(self, kind):
        type_token = self.consume(TokenType.FUN, f"Expect {kind} modifier.")
        type_lexeme = self.check_type(type_token.lexeme)
        type_ = CType.get_type(type_lexeme, is_function=True)
        if type_ == CType.NONE:
            raise self.error(type_token, f"Unexpected {kind} modifier.")
        name = self.consume(TokenType.IDENTIFIER, f"Expect {kind} name.")
        self.consume(TokenType.LEFT_PAREN, f"Expect '(' after {kind} name.")

        parameters = []
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                if len(parameters) >= 255:
                    self.error(self.peek(), "Can't have more than 255 parameters.")
                param_type = self.consume(TokenType.VAR, "Expect parameter type.")
                identifier = self.consume(TokenType.IDENTIFIER, "Expect parameter name.")
                parameters.append(Var(name=identifier, type=CType.get_type(param_type.lexeme), initializer=None))
                if not self.match(TokenType.COMMA):
                    break

        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")
        self.consume(TokenType.LEFT_BRACE, f"Expect 'brace' before {kind} body.")

        body = self.block()
        return Function(name=name, type=type_, params=parameters, body=body)

    def block(self):
        statements = []

        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            decl = self.declaration()
            if decl is not None:
                statements.append(decl)

        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def assignment(self):
        expr = self.or_()

        if self.match(TokenType.EQUAL, TokenType.PLUS_EQUAL, TokenType.MINUS_EQUAL, TokenType.SLASH_EQUAL,
                      TokenType.STAR_EQUAL):
            equals = self.previous()
            value = self.assignment()

            assign_type = AssignType.get_type(equals.lexeme)
            if assign_type is None:
                raise self.error(equals, "Invalid assignment.")

            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name=name, value=value, type=assign_type)
            if isinstance(expr, Get):
                return Set(object=object, name=expr.name, value=value, type=assign_type)
            if isinstance(expr, Subscript):
                return Subscript(name=expr.name, index=expr.index, value=value, paren=expr.paren, type=assign_type)

            raise self.error(equals, "Invalid assignment target.")

        return expr

    def or_(self):
        expr = self.and_()

        while self.match(TokenType.OR):
            operator = self.previous()
            right = self.and_()
            expr = Logical(left=expr, operator=operator, right=right)

        return expr

    def and_(self):
        expr = self.equality()

        while self.match(TokenType.AND):
            operator = self.previous()
            right = self.equality()
            expr = Logical(left=expr, operator=operator, right=right)

        return expr

    def equality(self):
        expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(left=expr, operator=operator, right=right)
        return expr

    def comparison(self):
        expr = self.term()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(left=expr, operator=operator, right=right)
        return expr

    def term(self):
        expr = self.factor()
        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(left=expr, operator=operator, right=right)
        return expr

    def factor(self):
        expr = self.unary()
        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(left=expr, operator=operator, right=right)
        return expr

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator=operator, right=right)
        return self.call()

    def finish_call(self, callee):
        arguments = []
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                if len(arguments) >= 255:
                    self.error(self.peek(), "Can't have more than 255 arguments.")
                arguments.append(self.expression())
                if not self.match(TokenType.COMMA):
                    break

        paren = self.consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")
        return Call(callee=callee, paren=paren, arguments=arguments)

    def call(self):
        expr = self.subscript()
        while True:
            if self.match(TokenType.LEFT_PAREN):
                expr = self.finish_call(expr)
            elif self.match(TokenType.DOT):
                name = self.consume(TokenType.IDENTIFIER, "Expect property name after '.'.")
                expr = Get(object=expr, name=name)
            else:
                break
        return expr

    def subscript(self):
        expr = self.primary()
        while True:
            if self.match(TokenType.LEFT_BRACKET):
                expr = self.finish_subscript(expr)
            else:
                break
        return expr

    def finish_subscript(self, expr):
        index = self.or_()
        paren = self.consume(TokenType.RIGHT_BRACKET, "Expect ']' after arguments.")
        return Subscript(name=expr, index=index, value=None, paren=paren, type=AssignType.NONE)

    def primary(self):
        if self.match(TokenType.FALSE):
            return Literal(value=False)
        if self.match(TokenType.TRUE):
            return Literal(value=True)
        if self.match(TokenType.NIL):
            return Literal(value=None)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(value=self.previous().literal)
        if self.match(TokenType.SUPER):
            keyword = self.previous()
            self.consume(TokenType.DOT, "Expect '.' after 'super'.")
            method = self.consume(TokenType.IDENTIFIER, "Expect superclass method name.")
            return Super(keyword=keyword, method=method)
        if self.match(TokenType.IDENTIFIER):
            return Variable(name=self.previous())
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expression=expr)

        if self.match(TokenType.LEFT_BRACE):
            return self.list()

        raise self.error(self.peek(), "Expect expression.")

    def list(self):
        values = []
        if self.match(TokenType.RIGHT_BRACE):
            return List(values=values)
        else:
            while True:
                if len(values) >= 255:
                    raise self.error(self.peek(), "Expect expression.")
                # value = self.or_()
                expr = self.or_()
                if isinstance(expr, Literal) and isinstance(expr.value, float) and expr.value == int(expr.value):
                    expr.value = int(expr.value)
                values.append(expr)
                if not self.match(TokenType.COMMA):
                    break

        self.consume(TokenType.RIGHT_BRACE, "Expect ']' at end of list.")
        # print('whats values:', [expr.value for expr in values])
        return List(values=values)
