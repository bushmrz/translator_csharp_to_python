from Ast.Nodes.expression import Expr
from Ast.Nodes.statement import Stmt

class AstPrinter:
    def print_nodes(self, statements):
        for statement in statements:
            print(self.print_node(statement))

    def print_node(self, node):
        if isinstance(node, Expr):
            return node.accept(self)
        elif isinstance(node, Stmt):
            return node.accept(self)

# Expressions
class ExprVisitor(AstPrinter):
    def visit_assign_expr(self, expr):
        return expr.name.lexeme + " " + expr.type.value + " " + self.print_node(expr.value)

    def visit_binary_expr(self, expr):
        return self.print_node(expr.left) + " " + expr.operator.lexeme + " " + self.print_node(expr.right)

    def visit_call_expr(self, expr):
        builder = self.print_node(expr.callee) + " "
        for argument in expr.arguments:
            builder += self.print_node(argument) + " "
        return builder + "CALL"

    def visit_get_expr(self, expr):
        return self.print_node(expr.object) + " " + expr.name.lexeme

    def visit_grouping_expr(self, expr):
        return "(" + self.print_node(expr.expression) + ")"

    def visit_literal_expr(self, expr):
        if expr.value is not None:
            if isinstance(expr.value, str):
                return f'"{expr.value}"'
            return str(expr.value)
        return "null"

    def visit_logical_expr(self, expr):
        return self.print_node(expr.right) + " " + expr.operator.lexeme + " " + self.print_node(expr.left)

    def visit_set_expr(self, expr):
        return self.print_node(expr.object) + " " + expr.name.lexeme + " " + expr.type.value + " " + self.print_node(expr.value)

    def visit_super_expr(self, expr):
        return "BASE." + expr.method.lexeme

    def visit_this_expr(self, expr):
        return "BASE"

    def visit_unary_expr(self, expr):
        return expr.operator.lexeme + self.print_node(expr.right)

    def visit_variable_expr(self, expr):
        return expr.name.lexeme

    def visit_list_expr(self, expr):
        builder = f"( ARRAY LENGTH({len(expr.values)})"
        for element in expr.values:
            builder += " " + self.print_node(element)
        builder += " )"
        return builder

    def visit_subscript_expr(self, expr):
        builder = self.print_node(expr.name) + " INDEX(" + self.print_node(expr.index) + ")"
        if expr.value:
            return builder + " " + (expr.type.value if expr.type else "=") + " " + self.print_node(expr.value)
        return "GET " + builder

# Statements
class StmtVisitor(AstPrinter):
    def visit_block_stmt(self, stmt):
        builder = "( "
        for statement in stmt.statements:
            builder += self.print_node(statement) + " "
        builder += ")"
        return builder

    def visit_class_stmt(self, stmt):
        builder = f"( CLASS {stmt.name.lexeme}"
        if stmt.superclass:
            builder += " < PARENTCLASS " + self.print_node(stmt.superclass)
        builder += " ("
        for method in stmt.methods:
            builder += self.print_node(method)
        builder += ") )"
        return builder

    def visit_expression_stmt(self, stmt):
        return self.print_node(stmt.expression)

    def visit_function_stmt(self, stmt):
        builder = f"{str(stmt.type)[6:]} {stmt.name.lexeme} ("

        for index, param in enumerate(stmt.params):
            if index != 0:
                builder += " "
            builder += f"{str(param.type)[6:]} {param.name.lexeme}"
        builder += ") ("
        for body in stmt.body:
            builder += "(" + self.print_node(body) + ") "
        builder += ")"
        return builder

    def visit_if_stmt(self, stmt):
        result = "IF " + self.print_node(stmt.condition) + " THEN " + self.print_node(stmt.then_branch)
        if stmt.else_branch:
            result += " ELSE " + self.print_node(stmt.else_branch)
        result += " END"
        return result

    def visit_print_stmt(self, stmt):
        return "(PRINT " + self.print_node(stmt.expression) + ")"

    def visit_return_stmt(self, stmt):
        if stmt.value:
            return "(RETURN " + self.print_node(stmt.value) + ")"
        return "RETURN"

    def visit_var_stmt(self, stmt):
        if stmt.initializer:
            return str(stmt.type)[6:] + " " + str(stmt.name.lexeme) + " = " + self.print_node(stmt.initializer)
        return str(stmt.type)[6:] + " " + stmt.name.lexeme

    def visit_while_stmt(self, stmt):
        return "WHILE " + self.print_node(stmt.condition) + " DO " + self.print_node(stmt.body) + " END"

# Inherit ExprVisitor and StmtVisitor in AstPrinter
class AstPrinter(ExprVisitor, StmtVisitor):
    pass
