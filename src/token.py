from enum import Enum, auto


class TokenType(Enum):
    INTEGER = auto()
    IDENTIFIER = auto()
    STRING = auto()
    FN = auto()
    LET = auto()
    MUT = auto()
    RETURN = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    MATCH = auto()
    USE = auto()
    TRUE = auto()
    FALSE = auto()
    PRINTLN = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()
    EQ = auto()
    EQ_EQ = auto()
    NEQ = auto()
    GT = auto()
    LT = auto()
    GTE = auto()
    LTE = auto()
    ASSIGN = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    SEMICOLON = auto()
    COLON = auto()
    COMMA = auto()
    ARROW = auto()
    DOUBLE_COLON = auto()
    EOF = auto()


KEYWORDS = {
    "fn": TokenType.FN,
    "let": TokenType.LET,
    "mut": TokenType.MUT,
    "return": TokenType.RETURN,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "match": TokenType.MATCH,
    "use": TokenType.USE,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "println!": TokenType.PRINTLN,
}


class Token:
    __slots__ = ("type", "value", "line", "column")

    def __init__(self, type_: TokenType, value: object, line: int, column: int):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return (
            f"Token({self.type.name}, {self.value!r}, L:{self.line}, C:{self.column})"
        )
