import click
from glacier.bytecode import ByteCode
from glacier.passes.codegen import CodeGenerator
from glacier.passes.struct_defs import StructureDefinitions
from glacier.passes.function_table import FunctionTable
from glacier.lexer import Lexer, TokenType
from glacier.parser import Parser


def print_tokens(tokens):
    print("=== Printing tokens ===")
    for t in tokens:
        print(tok)
        if t.type == TokenType.EOF:
            break
    print("=== Printed {} tokens ===".format(len(tokens)))


def print_ast(exprs):
    print("=== Printing AST ===")
    for e in exprs:
        if e is None:
            break
        print(e)
    print("=== Printed {} top level exprs ===".format(len(exprs)))


def print_bc(bc):
    print("=== Printing bytecode ===")
    print(bc.construct())
    print("=== Printed bytecode ===")


@click.command()
@click.argument("src", nargs=1)
@click.option("-o", default="a.bc", help="Write bytecode to <file>")
@click.option("--print_tokens", default=False, help="Print tokens to stdout")
@click.option("--print_ast", default=False, help="Print AST to stdout")
@click.option("--print_bc", default=False, help="Print bytecode to stdout")
def glacierc_compile(src, o, print_tokens, print_ast, print_bc):
    with open(src) as f:
        lexer = Lexer(f.read())

    tokens = list()
    while True:
        tok = lexer.lex_token()
        tokens.append(tok)
        if tok.type == TokenType.EOF:
            break
    if print_tokens:
        print_tokens(tokens)

    parser = Parser(tokens)
    exprs = list()
    while True:
        expr = parser.parse_top_level_expr()
        if expr is None:
            break
        exprs.append(expr)
    if print_ast:
        print_ast(exprs)

    bc = ByteCode()
    structs = dict()
    passes = [StructureDefinitions(bc, structs), CodeGenerator(bc, structs), FunctionTable(bc)]
    for p in passes:
        p.walk_ast(exprs)
    if print_bc:
        print_bc(bc)

    with open(o, "wb") as f:
        f.write(bc.construct())


if __name__ == "__main__":
    glacierc_compile()
