class Variable:
    def __init__(self, type_, item):
        self.type = type_
        self.item = item


class Environment:
    def __init__(self, enclosing=None):
        self.enclosing = enclosing
        self.values = {}

    def get(self, name):
        if name.lexeme in self.values:
            return Variable(*self.values[name.lexeme])

        if self.enclosing:
            return self.enclosing.get(name)

        raise RuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def assign(self, name, type_, value):
        if name.lexeme in self.values:
            self.values[name.lexeme] = (type_, value)
            return

        if self.enclosing:
            self.enclosing.assign(name, type_, value)
            return

        raise RuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def define(self, name, type_, value):
        self.values[name] = (type_, value)

    def ancestor(self, distance):
        environment = self
        for _ in range(distance):
            environment = environment.enclosing
        return environment

    def get_at(self, distance, name):
        return Variable(*self.ancestor(distance).values[name])

    def assign_at(self, distance, name, type_, value):
        self.ancestor(distance).values[name.lexeme] = (type_, value)
