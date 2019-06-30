from glacier.lexer import TokenType
import glacier.ast as ast


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        assert len(self.tokens) > 0
        self.cur_tok = self.tokens[0]

    def parse_top_level_expr(self):
        # Parse top level expressions.
        if self._consume_token(TokenType.FUNCTION):
            return self._parse_function()
        if self._consume_token(TokenType.STRUCTURE):
            return self._parse_structure()

        # If we get down here, it should be EOF.
        # If not, then this is malformed.
        if not self._consume_token(TokenType.EOF):
            raise RuntimeError("unrecognised top level expr: Token=({0})".format(self.cur_tok))

        return None

    def _next_token(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.cur_tok = self.tokens[self.pos]
        else:
            self.cur_tok = None

    def _consume_token(self, token_type):
        if self.cur_tok is None or self.cur_tok.type != token_type:
            return False
        self._next_token()
        return True

    def _expect_token(self, token_type):
        if not self._consume_token(token_type):
            raise RuntimeError(
                "unexpected token: Got=({0}), Expected=({1})".format(
                    self.cur_tok.type, token_type))

    def _parse_function(self):
        f_name = self.cur_tok.value
        self._expect_token(TokenType.IDENTIFIER)
        return ast.Function(f_name, [])

    def _parse_structure(self):
        s_name = self.cur_tok.value
        self._expect_token(TokenType.IDENTIFIER)
        self._expect_token(TokenType.L_BRACE)

        # Parse members.
        members = []
        while not (self.cur_tok.type == TokenType.FUNCTION or
                   self.cur_tok.type == TokenType.R_BRACE):
            members.append(self._parse_member())

        while self._consume_token(TokenType.FUNCTION):
            pass

        self._expect_token(TokenType.R_BRACE)
        self._expect_token(TokenType.SEMICOLON)
        return ast.Structure(s_name, members)

    def _parse_member(self):
        m_type = ast.Type.USER
        if self._consume_token(TokenType.INT):
            m_type = ast.Type.INT
        elif self._consume_token(TokenType.STRING):
            m_type = ast.Type.STRING
        else:
            self._expect_token(TokenType.IDENTIFIER)
        m_name = self.cur_tok.value
        self._expect_token(TokenType.IDENTIFIER)
        self._expect_token(TokenType.SEMICOLON)
        return m_type, m_name
