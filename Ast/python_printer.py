from Ast.Nodes.expression import Expr, List
from Ast.Nodes.statement import Stmt


class PythonPrinter:
    indentation_level = 0

    def print_nodes(self, statements):
        for statement in statements:
            print(self.get_node(statement))

    def get_node(self, node):
        if isinstance(node, Expr):
            return node.accept(self)
        elif isinstance(node, Stmt):
            return node.accept(self)


# Expressions
class ExprVisitor(PythonPrinter):
    @property
    def indent(self):
        return "    " * self.indentation_level

    def get_nodes(self, statements):
        return "\n".join([self.get_node(stmt) for stmt in statements])

    def get_node(self, expr):
        return expr.accept(visitor=self)

    def visit_assign_expr(self, expr):
        return f"{expr.name.lexeme} = {self.get_node(expr.value)}"

    def visit_binary_expr(self, expr):
        return f"{self.get_node(expr.left)} {expr.operator.lexeme} {self.get_node(expr.right)}"

    def visit_call_expr(self, expr):
        arguments = ", ".join([self.get_node(arg) for arg in expr.arguments])
        return f"{self.get_node(expr.callee)}({arguments})"

    def visit_get_expr(self, expr):
        return f"{self.get_node(expr.object)}.{expr.name.lexeme}"

    def visit_grouping_expr(self, expr):
        return f"({self.get_node(expr.expression)})"

    def visit_literal_expr(self, expr):
        if expr.value is not None:
            if isinstance(expr.value, str):
                return f"\"{expr.value}\""
            return str(expr.value)
        return "None"

    def visit_logical_expr(self, expr):
        return f"({self.get_node(expr.left)} {expr.operator.lexeme} {self.get_node(expr.right)})"

    def visit_set_expr(self, expr):
        return f"{self.get_node(expr.object)}.{expr.name.lexeme} = {self.get_node(expr.value)}"

    def visit_super_expr(self, expr):
        return f"super.{expr.method.lexeme}"

    def visit_this_expr(self, expr):
        return "self."

    def visit_unary_expr(self, expr):
        return f"({expr.operator.lexeme}{self.get_node(expr.right)})"

    def visit_variable_expr(self, expr):
        return expr.name.lexeme

    def visit_list_expr(self, expr):
        elements = ", ".join([self.get_node(val) for val in expr.values])
        return f"[{elements}]"

    def visit_subscript_expr(self, expr):
        subscript_str = f"{self.get_node(expr.name)}[{self.get_node(expr.index)}]"
        if expr.value is not None:
            subscript_str += f" = {self.get_node(expr.value)}"
        return subscript_str


# Statements
class StmtVisitor(PythonPrinter):
    @property
    def indent(self):
        return "    " * self.indentation_level

    def visit_block_stmt(self, stmt):
        block_str = "\n".join([self.get_node(statement) for statement in stmt.statements])
        return block_str

    def visit_class_stmt(self, stmt):
        class_str = f"class {stmt.name.lexeme}"
        if stmt.superclass is not None:
            class_str += f"({stmt.superclass.name.lexeme})"
        class_str += ":\n"
        self.indentation_level += 1
        if not stmt.methods:
            class_str += f"{self.indent}pass"
        else:
            for method in stmt.methods:
                class_str += f"{self.indent}{self.get_node(method)}\n"
        self.indentation_level -= 1
        class_str += self.indent
        return class_str

    def visit_expression_stmt(self, stmt):
        return self.get_node(stmt.expression)

    def visit_function_stmt(self, stmt):
        function_str = f"def {stmt.name.lexeme}("
        function_str += ", ".join([param.name.lexeme for param in stmt.params])
        function_str += "):\n"
        self.indentation_level += 1
        for statement in stmt.body:
            function_str += f"{self.indent}{self.get_node(statement)}\n"
        self.indentation_level -= 1
        function_str += self.indent
        return function_str

    def visit_if_stmt(self, stmt):
        if_str = f"if {self.get_node(stmt.condition)}:\n"
        self.indentation_level += 1
        if_str += f"{self.indent}{self.get_node(stmt.then_branch)}\n"
        self.indentation_level -= 1
        if_str += self.indent
        if stmt.else_branch is not None:
            if_str += "else:\n"
            self.indentation_level += 1
            if_str += f"{self.indent}{self.get_node(stmt.else_branch)}\n"
            self.indentation_level -= 1
            if_str += self.indent
        return if_str

    def visit_print_stmt(self, stmt):
        return f"print({self.get_node(stmt.expression)})"

    def visit_return_stmt(self, stmt):
        return_str = "return"
        if stmt.value is not None:
            return_str += f" {self.get_node(stmt.value)}"
        return return_str

    def visit_var_stmt(self, stmt):
        var_str = stmt.name.lexeme
        if stmt.initializer is not None:
            if isinstance(stmt.initializer, List):
                if len(self.get_node(stmt.initializer)) <= 1:
                    var_str += f"[{len(stmt.initializer.values)}] = {self.get_node(stmt.initializer)}"
                else:
                    var_str += f" = {self.get_node(stmt.initializer)}"
            else:
                var_str += f" = {self.get_node(stmt.initializer)}"
        return var_str

    def visit_while_stmt(self, stmt):
        while_str = f"while {self.get_node(stmt.condition)}:\n"
        self.indentation_level += 1
        while_str += f"{self.indent}{self.get_node(stmt.body)}\n"
        self.indentation_level -= 1
        while_str += self.indent
        return while_str


# Inherit ExprVisitor and StmtVisitor in AstPrinter
class PythonPrinter(ExprVisitor, StmtVisitor):
    pass
