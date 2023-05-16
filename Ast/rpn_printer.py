from Ast.Nodes.expression import Expr
from Ast.Nodes.statement import Stmt


class RpnPrinter:
    def print_nodes(self, statements):
        for statement in statements:
            print(self.print_node(statement))

    def print_node(self, node):
        if isinstance(node, Expr):
            return node.accept(self)
        elif isinstance(node, Stmt):
            return node.accept(self)

    def return_text(self, statements):
        with open("opz.txt", 'w') as file:
            for statement in statements:
                result = self.print_node(statement)
                file.write(result + '\n')


# Expressions
class ExprVisitor(RpnPrinter):
    def visit_assign_expr(self, expr):
        return expr.name.lexeme + " " + self.print_node(expr.value) + " " + expr.type.value

    def visit_binary_expr(self, expr):
        return self.print_node(expr.left) + " " + self.print_node(expr.right) + " " + expr.operator.lexeme

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
        return self.print_node(expr.right) + " " + self.print_node(expr.left) + " " + expr.operator.lexeme

    def visit_set_expr(self, expr):
        return self.print_node(expr.object) + " " + expr.name.lexeme + " " + self.print_node(
            expr.value) + " " + expr.type.value

    def visit_super_expr(self, expr):
        return "BASE." + expr.method.lexeme

    def visit_this_expr(self, expr):
        return "BASE"

    def visit_unary_expr(self, expr):
        return expr.operator.lexeme + self.print_node(expr.right)

    def visit_variable_expr(self, expr):
        return expr.name.lexeme

    def visit_list_expr(self, expr):
        builder = f"("
        for element in expr.values:
            builder += " " + self.print_node(element)
        builder += f" ARRAY LENGTH({len(expr.values)})"
        return builder

    def visit_subscript_expr(self, expr):
        builder = self.print_node(expr.name) + " INDEX(" + self.print_node(expr.index) + ") "
        if expr.value:
            return builder + self.print_node(expr.value) + " " + (expr.type.value if expr.type else "=")
        return builder + "GET"


# Statements
class StmtVisitor(RpnPrinter):
    def visit_block_stmt(self, stmt):
        builder = "BLOCK_START "
        for statement in stmt.statements:
            builder += self.print_node(statement) + " "
        builder += "BLOCK_END"
        return builder

    def visit_class_stmt(self, stmt):
        builder = f"( {stmt.name.lexeme} CLASS"
        if stmt.superclass:
            builder += " < " + self.print_node(stmt.superclass) + " PARENTCLASS"
        builder += " ("
        for method in stmt.methods:
            builder += self.print_node(method)
        builder += ") )"
        return builder

    def visit_expression_stmt(self, stmt):
        return self.print_node(stmt.expression)

    def visit_function_stmt(self, stmt):
        builder = f"{str(stmt.type)[6:]} {stmt.name.lexeme}"

        for param in stmt.params:
            builder += f" {param.name.lexeme} {str(param.type)[6:]}"
        builder += f" FUNCTION({len(stmt.params)}) {str(stmt.type)[6:]} PROC_START "
        for body in stmt.body:
            builder += self.print_node(body) + " "
        builder += "PROC_END"
        return builder

    def visit_if_stmt(self, stmt):
        result = self.print_node(stmt.condition) + " MARK_1 COND_JUMP " + self.print_node(stmt.then_branch)
        if stmt.else_branch:
            result += " MARK_2 UNCOND_JUMP MARK_1: " + self.print_node(stmt.else_branch) + " MARK_2:"
        else:
            result += " MARK_1:"
        return result

    def visit_print_stmt(self, stmt):
        return self.print_node(stmt.expression) + " PRINT"

    def visit_return_stmt(self, stmt):
        if stmt.value:
            return self.print_node(stmt.value) + " RETURN"
        return "RETURN"

    def visit_var_stmt(self, stmt):
        if stmt.initializer:
            return str(stmt.name.lexeme) + " " + self.print_node(stmt.initializer) + " = " + str(stmt.type)[6:]
        return stmt.name.lexeme + " " + str(stmt.type)[6:]

    def visit_while_stmt(self, stmt):
        return self.print_node(stmt.condition) + " LOOP_MARK COND_JUMP " + self.print_node(stmt.body) + " LOOP_MARK:"


# Inherit ExprVisitor and StmtVisitor in AstPrinter
class RpnPrinter(ExprVisitor, StmtVisitor):
    pass
