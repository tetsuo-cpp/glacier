import glacier.ast as ast
import unittest

from glacier.lexer import Lexer, TokenType
from glacier.parser import Parser


class ParserTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = None
        self.exprs = []

    def _test_parse_impl(self, buf, expected_exprs):
        lexer = Lexer(buf)
        tokens = []
        while True:
            tok = lexer.lex_token()
            tokens.append(tok)
            if tok.type == TokenType.EOF:
                break
        self.parser = Parser(tokens)
        while True:
            expr = self.parser.parse_top_level_expr()
            if expr is None:
                break
            self.exprs.append(expr)
        self.assertEqual(len(self.exprs), len(expected_exprs))
        for e, exp in zip(self.exprs, expected_exprs):
            self.assertEqual(e, exp)

    def test_struct(self):
        buf = '''
        struct Foo {
          string name;
          int age;
        };
        '''
        exprs = [
            ast.Structure("Foo", [
                (ast.Type.STRING, "name"),
                (ast.Type.INT, "age")
            ])
        ]
        self._test_parse_impl(buf, exprs)


if __name__ == '__main__':
    unittest.main()
