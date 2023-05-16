from enum import Enum

class TokenType(Enum):
    # Single-character tokens.
    LEFT_PAREN = '('
    RIGHT_PAREN = ')'
    LEFT_BRACE = '{'
    RIGHT_BRACE = '}'
    LEFT_BRACKET = '['
    RIGHT_BRACKET = ']'
    COMMA = ','
    DOT = '.'
    MINUS = '-'
    PLUS = '+'
    SEMICOLON = ';'
    SLASH = '/'
    STAR = '*'
    COLON = ':'

    # One or two character tokens.
    BANG = '!'
    BANG_EQUAL = '!='
    EQUAL = '='
    EQUAL_EQUAL = '=='
    GREATER = '>'
    GREATER_EQUAL = '>='
    LESS = '<'
    LESS_EQUAL = '<='

    MINUS_EQUAL = '-='
    PLUS_EQUAL = '+='
    SLASH_EQUAL = '/='
    STAR_EQUAL = '*='
    MINUS_MINUS = '--'
    PLUS_PLUS = '++'

    # Literals.
    IDENTIFIER = 'IDENTIFIER'
    STRING = 'STRING'
    NUMBER = 'NUMBER'

    # Keywords.
    AND = 'and'
    CLASS = 'class'
    ELSE = 'else'
    FALSE = 'false'
    FUN = 'fun'
    FOR = 'for'
    IF = 'if'
    NIL = 'nil'
    OR = 'or'
    PRINT = 'print'
    RETURN = 'return'
    SUPER = 'super'
    TRUE = 'true'
    VAR = 'var'
    WHILE = 'while'

    # End of file.
    EOF = 'EOF'

    # Optional
    NONE = 'none'

