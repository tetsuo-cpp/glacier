from glacier.codegen import CodeGenerator
from glacier.lexer import Lexer, TokenType
from glacier.parser import Parser


def main():
    file_name = "test.glac"
    with open(file_name) as f:
        lexer = Lexer(f.read())
    tokens = []
    while True:
        tok = lexer.lex_token()
        print(tok)
        tokens.append(tok)
        if tok.type == TokenType.EOF:
            break
    print("Successfully lexed {0} tokens.".format(len(tokens)))
    parser = Parser(tokens)
    exprs = []
    while True:
        expr = parser.parse_top_level_expr()
        if expr is None:
            break
        print(expr)
        exprs.append(expr)
    print("Successfully parsed {0} top level expressions.".format(len(exprs)))
    codegen = CodeGenerator()
    codegen.walk_ast(exprs)


if __name__ == "__main__":
    main()
