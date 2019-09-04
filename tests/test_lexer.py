import unittest
from glacier.lexer import Lexer, TokenType, Token


class LexerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.lexer = None
        self.tokens = list()

    def _test_lex_impl(self, buf, expected_tokens):
        self.lexer = Lexer(buf)
        while True:
            tok = self.lexer.lex_token()
            self.tokens.append(tok)
            if tok.type == TokenType.EOF:
                break
        self.assertEqual(len(self.tokens), len(expected_tokens))
        for t, exp in zip(self.tokens, expected_tokens):
            self.assertEqual(t, exp, msg="Got=({0}), Expected=({1})".format(t, exp))

    def test_function(self):
        buf = """
        fn foo() -> int {
          print("blah");
        };
        """
        tokens = [
            Token(TokenType.FUNCTION, "fn"),
            Token(TokenType.IDENTIFIER, "foo"),
            Token(TokenType.L_BRACKET, "("),
            Token(TokenType.R_BRACKET, ")"),
            Token(TokenType.ARROW, "->"),
            Token(TokenType.INT, "int"),
            Token(TokenType.L_BRACE, "{"),
            Token(TokenType.IDENTIFIER, "print"),
            Token(TokenType.L_BRACKET, "("),
            Token(TokenType.STRING_LITERAL, "blah"),
            Token(TokenType.R_BRACKET, ")"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.R_BRACE, "}"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.EOF, str()),
        ]
        self._test_lex_impl(buf, tokens)

    def test_function_w_args(self):
        buf = """
        fn foo(int one, string two) -> int {
          print("blah");
        };
        """
        tokens = [
            Token(TokenType.FUNCTION, "fn"),
            Token(TokenType.IDENTIFIER, "foo"),
            Token(TokenType.L_BRACKET, "("),
            Token(TokenType.INT, "int"),
            Token(TokenType.IDENTIFIER, "one"),
            Token(TokenType.COMMA, ","),
            Token(TokenType.STRING, "string"),
            Token(TokenType.IDENTIFIER, "two"),
            Token(TokenType.R_BRACKET, ")"),
            Token(TokenType.ARROW, "->"),
            Token(TokenType.INT, "int"),
            Token(TokenType.L_BRACE, "{"),
            Token(TokenType.IDENTIFIER, "print"),
            Token(TokenType.L_BRACKET, "("),
            Token(TokenType.STRING_LITERAL, "blah"),
            Token(TokenType.R_BRACKET, ")"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.R_BRACE, "}"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.EOF, str()),
        ]
        self._test_lex_impl(buf, tokens)

    def test_struct(self):
        buf = """
        struct Foo {
          int id = 3;
          string name;
          fn foo() -> int {
            return 3;
          }
        };
        """
        tokens = [
            Token(TokenType.STRUCTURE, "struct"),
            Token(TokenType.IDENTIFIER, "Foo"),
            Token(TokenType.L_BRACE, "{"),
            Token(TokenType.INT, "int"),
            Token(TokenType.IDENTIFIER, "id"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.NUMBER_LITERAL, "3"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.STRING, "string"),
            Token(TokenType.IDENTIFIER, "name"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.FUNCTION, "fn"),
            Token(TokenType.IDENTIFIER, "foo"),
            Token(TokenType.L_BRACKET, "("),
            Token(TokenType.R_BRACKET, ")"),
            Token(TokenType.ARROW, "->"),
            Token(TokenType.INT, "int"),
            Token(TokenType.L_BRACE, "{"),
            Token(TokenType.RETURN, "return"),
            Token(TokenType.NUMBER_LITERAL, "3"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.R_BRACE, "}"),
            Token(TokenType.R_BRACE, "}"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.EOF, str()),
        ]
        self._test_lex_impl(buf, tokens)

    def test_control_flow(self):
        buf = """
        if (x == 3) {
          let y = 3;
        }
        """
        tokens = [
            Token(TokenType.IF, "if"),
            Token(TokenType.L_BRACKET, "("),
            Token(TokenType.IDENTIFIER, "x"),
            Token(TokenType.EQUALS, "=="),
            Token(TokenType.NUMBER_LITERAL, "3"),
            Token(TokenType.R_BRACKET, ")"),
            Token(TokenType.L_BRACE, "{"),
            Token(TokenType.LET, "let"),
            Token(TokenType.IDENTIFIER, "y"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.NUMBER_LITERAL, "3"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.R_BRACE, "}"),
            Token(TokenType.EOF, str()),
        ]
        self._test_lex_impl(buf, tokens)


if __name__ == "__main__":
    unittest.main()
