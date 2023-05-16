from Token.token_type import TokenType
from Token.token import Token
from Runtime.Language_.callbacks import scanner_error
from Runtime.interpreter import can_convert_to_int

class Scanner:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self):
        c = self.advance()
        if c == "(":
            self.add_token(TokenType.LEFT_PAREN)
        elif c == ")":
            self.add_token(TokenType.RIGHT_PAREN)
        elif c == "{":
            self.add_token(TokenType.LEFT_BRACE)
        elif c == "}":
            self.add_token(TokenType.RIGHT_BRACE)
        elif c == "[":
            self.add_token(TokenType.LEFT_BRACKET)
        elif c == "]":
            self.add_token(TokenType.RIGHT_BRACKET)
        elif c == ":":
            self.add_token(TokenType.COLON)
        elif c == ",":
            self.add_token(TokenType.COMMA)
        elif c == ".":
            self.add_token(TokenType.DOT)
        elif c == "-":
            self.add_token(TokenType.MINUS_EQUAL if self.match("=") else TokenType.MINUS)
        elif c == "+":
            self.add_token(TokenType.PLUS_EQUAL if self.match("=") else TokenType.PLUS)
        elif c == ";":
            self.add_token(TokenType.SEMICOLON)
        elif c == "*":
            self.add_token(TokenType.STAR_EQUAL if self.match("=") else TokenType.STAR)
        elif c == "!":
            self.add_token(TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG)
        elif c == "=":
            self.add_token(TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL)
        elif c == "<":
            self.add_token(TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS)
        elif c == ">":
            self.add_token(TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER)
        elif c == "/":
            if self.match("/"):
                while self.peek() != "\n" and not self.is_at_end():
                    self.advance()
            else:
                self.add_token(TokenType.SLASH_EQUAL if self.match("=") else TokenType.SLASH)
        elif c in {" ", "\r", "\t"}:
            pass
        elif c == "\n":
            self.line += 1
        elif c == "\"":
            self.string()
        else:
            if c.isdigit():
                self.number()
            elif c.isalpha() or c == "_" or c == "&" or c == "|":
                self.identifier()
            else:
                Scanner.error(self.line, "Unexpected character.")

    def identifier(self):
        while self.peek().isalnum() or self.peek() in {"_", "&", "|"}:
            self.advance()

        text = self.source[self.start:self.current]
        type_ = KEYWORDS.get(text, TokenType.IDENTIFIER)

        saved_position = self.current
        if type_ == TokenType.VAR:
            while self.peek() in {" ", "[", "]"}:
                self.advance()
            if self.peek().isalpha() or self.peek() in {"_", "&", "|"}:
                self.advance()
                while self.peek().isalnum() or self.peek() in {"_", "&", "|"}:
                    self.advance()
                while self.peek() == " ":
                    self.advance()
                if self.peek() == "(":
                    type_ = TokenType.FUN

        self.current = saved_position
        self.add_token(type_)

    def number(self):
        while self.peek().isdigit():
            self.advance()

        if self.peek() == "." and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()

        value = float(self.source[self.start:self.current])
        if can_convert_to_int(value):
            value = int(value)
        self.add_token(TokenType.NUMBER, value)

    def string(self):
        while self.peek() != "\"" and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.is_at_end():
            Scanner.error(self.line, "Unterminated string.")
            return

        self.advance()
        value = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, value)

    def match(self, expected):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self):
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def is_at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, type_, literal=None):
        text = self.source[self.start:self.current]
        token = Token(type_, text, literal, self.line)
        self.tokens.append(token)

    def error(self, line, message):
        scanner_error(line, message)


KEYWORDS = {
    "&&": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "if": TokenType.IF,
    "null": TokenType.NIL,
    "||": TokenType.OR,
    "WriteLine": TokenType.PRINT,
    "return": TokenType.RETURN,
    "base": TokenType.SUPER,
    "true": TokenType.TRUE,
    "while": TokenType.WHILE,
    "int": TokenType.VAR,
    "string": TokenType.VAR,
    "char": TokenType.VAR,
    "float": TokenType.VAR,
    "bool": TokenType.VAR,
    "void": TokenType.FUN,
}
