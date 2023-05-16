from typing import Any

from Token.token import Token
from Runtime.runtime_error import RuntimeError
class LanguageInstance:
    def __init__(self, cls):
        self.cls = cls
        self.fields = {}

    def get(self, name: Token):
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]

        method = self.cls.find_method(name.lexeme)
        if method is not None:
            return method.bind(instance=self)

        raise RuntimeError(token=name, message=f"Undefined property '{name.lexeme}'.")

    def set(self, name: Token, value: Any):
        self.fields[name.lexeme] = value

    def __str__(self):
        return f"{self.cls.name} instance"
