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
        self._expect_token(TokenType.L_BRACKET)

        # Parse function arguments.
        args = []
        while not self._consume_token(TokenType.R_BRACKET):
            if args:
                self._expect_token(TokenType.COMMA)
            arg_type_name = self.cur_tok.value
            arg_type = self._parse_type()
            arg_name = self.cur_tok.value
            self._expect_token(TokenType.IDENTIFIER)
            args.append((arg_name, arg_type, arg_type_name))

        # Parse return type.
        self._expect_token(TokenType.ARROW)
        return_type_name = self.cur_tok.value
        return_type = self._parse_type()

        self._expect_token(TokenType.L_BRACE)
        statements = []
        while not self._consume_token(TokenType.R_BRACE):
            statements.append(self._parse_statement())

        return ast.Function(f_name, args, statements, (return_type_name, return_type))

    def _parse_structure(self):
        s_name = self.cur_tok.value
        self._expect_token(TokenType.IDENTIFIER)
        self._expect_token(TokenType.L_BRACE)

        # Parse members.
        members = []
        while not (self.cur_tok.type == TokenType.FUNCTION or
                   self.cur_tok.type == TokenType.R_BRACE):
            members.append(self._parse_member())

        member_functions = []
        while self._consume_token(TokenType.FUNCTION):
            member_functions.append(self._parse_function())

        self._expect_token(TokenType.R_BRACE)
        self._expect_token(TokenType.SEMICOLON)
        return ast.Structure(s_name, members, member_functions)

    def _parse_member(self):
        m_type_name = self.cur_tok.value
        m_type = self._parse_type()
        m_name = self.cur_tok.value
        self._expect_token(TokenType.IDENTIFIER)
        self._expect_token(TokenType.SEMICOLON)
        return ast.Member(m_name, m_type, m_type_name)

    def _parse_type(self):
        if self._consume_token(TokenType.INT):
            return ast.Type.INT
        elif self._consume_token(TokenType.STRING):
            return ast.Type.STRING
        else:
            # User defined type. Should just look like a regular identifier.
            self._expect_token(TokenType.IDENTIFIER)
            return ast.Type.USER

    def _parse_statement(self):
        if self._consume_token(TokenType.LET):
            return self._parse_let()
        elif self._consume_token(TokenType.RETURN):
            return self._parse_return()
        else:
            raise RuntimeError("unknown statement type: Token=({0})".format(self.cur_tok))

    def _parse_let(self):
        v_name = self.cur_tok.value
        self._expect_token(TokenType.IDENTIFIER)
        self._expect_token(TokenType.ASSIGNMENT)
        v_expr = self._parse_expr()
        return ast.LetStatement(v_name, v_expr)

    def _parse_return(self):
        expr = self._parse_expr()
        return ast.ReturnStatement(expr)

    def _parse_expr(self):
        # Need to do Pratt parsing here like in Monkey.
        # For the time being, let's just make sure we understand literals.
        value = self.cur_tok.value
        expr = None
        if self._consume_token(TokenType.NUMBER_LITERAL):
            expr = ast.Number(int(value))
        elif self._consume_token(TokenType.STRING_LITERAL):
            expr = ast.String(value)

        while not self._consume_token(TokenType.SEMICOLON):
            self._next_token()
        return expr
