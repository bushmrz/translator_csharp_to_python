from datetime import datetime, timezone

from Token.token_type import TokenType
from Ast.Nodes.statement import *
from Runtime.Language_.language_list import LanguageList
from Runtime.Language_.language_instance import LanguageInstance
from Runtime.Language_.language_function import LanguageCallable, LanguageFunction
from Runtime.Language_.language_class import LanguageClass
from Runtime.Language_.assign_type import AssignType

from Extensions.numeric import Numeric
from Extensions.string import String
from Extensions.custom_any import CustomAny
from Runtime.return_ import ReturnException

from Runtime.runtime_error import RuntimeError
from Runtime.environment import Environment

from Runtime.Language_.error_handler import ErrorHandler


def can_convert_to_int(value):
    if isinstance(value, int):
        return True
    elif isinstance(value, float):
        return value == int(value)
    return False


class Clock:
    def arity(self):
        return 0

    def call(self, interpreter, arguments):
        current_time = datetime.now(timezone.utc).timestamp()
        current_time_in_seconds = current_time / 1000.0
        return current_time_in_seconds

    def __str__(self):
        return "<native fn>"


class Interpreter:
    def __init__(self, error_handler):
        self.globals = Environment()
        self.is_printable = True
        self.environment = self.globals
        self.locals = {}
        self.globals.define("clock", CType.NONE, Clock())
        self.error_handler = error_handler

    def interpret(self, statements, is_printable=True):
        self.is_printable = is_printable
        try:
            for statement in statements:
                self.execute(statement)
        except RuntimeError as error:
            self.error_handler.runtime_error(error)

    def evaluate(self, expr):
        return expr.accept(visitor=self)

    def execute(self, stmt):
        return stmt.accept(visitor=self)

    def resolve(self, expr, depth):
        self.locals[expr] = depth

    def execute_block(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        except Exception as error:
            self.environment = previous
            raise error
        self.environment = previous

    def handle_assigning(self, assign_type, token, previous_value, new_value):
        if new_value is None or previous_value is None:
            return None

        if assign_type == AssignType.ASSIGN:
            return new_value

        if assign_type == AssignType.PLUS_ASSIGN:
            result_value = Numeric.perform_operation(lambda x, y: x + y, previous_value, new_value)
            if result_value is None:
                result_value = String.perform_operation(lambda x, y: x + y, previous_value, new_value)
            if result_value is not None:
                return result_value
            raise self.throw_wrong_type(token)

        if assign_type == AssignType.MINUS_ASSIGN:
            result_value = Numeric.perform_operation(lambda x, y: x - y, previous_value, new_value)
            if result_value is not None:
                return result_value
            raise self.throw_wrong_type(token)

        if assign_type == AssignType.SLASH_ASSIGN:
            result_value = Numeric.perform_operation(lambda x, y: x / y, previous_value, new_value)
            if result_value is not None:
                return result_value
            raise self.throw_wrong_type(token)

        if assign_type == AssignType.STAR_ASSIGN:
            result_value = Numeric.perform_operation(lambda x, y: x * y, previous_value, new_value)
            if result_value is not None:
                return result_value
            raise self.throw_wrong_type(token)

    def check_type(self, token, ctype, value):
        # print(f"token--{token},ctype--{ctype},value--{value}","\n")
        if value is None:
            return
        if ctype == CType.INT:
            if not can_convert_to_int(value):
                raise self.throw_wrong_type(token)
        elif ctype in (CType.FLOAT, CType.DOUBLE):
            if not isinstance(value, float):
                raise self.throw_wrong_type(token)
        elif ctype == CType.STRING:
            if not isinstance(value, str):
                raise self.throw_wrong_type(token)
        elif ctype == CType.CHAR:
            if not (isinstance(value, str) and len(value) == 1):
                raise self.throw_wrong_type(token)
        elif ctype == CType.BOOL:
            if not isinstance(value, bool):
                raise self.throw_wrong_type(token)
        elif ctype == CType.STRING_ARRAY:
            if not (isinstance(value, LanguageList) and all(isinstance(v, str) for v in value.values)):
                raise self.throw_wrong_type(token)
        elif ctype == CType.INT_ARRAY:
            if not (isinstance(value, LanguageList) and all(can_convert_to_int(v) for v in value.values)):
                raise self.throw_wrong_type(token)
        elif ctype in (CType.DOUBLE_ARRAY, CType.FLOAT_ARRAY):
            if not (isinstance(value, LanguageList) and all(isinstance(v, float) for v in value.values)):
                raise self.throw_wrong_type(token)
        elif ctype == CType.CHAR_ARRAY:
            if not (isinstance(value, LanguageList) and all(isinstance(v, str) and len(v) == 1 for v in value.values)):
                raise self.throw_wrong_type(token)
        elif ctype == CType.BOOL_ARRAY:
            if not (isinstance(value, LanguageList) and all(isinstance(v, bool) for v in value.values)):
                raise self.throw_wrong_type(token)
        elif ctype in (CType.VOID, CType.NONE):
            pass
        else:
            raise self.throw_wrong_type(token)

    def throw_wrong_type(self, token):
        # self.error_handler.error_token(token=token, message="Value does not match variable's type")
        return RuntimeError(token=token, message="Value does not match variable's type")

    def look_up_variable(self, name, expr):
        if expr in self.locals:
            distance = self.locals[expr]
            return self.environment.get_at(distance, name.lexeme)
        return self.globals.get(name)

    def check_number_operand(self, operator, operand):
        if isinstance(operand, float) or isinstance(operand, int):
            return
        raise RuntimeError(token=operator, message="Operand must be a number.")

    def check_number_operands(self, operator, left, right):
        if (isinstance(left, float) and isinstance(right, float)) or (isinstance(left, int) and isinstance(right, int)):
            return
        raise RuntimeError(token=operator, message="Operands must be numbers.")

    def is_truthy(self, obj):
        if obj is None:
            return False
        if isinstance(obj, bool):
            return obj
        return True

    def is_equal(self, a, b):
        if a is None and b is None:
            return True
        if a is None:
            return False
        return a == b

    def stringify(self, obj):
        if obj is None:
            return "nil"
        if isinstance(obj, float):
            text = str(obj)
            if text.endswith(".0"):
                text = text[:-2]
            return text
        if isinstance(obj, int):
            return str(obj)
        if isinstance(obj, str):
            return obj
        if isinstance(obj, bool):
            return "true" if obj else "false"
        if isinstance(obj, LanguageFunction):
            return str(obj)
        if isinstance(obj, LanguageClass):
            return str(obj)
        if isinstance(obj, LanguageList):
            result = "["
            for index, value in enumerate(obj.values):
                result += self.stringify(value)
                if index < len(obj.values) - 1:
                    result += ", "
            result += "]"
            return result
        return "stringify: cannot recognize type"

    # ----------------------------
    # ExprVisitor
    # ----------------------------

    def visit_list_expr(self, expr):
        lst = LanguageList()
        for value in expr.values:
            lst.append(self.evaluate(value))
        return lst

    def visit_subscript_expr(self, expr):
        name = self.evaluate(expr.name)
        index = self.evaluate(expr.index)
        if not isinstance(name, LanguageList):
            raise RuntimeError(expr.paren, "Only lists can be subscripted.")

        if not can_convert_to_int(index):
            raise RuntimeError(expr.paren, "Index should be of type int.")

        index = int(index)
        if expr.value is not None:
            value = self.evaluate(expr.value)
            previous_value = name.get_ele_at(index)
            if not CustomAny.can_be_casted_to_same_type(value, previous_value) or (
                    value is None and previous_value is None):
                raise RuntimeError(expr.paren, "Unexpected assignment value type.")
            new_value = self.handle_assigning(expr.type, expr.paren, previous_value, value)
            if name.set_at_index(index, new_value):
                return new_value
            raise RuntimeError(expr.paren, "Index out of range.")
        else:
            if index < 0 or index >= name.length():
                raise RuntimeError(expr.paren, "Index out of range.")
            return name.get_ele_at(index)

    def visit_assign_expr(self, expr):
        value = self.evaluate(expr.value)
        variable = self.look_up_variable(expr.name, expr)
        var_type = variable.type
        previous_value = variable.item
        new_value = self.handle_assigning(expr.type, expr.name, previous_value, value)
        self.check_type(expr.name, var_type, value)
        if expr in self.locals:
            distance = self.locals[expr]
            self.environment.assign_at(distance, expr.name, var_type, new_value)
        else:
            self.globals.assign(expr.name, var_type, new_value)
        return new_value

    def visit_binary_expr(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        operator_type = expr.operator.type
        if operator_type == TokenType.BANG_EQUAL:
            return not self.is_equal(left, right)
        elif operator_type == TokenType.EQUAL_EQUAL:
            return self.is_equal(left, right)
        elif operator_type in (TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL,
                               TokenType.MINUS, TokenType.PLUS, TokenType.SLASH, TokenType.STAR):
            self.check_number_operands(expr.operator, left, right)
            if operator_type == TokenType.GREATER:
                return left > right
            elif operator_type == TokenType.GREATER_EQUAL:
                return left >= right
            elif operator_type == TokenType.LESS:
                return left < right
            elif operator_type == TokenType.LESS_EQUAL:
                return left <= right
            elif operator_type == TokenType.MINUS:
                return left - right
            elif operator_type == TokenType.PLUS:
                if isinstance(left, str) and isinstance(right, str):
                    return left + right
                return left + right
            elif operator_type == TokenType.SLASH:
                return left / right
            elif operator_type == TokenType.STAR:
                return left * right
        return None

    def visit_call_expr(self, expr):
        callee = self.evaluate(expr.callee)
        arguments = [self.evaluate(arg) for arg in expr.arguments]
        if not isinstance(callee, LanguageCallable):
            raise RuntimeError(expr.paren, "Can only call functions and classes.")
        if len(arguments) != callee.arity():
            raise RuntimeError(expr.paren, f"Expected {callee.arity()} arguments but got {len(arguments)}.")
        return callee.call(self, arguments)

    def visit_get_expr(self, expr):
        obj = self.evaluate(expr.object)
        if isinstance(obj, LanguageInstance):
            return obj.get(expr.name)
        raise RuntimeError(expr.name, "Only instances have properties.")

    def visit_grouping_expr(self, expr):
        return self.evaluate(expr.expression)

    def visit_literal_expr(self, expr):
        return expr.value

    def visit_logical_expr(self, expr):
        left = self.evaluate(expr.left)
        if expr.operator.type == TokenType.OR:
            if self.is_truthy(left):
                return left
        else:
            if not self.is_truthy(left):
                return left
        return self.evaluate(expr.right)

    def visit_set_expr(self, expr):
        obj = self.evaluate(expr.object)
        if not isinstance(obj, LanguageInstance):
            raise RuntimeError(expr.name, "Only instances have fields.")
        value = self.evaluate(expr.value)
        previous_value = obj.get(expr.name)
        new_value = self.handle_assigning(expr.type, expr.name, previous_value, value)
        obj.set(expr.name, new_value)
        return value

    def visit_super_expr(self, expr):
        distance = self.locals[expr]
        superclass = self.environment.get_at(distance, "super").item
        instance = self.environment.get_at(distance - 1, "this").item
        method = superclass.find_method(expr.method.lexeme)
        if method is None:
            raise RuntimeError(expr.method, f"Undefined property '{expr.method.lexeme}'.")
        return method.bind(instance)

    def visit_this_expr(self, expr):
        return self.look_up_variable(expr.keyword, expr).item

    def visit_unary_expr(self, expr):
        right = self.evaluate(expr.right)
        if expr.operator.type == TokenType.BANG:
            return not self.is_truthy(right)
        elif expr.operator.type == TokenType.MINUS:
            self.check_number_operand(expr.operator, right)
            return -(right)
        else:
            return None

    def visit_variable_expr(self, expr):
        value = self.look_up_variable(expr.name, expr).item
        if value is None:
            raise RuntimeError(expr.name, "Variable not initialized.")
        return value

    # ----------------------------
    # InterpreterStmtVisitorMixin:
    # ----------------------------
    def visit_var_stmt(self, stmt):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
            self.check_type(stmt.name, stmt.type, value)
        self.environment.define(stmt.name.lexeme, stmt.type, value)

    def visit_while_stmt(self, stmt):
        while self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)

    def visit_block_stmt(self, stmt):
        self.execute_block(stmt.statements, Environment(enclosing=self.environment))

    def visit_class_stmt(self, stmt):
        self.environment.define(stmt.name.lexeme, TokenType.NONE, None)

        superclass = None
        if stmt.superclass is not None:
            superclass = self.evaluate(stmt.superclass)
            if not isinstance(superclass, LanguageClass):
                raise RuntimeError(stmt.superclass.name, "Superclass must be a class.")
            self.environment = Environment(enclosing=self.environment)
            self.environment.define("super", TokenType.NONE, superclass)

        methods = {}
        for method in stmt.methods:
            function = LanguageFunction(method, self.environment, is_initializer=(method.name.lexeme == "init"))
            methods[method.name.lexeme] = function
        klass = LanguageClass(stmt.name.lexeme, superclass, methods)
        self.environment.assign(stmt.name, TokenType.NONE, klass)
        if stmt.superclass is not None:
            self.environment = self.environment.enclosing

    def visit_expression_stmt(self, stmt):
        self.evaluate(stmt.expression)

    def visit_function_stmt(self, stmt):
        function = LanguageFunction(stmt, self.environment, is_initializer=False)
        self.environment.define(stmt.name.lexeme, stmt.type, function)

    def visit_if_stmt(self, stmt):
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)

    def visit_print_stmt(self, stmt):
        value = self.evaluate(stmt.expression)
        if self.is_printable:
            print(self.stringify(value))

    def visit_return_stmt(self, stmt):
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)
        raise ReturnException(value)
