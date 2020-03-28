import compiler.ast as ast
import unittest
from compiler.lexer import Lexer, TokenType, Token
from compiler.parser import Parser


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
        buf = """
        struct Foo {
          string name;
          int age;
        };
        """
        exprs = [
            ast.Structure(
                "Foo",
                [
                    ast.Member("name", ast.Type(ast.TypeKind.STRING)),
                    ast.Member("age", ast.Type(ast.TypeKind.INT)),
                ],
                [],
            )
        ]
        self._test_parse_impl(buf, exprs)

    def test_function(self):
        buf = """
        fn fooFunc(string name, int age) -> int {
          return 1;
        }
        """
        exprs = [
            ast.Function(
                "fooFunc",
                [("name", ast.Type(ast.TypeKind.STRING)), ("age", ast.Type(ast.TypeKind.INT))],
                [ast.ReturnStatement(ast.Number(1))],
                ast.Type(ast.TypeKind.INT),
            )
        ]
        self._test_parse_impl(buf, exprs)

    def test_struct_with_member_functions(self):
        buf = """
        struct Foo {
          string name;
          int age;
          fn memberFunc() -> int {
            return age;
          }
        };
        """
        exprs = [
            ast.Structure(
                "Foo",
                [
                    ast.Member("name", ast.Type(ast.TypeKind.STRING)),
                    ast.Member("age", ast.Type(ast.TypeKind.INT)),
                ],
                [
                    ast.Function(
                        "memberFunc",
                        [("this", ast.Type(ast.TypeKind.USER, "Foo"))],
                        [ast.ReturnStatement(ast.VariableRef("age"))],
                        ast.Type(ast.TypeKind.INT),
                    )
                ],
            )
        ]
        self._test_parse_impl(buf, exprs)

    def test_let_statement(self):
        buf = """
        fn letFunc() -> int {
          let x = 1;
          return x;
        }
        """
        exprs = [
            ast.Function(
                "letFunc",
                [],
                [ast.LetStatement("x", ast.Number(1)), ast.ReturnStatement(ast.VariableRef("x"))],
                ast.Type(ast.TypeKind.INT),
            )
        ]
        self._test_parse_impl(buf, exprs)

    def test_function_call(self):
        buf = """
        fn funcCall() -> int {
          return otherFunc();
        }
        """
        exprs = [
            ast.Function(
                "funcCall",
                [],
                [ast.ReturnStatement(ast.FunctionCall("otherFunc", []))],
                ast.Type(ast.TypeKind.INT),
            )
        ]
        self._test_parse_impl(buf, exprs)

    def test_precedence(self):
        buf = """
        fn prec() -> int {
          2 + 3 * 2 + 2 / 8;
        }
        """
        exprs = [
            ast.Function(
                "prec",
                [],
                [
                    ast.ExprStatement(
                        ast.BinaryOp(
                            ast.BinaryOp(
                                ast.Number(2),
                                ast.BinaryOp(
                                    ast.Number(3), ast.Number(2), Token(TokenType.MULTIPLY, "*")
                                ),
                                Token(TokenType.ADD, "+"),
                            ),
                            ast.BinaryOp(
                                ast.Number(2), ast.Number(8), Token(TokenType.DIVIDE, "/")
                            ),
                            Token(TokenType.ADD, "+"),
                        )
                    )
                ],
                ast.Type(ast.TypeKind.INT),
            )
        ]
        self._test_parse_impl(buf, exprs)

    def test_string_literals(self):
        buf = """
        fn fooString() -> string {
          return "string_literal_value";
        }
        """
        exprs = [
            ast.Function(
                "fooString",
                [],
                [ast.ReturnStatement(ast.String("string_literal_value"))],
                ast.Type(ast.TypeKind.STRING),
            )
        ]
        self._test_parse_impl(buf, exprs)

    def test_if_statements(self):
        buf = """
        fn foo() -> string {
          if (3 == 3) {
            return "foo";
          }
          return "bar";
        }
        """
        exprs = [
            ast.Function(
                "foo",
                [],
                [
                    ast.IfStatement(
                        ast.BinaryOp(ast.Number(3), ast.Number(3), Token(TokenType.EQUALS, "==")),
                        [ast.ReturnStatement(ast.String("foo"))],
                        list(),
                    ),
                    ast.ReturnStatement(ast.String("bar")),
                ],
                ast.Type(ast.TypeKind.STRING),
            )
        ]
        self._test_parse_impl(buf, exprs)

    def test_member_access(self):
        buf = """
        fn foo() -> int {
          return bar.age;
        }
        """
        exprs = [
            ast.Function(
                "foo",
                [],
                [ast.ReturnStatement(ast.MemberAccess(ast.VariableRef("bar"), "age"))],
                ast.Type(ast.TypeKind.INT),
            )
        ]
        self._test_parse_impl(buf, exprs)

    def test_constructor(self):
        buf = """
        fn constructorTest() -> int {
          let foo = new Foo(name, age);
          return 0;
        }
        """
        exprs = [
            ast.Function(
                "constructorTest",
                [],
                [
                    ast.LetStatement(
                        "foo",
                        ast.Constructor("Foo", [ast.VariableRef("name"), ast.VariableRef("age")]),
                    ),
                    ast.ReturnStatement(ast.Number(0)),
                ],
                ast.Type(ast.TypeKind.INT),
            )
        ]
        self._test_parse_impl(buf, exprs)

    def test_while_loop(self):
        buf = """
        fn loopTest(int x) -> int {
          while (x < 5) {
            print("blah");
          }
          return 0;
        }
        """
        exprs = [
            ast.Function(
                "loopTest",
                [("x", ast.Type(ast.TypeKind.INT))],
                [
                    ast.WhileLoop(
                        ast.BinaryOp(
                            ast.VariableRef("x"), ast.Number(5), Token(TokenType.LESS_THAN, "<")
                        ),
                        [ast.ExprStatement(ast.FunctionCall("print", [ast.String("blah")]))],
                    ),
                    ast.ReturnStatement(ast.Number(0)),
                ],
                ast.Type(ast.TypeKind.INT),
            )
        ]
        self._test_parse_impl(buf, exprs)


if __name__ == "__main__":
    unittest.main()
