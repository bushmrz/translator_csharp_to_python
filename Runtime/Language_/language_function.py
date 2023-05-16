from typing import Any, List
from Runtime.Language_.language_callable import LanguageCallable
from Runtime.return_ import ReturnException
from Runtime.environment import Environment


class LanguageFunction(LanguageCallable):
    def __init__(self, declaration, closure, is_initializer):
        self.declaration = declaration
        self.closure = closure
        self.is_initializer = is_initializer

    def bind(self, instance):
        environment = Environment(enclosing=self.closure)
        environment.define("this", type_=None, value=instance)
        return LanguageFunction(declaration=self.declaration, closure=environment, is_initializer=self.is_initializer)

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"

    def arity(self):
        return len(self.declaration.params)

    def call(self, interpreter, arguments: List[Any]):
        environment = Environment(enclosing=self.closure)
        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].name.lexeme, type_=None, value=arguments[i])

        try:
            interpreter.execute_block(statements=self.declaration.body, environment=environment)
        except ReturnException as returnValue:
            if self.is_initializer:
                return self.closure.get_at(distance=0, name="this")
            return returnValue.value
        except Exception:
            return None

        if self.is_initializer:
            return self.closure.get_at(distance=0, name="this")
        return None
