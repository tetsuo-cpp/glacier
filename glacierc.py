from glacier.lexer import Lexer, TokenType


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
    print("Successfully lexed {} tokens.".format(len(tokens)))


if __name__ == "__main__":
    main()