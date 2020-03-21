from glacier.bytecode import OpCode
from .. import ast


class InstrinsicFunction:
    def __init__(self, name, codegen, type_check):
        self.name = name
        self.codegen = codegen
        self.type_check = type_check


def _print_type_check(type_check, expr):
    assert len(expr.args) == 1
    print_arg = expr.args[0]
    type_check._walk(print_arg)
    assert (
        print_arg.ret_type.kind == ast.TypeKind.INT
        or print_arg.ret_type.kind == ast.TypeKind.STRING
    )


def _print_codegen(codegen, expr):
    codegen._walk(expr.args[0])
    codegen.bc.write_op(OpCode.PRINT)


INTRINSICS = [InstrinsicFunction("print", _print_codegen, _print_type_check)]


class Intrinsics:
    def __init__(self):
        self.intrinsics = dict()
        for i in INTRINSICS:
            self._register_intrinsic(i)

    def _register_intrinsic(self, i):
        self.intrinsics[i.name] = i

    def is_intrinsic(self, name):
        return name in self.intrinsics

    def codegen(self, expr, codegen):
        assert self.is_intrinsic(expr.name)
        self.intrinsics[expr.name].codegen(codegen, expr)

    def type_check(self, expr, type_check):
        assert self.is_intrinsic(expr.name)
        self.intrinsics[expr.name].type_check(type_check, expr)
