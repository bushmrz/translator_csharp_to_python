from Runtime.Language_.error_handler import ErrorHandler


class Resolver:
    class FunctionType:
        NONE = "none"
        FUNCTION = "function"
        INITIALIZER = "initializer"
        METHOD = "method"

    class ClassType:
        NONE = "none"
        CLASS = "class"
        SUBCLASS = "subclass"

    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.scopes = [{}]
        self.current_function = Resolver.FunctionType.NONE
        self.current_class = Resolver.ClassType.NONE
        self.identifiers = [{}]

    def begin_scope(self):
        self.identifiers.append({})
        self.scopes.append({})

    def end_scope(self):
        self.identifiers.pop()
        self.scopes.pop()

    def declare(self, name):
        if not self.scopes or not self.identifiers:
            return

        current_scope = self.scopes[-1]
        current_block = self.identifiers[-1]

        if name.lexeme in current_scope:
            ErrorHandler.error_token(self, token=name, message="Already a variable with this name in this scope.")

        current_block[name] = 0
        current_scope[name.lexeme] = False

        self.identifiers[-1] = current_block
        self.scopes[-1] = current_scope

    def define(self, name):
        if not self.scopes:
            return
        self.scopes[-1][name.lexeme] = True

    def resolve(self, statements):
        for statement in statements:
            self.resolve_stmt(statement)

    def resolve_local(self, expr, name):
        for i, scope in reversed(list(enumerate(self.scopes))):
            if name.lexeme in scope:
                self.identifiers[i].pop(name, None)
                self.interpreter.resolve(expr=expr, depth=len(self.scopes) - 1 - i)
                return

    def resolve_stmt(self, stmt):
        stmt.accept(visitor=self)

    def resolve_expr(self, expr):
        expr.accept(visitor=self)

    def resolve_function(self, function, func_type):
        enclosing_function = self.current_function
        self.current_function = func_type

        self.begin_scope()
        for param in function.params:
            self.declare(param.name)
            self.define(param.name)
        self.resolve(function.body)
        self.end_scope()

        self.current_function = enclosing_function

    # Statement visitor methods
    def visit_block_stmt(self, stmt):
        self.begin_scope()
        self.resolve(stmt.statements)
        self.end_scope()

    def visit_class_stmt(self, stmt):
        self.declare(stmt.name)
        self.define(stmt.name)

        enclosing_class = self.current_class
        self.current_class = Resolver.ClassType.CLASS

        if stmt.superclass:
            if stmt.name.lexeme == stmt.superclass.name.lexeme:
                ErrorHandler.error_token(self, token=stmt.superclass.name, message="A class can't inherit from itself.")
            self.current_class = Resolver.ClassType.SUBCLASS
            self.resolve_expr(stmt.superclass)

            self.begin_scope()
            self.scopes[-1]["base"] = True

        self.begin_scope()

        for method in stmt.methods:
            declaration = Resolver.FunctionType.INITIALIZER if method.name.lexeme == "init" else Resolver.FunctionType.METHOD
            self.resolve_function(method, func_type=declaration)

        self.end_scope()

        if stmt.superclass:
            self.end_scope()

        self.current_class = enclosing_class

    def visit_expression_stmt(self, stmt):
        self.resolve_expr(stmt.expression)

    def visit_function_stmt(self, stmt):
        self.declare(stmt.name)
        self.define(stmt.name)
        self.resolve_function(stmt, func_type=Resolver.FunctionType.FUNCTION)

    def visit_if_stmt(self, stmt):
        self.resolve_expr(stmt.condition)
        self.resolve_stmt(stmt.then_branch)
        if stmt.else_branch:
            self.resolve_stmt(stmt.else_branch)

    def visit_print_stmt(self, stmt):
        self.resolve_expr(stmt.expression)

    def visit_return_stmt(self, stmt):
        if self.current_function == Resolver.FunctionType.NONE:
            ErrorHandler.error_token(self, token=stmt.keyword, message="Can't return from top-level code.")

        if stmt.value:
            if self.current_function == Resolver.FunctionType.INITIALIZER:
                ErrorHandler.error_token(self, token=stmt.keyword, message="Can't return a value from an initializer.")
            self.resolve_expr(stmt.value)

    def visit_var_stmt(self, stmt):
        self.declare(stmt.name)
        if stmt.initializer:
            self.resolve_expr(stmt.initializer)
        self.define(stmt.name)

    def visit_while_stmt(self, stmt):
        self.resolve_expr(stmt.condition)
        self.resolve_stmt(stmt.body)

    # Expression visitor methods
    def visit_list_expr(self, expr):
        for value in expr.values:
            self.resolve_expr(value)

    def visit_subscript_expr(self, expr):
        self.resolve_expr(expr.name)
        self.resolve_expr(expr.index)
        if expr.value:
            self.resolve_expr(expr.value)

    def visit_assign_expr(self, expr):
        self.resolve_expr(expr.value)
        self.resolve_local(expr, name=expr.name)

    def visit_binary_expr(self, expr):
        self.resolve_expr(expr.left)
        self.resolve_expr(expr.right)

    def visit_call_expr(self, expr):
        self.resolve_expr(expr.callee)

        for argument in expr.arguments:
            self.resolve_expr(argument)

    def visit_get_expr(self, expr):
        self.resolve_expr(expr.object)

    def visit_grouping_expr(self, expr):
        self.resolve_expr(expr.expression)

    def visit_literal_expr(self, expr):
        return

    def visit_logical_expr(self, expr):
        self.resolve_expr(expr.left)
        self.resolve_expr(expr.right)

    def visit_set_expr(self, expr):
        self.resolve_expr(expr.value)
        self.resolve_expr(expr.object)

    def visit_super_expr(self, expr):
        if self.current_class == Resolver.ClassType.NONE:
            ErrorHandler.error_token(self, token=expr.keyword, message="Can't use 'super' outside of a class.")
        elif self.current_class != Resolver.ClassType.SUBCLASS:
            ErrorHandler.error_token(self, token=expr.keyword,
                                     message="Can't use 'super' in a class with no superclass.")
        self.resolve_local(expr, name=expr.keyword)

    def visit_this_expr(self, expr):
        if self.current_class == Resolver.ClassType.NONE:
            ErrorHandler.error_token(self, token=expr.keyword, message="Can't use 'this' outside of a class.")
            return
        self.resolve_local(expr, name=expr.keyword)

    def visit_unary_expr(self, expr):
        self.resolve_expr(expr.right)

    def visit_variable_expr(self, expr):
        if expr.name.lexeme in self.scopes[-1] and not self.scopes[-1][expr.name.lexeme]:
            ErrorHandler.error_token(self, token=expr.name, message="Can't read local variable in its own initializer.")
            return
        self.resolve_local(expr, name=expr.name)
