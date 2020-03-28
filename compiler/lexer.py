from enum import Enum


class TokenType(Enum):
    EOF = 0
    IDENTIFIER = 1
    NUMBER_LITERAL = 2
    STRING_LITERAL = 3
    STRUCTURE = 4
    FUNCTION = 5
    LET = 6
    IF = 7
    ELSE = 8
    L_BRACE = 9
    R_BRACE = 10
    L_BRACKET = 11
    R_BRACKET = 12
    SEMICOLON = 13
    ASSIGN = 14
    ARROW = 15
    EQUALS = 16
    INT = 17
    STRING = 18
    COMMA = 19
    RETURN = 20
    L_PAREN = 21
    R_PAREN = 22
    NOT_EQUALS = 23
    LESS_THAN = 24
    LESS_THAN_EQ = 25
    GREATER_THAN = 26
    GREATER_THAN_EQ = 27
    ADD = 28
    SUBTRACT = 29
    MULTIPLY = 30
    DIVIDE = 31
    DOT = 32
    NEW = 33
    WHILE = 34
    VECTOR = 35
    MAP = 36
    COLON = 37
    VOID = 38


class Token:
    def __init__(self, token_type, value=str()):
        self.type = token_type
        self.value = value

    def __str__(self):
        return 'Token(Type={0}, Value="{1}")'.format(self.type, self.value)

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value


KEYWORDS = {
    "struct": TokenType.STRUCTURE,
    "fn": TokenType.FUNCTION,
    "let": TokenType.LET,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "int": TokenType.INT,
    "string": TokenType.STRING,
    "return": TokenType.RETURN,
    "new": TokenType.NEW,
    "while": TokenType.WHILE,
    "vector": TokenType.VECTOR,
    "map": TokenType.MAP,
    "void": TokenType.VOID,
}

SYMBOLS = {
    "{": TokenType.L_BRACE,
    "}": TokenType.R_BRACE,
    "(": TokenType.L_BRACKET,
    ")": TokenType.R_BRACKET,
    ";": TokenType.SEMICOLON,
    "=": TokenType.ASSIGN,
    "->": TokenType.ARROW,
    "==": TokenType.EQUALS,
    ",": TokenType.COMMA,
    "[": TokenType.L_PAREN,
    "]": TokenType.R_PAREN,
    "!=": TokenType.NOT_EQUALS,
    "<": TokenType.LESS_THAN,
    "<=": TokenType.LESS_THAN_EQ,
    ">": TokenType.GREATER_THAN,
    ">=": TokenType.GREATER_THAN_EQ,
    "+": TokenType.ADD,
    "-": TokenType.SUBTRACT,
    "*": TokenType.MULTIPLY,
    "/": TokenType.DIVIDE,
    ".": TokenType.DOT,
    ":": TokenType.COLON,
}


class Lexer:
    def __init__(self, buffer):
        self.buffer = buffer
        self.pos = 0
        self._get_char()

    def lex_token(self):
        self._trim_whitespace()
        if self.cur_char is None:
            return Token(TokenType.EOF)
        if self.cur_char.isnumeric():
            return self._lex_number()
        if self.cur_char.isalpha():
            return self._lex_identifier()
        if self.cur_char == '"':
            return self._lex_string()
        return self._lex_symbol()

    def _get_char(self):
        if self.pos >= len(self.buffer):
            self.cur_char = None
            return
        self.cur_char = self.buffer[self.pos]
        self.pos += 1

    def _trim_whitespace(self):
        while self.cur_char is not None and self.cur_char.isspace():
            self._get_char()

    def _lex_number(self):
        value = self.cur_char
        while True:
            self._get_char()
            if self.cur_char is not None and self.cur_char.isnumeric():
                value += self.cur_char
            else:
                break
        return Token(TokenType.NUMBER_LITERAL, value)

    def _lex_identifier(self):
        value = self.cur_char
        while True:
            self._get_char()
            if self.cur_char is not None and self.cur_char.isalnum():
                value += self.cur_char
            else:
                break
        if value in KEYWORDS:
            return Token(KEYWORDS[value], value)
        return Token(TokenType.IDENTIFIER, value)

    def _lex_string(self):
        value = str()
        while True:
            self._get_char()
            if self.cur_char is not None and self.cur_char != '"':
                value += self.cur_char
            else:
                break
        if self.cur_char is None:
            raise RuntimeError("encountered string with no closing quote")
        self._get_char()
        return Token(TokenType.STRING_LITERAL, value)

    def _lex_symbol(self):
        # This technique only works for two char compound symbols.
        single = self.cur_char
        self._get_char()
        compound = None
        if self.cur_char is not None:
            compound = single + self.cur_char
        if compound in SYMBOLS:
            self._get_char()
            return Token(SYMBOLS[compound], compound)
        elif single in SYMBOLS:
            return Token(SYMBOLS[single], single)
        else:
            return None
