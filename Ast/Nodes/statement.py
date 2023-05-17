# from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Generic
from Token.token import Token
from Ast.Nodes.expression import *
from Runtime.Language_.c_type import CType

ReturnTypeStmt = TypeVar('ReturnTypeStmt')


class StmtVisitor(Generic[ReturnTypeStmt], ABC):
    @abstractmethod
    def visit_block_stmt(self, stmt: 'Block') -> ReturnTypeStmt:
        pass

    @abstractmethod
    def visit_class_stmt(self, stmt: 'Class') -> ReturnTypeStmt:
        pass

    @abstractmethod
    def visit_expression_stmt(self, stmt: 'Expression') -> ReturnTypeStmt:
        pass

    @abstractmethod
    def visit_function_stmt(self, stmt: 'Function') -> ReturnTypeStmt:
        pass

    @abstractmethod
    def visit_if_stmt(self, stmt: 'If') -> ReturnTypeStmt:
        pass

    @abstractmethod
    def visit_print_stmt(self, stmt: 'Print') -> ReturnTypeStmt:
        pass

    @abstractmethod
    def visit_return_stmt(self, stmt: 'Return') -> ReturnTypeStmt:
        pass

    @abstractmethod
    def visit_var_stmt(self, stmt: 'Var') -> ReturnTypeStmt:
        pass

    @abstractmethod
    def visit_while_stmt(self, stmt: 'While') -> ReturnTypeStmt:
        pass


class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor: StmtVisitor[ReturnTypeStmt]) -> ReturnTypeStmt:
        pass


class Block(Stmt):
    def __init__(self, statements):
        self.statements = statements

    def accept(self, visitor: StmtVisitor[ReturnTypeStmt]) -> ReturnTypeStmt:
        return visitor.visit_block_stmt(self)


class Class(Stmt):
    def __init__(self, name: Token, superclass: Optional[Variable], methods):
        self.name = name
        self.superclass = superclass
        self.methods = methods

    def accept(self, visitor: StmtVisitor[ReturnTypeStmt]) -> ReturnTypeStmt:
        return visitor.visit_class_stmt(self)


class Expression(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: StmtVisitor[ReturnTypeStmt]) -> ReturnTypeStmt:
        return visitor.visit_expression_stmt(self)


class Function(Stmt):
    def __init__(self, name: Token,params, body, type: CType):
        self.name = name
        self.params = params
        self.body = body
        self.type = type

    def accept(self, visitor: StmtVisitor[ReturnTypeStmt]) -> ReturnTypeStmt:
        return visitor.visit_function_stmt(self)


class If(Stmt):
    def __init__(self, condition: Expr, then_branch: Stmt, else_branch: Optional[Stmt]):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor: StmtVisitor[ReturnTypeStmt]) -> ReturnTypeStmt:
        return visitor.visit_if_stmt(self)


class Print(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: StmtVisitor[ReturnTypeStmt]) -> ReturnTypeStmt:
        return visitor.visit_print_stmt(self)


class Return(Stmt):
    def __init__(self, keyword: Token, value: Optional[Expr]):
        self.keyword = keyword
        self.value = value

    def accept(self, visitor: StmtVisitor[ReturnTypeStmt]) -> ReturnTypeStmt:
        return visitor.visit_return_stmt(self)


class Var(Stmt):
    def __init__(self, name: Token, type: CType, initializer: Optional[Expr]):
        self.name = name
        self.type = type
        self.initializer = initializer

    def __str__(self):
        return self.name

    def accept(self, visitor: StmtVisitor[ReturnTypeStmt]) -> ReturnTypeStmt:
        return visitor.visit_var_stmt(self)



class While(Stmt):
    def __init__(self, condition: Expr, body: Stmt):
        self.condition = condition
        self.body = body

    def accept(self, visitor: StmtVisitor[ReturnTypeStmt]) -> ReturnTypeStmt:
        return visitor.visit_while_stmt(self)
