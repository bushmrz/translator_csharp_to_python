
class Token:
    def __init__(self, type, lexeme, literal, line):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return f"{self.type} {self.lexeme} {str(self.literal)}"

    def __eq__(self, other):
        return self.type == other.type and \
               self.lexeme == other.lexeme and \
               self.literal == other.literal and \
               self.line == other.line

    def __hash__(self):
        return hash((self.type, self.lexeme, str(self.literal), self.line))
