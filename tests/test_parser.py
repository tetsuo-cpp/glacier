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
        for e in self.exprs:
            print(e)
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
                ast.Member("name", ast.Type.STRING, "string"),
                ast.Member("age", ast.Type.INT, "int")
            ], [])
        ]
        self._test_parse_impl(buf, exprs)

    def test_function(self):
        buf = '''
        fn fooFunc(string name, int age) -> int {
          return 1;
        }
        '''
        exprs = [
            ast.Function("fooFunc", [
                ("name", ast.Type.STRING, "string"),
                ("age", ast.Type.INT, "int")
            ], [
                ast.ReturnStatement(ast.Number(1))
            ], ("int", ast.Type.INT))
        ]
        self._test_parse_impl(buf, exprs)

    def test_struct_with_member_functions(self):
        buf = '''
        struct Foo {
          string name;
          int age;
          fn memberFunc() -> int {
            return age;
          }
        };
        '''
        exprs = [
            ast.Structure("Foo", [
                ast.Member("name", ast.Type.STRING, "string"),
                ast.Member("age", ast.Type.INT, "int")
            ], [
                ast.Function("memberFunc", [], [
                    ast.ReturnStatement(None)
                ], ("int", ast.Type.INT))
            ])
        ]
        self._test_parse_impl(buf, exprs)

    def test_let_statement(self):
        buf = '''
        fn letFunc() -> int {
          let x = 1;
          return x;
        }
        '''
        exprs = [
            ast.Function("letFunc", [], [
                ast.LetStatement("x", ast.Number(1)),
                ast.ReturnStatement(None)
            ], ("int", ast.Type.INT))
        ]
        self._test_parse_impl(buf, exprs)


if __name__ == '__main__':
    unittest.main()
