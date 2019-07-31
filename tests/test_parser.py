import glacier.ast as ast
import unittest

from glacier.lexer import Lexer, TokenType, Token
from glacier.parser import Parser


class ParserTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = None
        self.exprs = list()

    def _test_parse_impl(self, buf, expected_exprs):
        lexer = Lexer(buf)
        tokens = list()
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
                    ast.ReturnStatement(ast.VariableRef("age"))
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
                ast.ReturnStatement(ast.VariableRef("x"))
            ], ("int", ast.Type.INT))
        ]
        self._test_parse_impl(buf, exprs)

    def test_function_call(self):
        buf = '''
        fn funcCall() -> int {
          return otherFunc();
        }
        '''
        exprs = [
            ast.Function("funcCall", [], [
                ast.ReturnStatement(ast.FunctionCall("otherFunc", []))
            ], ("int", ast.Type.INT))
        ]
        self._test_parse_impl(buf, exprs)

    def test_precedence(self):
        buf = '''
        fn prec() -> int {
          2 + 3 * 2 + 2 / 8;
        }
        '''
        exprs = [
            ast.Function("prec", [], [
                ast.ExprStatement(
                    ast.BinaryOp(
                        ast.BinaryOp(
                            ast.Number(2),
                            ast.BinaryOp(ast.Number(3), ast.Number(2), Token(TokenType.MULTIPLY, "*")),
                            Token(TokenType.ADD, "+")
                        ),
                        ast.BinaryOp(ast.Number(2), ast.Number(8), Token(TokenType.DIVIDE, "/")),
                        Token(TokenType.ADD, "+")
                    )
                )
            ], ("int", ast.Type.INT))
        ]
        self._test_parse_impl(buf, exprs)


if __name__ == '__main__':
    unittest.main()
