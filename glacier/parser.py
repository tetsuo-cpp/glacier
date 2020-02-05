import glacier.ast as ast
from glacier.lexer import TokenType


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
                "unexpected token: Got=({0}), Expected=({1})".format(self.cur_tok.type, token_type)
            )

    def _parse_function(self, this=None):
        f_name = self.cur_tok.value
        self._expect_token(TokenType.IDENTIFIER)
        self._expect_token(TokenType.L_BRACKET)

        # Parse function arguments.
        args = list()
        while not self._consume_token(TokenType.R_BRACKET):
            if args:
                self._expect_token(TokenType.COMMA)
            arg_type = self._parse_type()
            arg_name = self.cur_tok.value
            self._expect_token(TokenType.IDENTIFIER)
            args.append((arg_name, arg_type))

        # Parse return type.
        self._expect_token(TokenType.ARROW)
        return_type = self._parse_type()

        self._expect_token(TokenType.L_BRACE)
        statements = list()
        while not self._consume_token(TokenType.R_BRACE):
            statements.append(self._parse_statement())

        if this is not None:
            args.insert(0, this)

        return ast.Function(f_name, args, statements, return_type)

    def _parse_structure(self):
        s_name = self.cur_tok.value
        self._expect_token(TokenType.IDENTIFIER)
        self._expect_token(TokenType.L_BRACE)

        # Parse members.
        members = list()
        while not (
            self.cur_tok.type == TokenType.FUNCTION or self.cur_tok.type == TokenType.R_BRACE
        ):
            members.append(self._parse_member())

        member_functions = list()
        while self._consume_token(TokenType.FUNCTION):
            member_functions.append(
                self._parse_function(("this", ast.Type(ast.TypeKind.USER, s_name)))
            )

        self._expect_token(TokenType.R_BRACE)
        self._expect_token(TokenType.SEMICOLON)
        return ast.Structure(s_name, members, member_functions)

    def _parse_member(self):
        m_type = self._parse_type()
        m_name = self.cur_tok.value
        self._expect_token(TokenType.IDENTIFIER)
        default_value = None
        if self._consume_token(TokenType.ASSIGN):
            default_value = self._parse_primary_expr()
        self._expect_token(TokenType.SEMICOLON)
        return ast.Member(m_name, m_type, default_value)

    def _parse_type(self):
        if self._consume_token(TokenType.INT):
            return ast.Type(ast.TypeKind.INT)
        elif self._consume_token(TokenType.STRING):
            return ast.Type(ast.TypeKind.STRING)
        else:
            # User defined type. Should just look like a regular identifier.
            identifier = self.cur_tok.value
            self._expect_token(TokenType.IDENTIFIER)
            return ast.Type(ast.TypeKind.USER, identifier)

    def _parse_statement(self):
        if self._consume_token(TokenType.LET):
            return self._parse_let()
        elif self._consume_token(TokenType.RETURN):
            return self._parse_return()
        elif self._consume_token(TokenType.IF):
            return self._parse_if_statement()
        elif self._consume_token(TokenType.WHILE):
            return self._parse_while_loop()
        else:
            return self._parse_expr_statement()

    def _parse_let(self):
        v_name = self.cur_tok.value
        self._expect_token(TokenType.IDENTIFIER)
        self._expect_token(TokenType.ASSIGN)
        v_expr = self._parse_expr()
        while not self._consume_token(TokenType.SEMICOLON):
            self._next_token()
        return ast.LetStatement(v_name, v_expr)

    def _parse_return(self):
        expr = self._parse_expr()
        while not self._consume_token(TokenType.SEMICOLON):
            self._next_token()
        return ast.ReturnStatement(expr)

    def _parse_if_statement(self):
        self._expect_token(TokenType.L_BRACKET)
        cond = self._parse_expr()
        self._expect_token(TokenType.R_BRACKET)
        self._expect_token(TokenType.L_BRACE)

        then_statements = list()
        while not self._consume_token(TokenType.R_BRACE):
            then_statements.append(self._parse_statement())

        else_statements = list()
        if self._consume_token(TokenType.ELSE):
            self._expect_token(TokenType.L_BRACE)
            while not self._consume_token(TokenType.R_BRACE):
                else_statements.append(self._parse_statement())

        return ast.IfStatement(cond, then_statements, else_statements)

    def _parse_while_loop(self):
        self._expect_token(TokenType.L_BRACKET)
        cond = self._parse_expr()
        self._expect_token(TokenType.R_BRACKET)
        self._expect_token(TokenType.L_BRACE)

        # Parse the contents of the loop.
        loop_body = list()
        while not self._consume_token(TokenType.R_BRACE):
            loop_body.append(self._parse_statement())

        return ast.WhileLoop(cond, loop_body)

    def _parse_expr_statement(self):
        expr = self._parse_expr()
        while not self._consume_token(TokenType.SEMICOLON):
            self._next_token()
        return ast.ExprStatement(expr)

    def _parse_expr(self):
        return self._parse_assignment()

    def _parse_assignment(self):
        lhs = self._parse_equality()
        while True:
            tok = self.cur_tok
            if self._consume_token(TokenType.ASSIGN):
                lhs = ast.BinaryOp(lhs, self._parse_equality(), tok)
            else:
                return lhs

    def _parse_equality(self):
        lhs = self._parse_relational()
        while True:
            tok = self.cur_tok
            if self._consume_token(TokenType.EQUALS) or self._consume_token(TokenType.NOT_EQUALS):
                lhs = ast.BinaryOp(lhs, self._parse_relational(), tok)
            else:
                return lhs

    def _parse_relational(self):
        lhs = self._parse_addition()
        while True:
            tok = self.cur_tok
            if (
                self._consume_token(TokenType.LESS_THAN)
                or self._consume_token(TokenType.LESS_THAN_EQ)
                or self._consume_token(TokenType.GREATER_THAN)
                or self._consume_token(TokenType.GREATER_THAN_EQ)
            ):
                lhs = ast.BinaryOp(lhs, self._parse_addition(), tok)
            else:
                return lhs

    def _parse_addition(self):
        lhs = self._parse_multiplication()
        while True:
            tok = self.cur_tok
            if self._consume_token(TokenType.ADD) or self._consume_token(TokenType.SUBTRACT):
                lhs = ast.BinaryOp(lhs, self._parse_multiplication(), tok)
            else:
                return lhs

    def _parse_multiplication(self):
        lhs = self._parse_postfix()
        while True:
            tok = self.cur_tok
            if self._consume_token(TokenType.MULTIPLY) or self._consume_token(TokenType.DIVIDE):
                lhs = ast.BinaryOp(lhs, self._parse_primary_expr(), tok)
            else:
                return lhs

    def _parse_postfix(self):
        expr = self._parse_primary_expr()
        while True:
            if self._consume_token(TokenType.DOT):
                member_name = self.cur_tok.value
                self._expect_token(TokenType.IDENTIFIER)
                if self._consume_token(TokenType.L_BRACKET):
                    expr = self._parse_function_call(member_name, expr)
                else:
                    expr = ast.MemberAccess(expr, member_name)
            else:
                break
        return expr

    def _parse_primary_expr(self):
        value = self.cur_tok.value
        expr = None
        if self._consume_token(TokenType.NUMBER_LITERAL):
            expr = ast.Number(int(value))
        elif self._consume_token(TokenType.STRING_LITERAL):
            expr = ast.String(value)
        elif self._consume_token(TokenType.L_PAREN):
            expr = self._parse_array()
        elif self._consume_token(TokenType.NEW):
            expr = self._parse_constructor()
        elif self._consume_token(TokenType.IDENTIFIER):
            if self._consume_token(TokenType.L_BRACKET):
                return self._parse_function_call(value)
            return ast.VariableRef(value)
        else:
            raise RuntimeError("unrecognised primary expression: Token=({0})".format(self.cur_tok))
        return expr

    def _parse_array(self):
        elements = list()
        while not self._consume_token(TokenType.R_PAREN):
            if elements:
                self._expect_token(TokenType.COMMA)
            elements.append(self._parse_expr())
        # Need a type decl for let exprs to work.
        self._expect_token(TokenType.LESS_THAN)
        container_type = self._parse_type()
        self._expect_token(TokenType.GREATER_THAN)
        return ast.Array(elements, container_type)

    def _parse_constructor(self):
        params = list()
        struct_name = self.cur_tok.value
        self._expect_token(TokenType.IDENTIFIER)
        self._expect_token(TokenType.L_BRACKET)
        while not self._consume_token(TokenType.R_BRACKET):
            if params:
                self._expect_token(TokenType.COMMA)
            params.append(self._parse_expr())
        return ast.Constructor(struct_name, params)

    def _parse_function_call(self, name, this=None):
        args = list()
        while not self._consume_token(TokenType.R_BRACKET):
            if args:
                self._expect_token(TokenType.COMMA)
            args.append(self._parse_expr())
        if this is not None:
            args.insert(0, this)
        return ast.FunctionCall(name, args)
