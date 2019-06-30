from glacier.lexer import Lexer, TokenType
from glacier.parser import Parser


def main():
    file_name = "test.glac"
    lexer = Lexer(file_name)
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


if __name__ == "__main__":
    main()
