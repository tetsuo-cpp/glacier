from glacier.bytecode import ByteCode
from glacier.passes.codegen import CodeGenerator
from glacier.passes.struct_defs import StructureDefinitions
from glacier.lexer import Lexer, TokenType
from glacier.parser import Parser


def main():
    file_name = "test.glc"
    with open(file_name) as f:
        lexer = Lexer(f.read())

    tokens = list()
    while True:
        tok = lexer.lex_token()
        print(tok)
        tokens.append(tok)
        if tok.type == TokenType.EOF:
            break
    print("Successfully lexed {0} tokens.".format(len(tokens)))

    parser = Parser(tokens)
    exprs = list()
    while True:
        expr = parser.parse_top_level_expr()
        if expr is None:
            break
        print(expr)
        exprs.append(expr)
    print("Successfully parsed {0} top level expressions.".format(len(exprs)))

    bc = ByteCode()
    passes = [
        StructureDefinitions(bc),
        CodeGenerator(bc)
    ]
    for p in passes:
        p.walk_ast(exprs)
    print("Successfully generated bytecode {0}.".format(bc.buf))

    output_name = 'test.bc'
    with open(output_name, 'wb') as f:
        f.write(bc.buf)


if __name__ == "__main__":
    main()
