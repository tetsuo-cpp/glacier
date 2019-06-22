from enum import Enum


class TokenType(Enum):
    EOF = 0,
    IDENTIFIER = 1,
    NUMBER_LITERAL = 2,
    STRING_LITERAL = 3,
    STRUCTURE = 4,
    FUNCTION = 5,
    LET = 6,
    IF = 7,
    ELSE = 8,
    L_BRACE = 9,
    R_BRACE = 10,
    L_BRACKET = 11,
    R_BRACKET = 12,
    SEMICOLON = 13,
    ASSIGNMENT = 14,
    ARROW = 15,
    EQUALS = 16,
    INT = 17,
    STRING = 18,
    COMMA = 19,
    RETURN = 20


class Token:
    def __init__(self, token_type, value=str()):
        self.type = token_type
        self.value = value

    def __str__(self):
        return "Type={0}, Value=\"{1}\"".format(self.type, self.value)

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value;


KEYWORDS = {
    "struct": TokenType.STRUCTURE,
    "fn": TokenType.FUNCTION,
    "let": TokenType.LET,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "int": TokenType.INT,
    "string": TokenType.STRING,
    "return": TokenType.RETURN
}

SYMBOLS = {
    "{": TokenType.L_BRACE,
    "}": TokenType.R_BRACE,
    "(": TokenType.L_BRACKET,
    ")": TokenType.R_BRACKET,
    ";": TokenType.SEMICOLON,
    "=": TokenType.ASSIGNMENT,
    "->": TokenType.ARROW,
    "==": TokenType.EQUALS,
    ",": TokenType.COMMA
}


class Lexer:
    def __init__(self, buffer):
        self.buffer = buffer
        self.pos = 0
        self._get_char()

    def _get_char(self):
        if self.pos >= len(self.buffer):
            self.cur_char = None
            return
        self.cur_char = self.buffer[self.pos]
        self.pos += 1

    def lex_token(self):
        self._trim_whitespace()
        if self.cur_char is None:
            return Token(TokenType.EOF)
        if self.cur_char.isnumeric():
            return self._lex_number()
        if self.cur_char.isalpha():
            return self._lex_identifier()
        if self.cur_char == "\"":
            return self._lex_string()
        return self._lex_symbol()

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
            if self.cur_char is not None and self.cur_char != "\"":
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
        compound = single + self.cur_char
        if compound in SYMBOLS:
            self._get_char()
            return Token(SYMBOLS[compound], compound)
        elif single in SYMBOLS:
            return Token(SYMBOLS[single], single)
        else:
            return None
