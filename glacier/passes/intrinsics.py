from glacier.bytecode import OpCode
from .. import ast


class IntrinsicFunction:
    def __init__(self, name, codegen, type_check):
        self.name = name
        self.codegen = codegen
        self.type_check = type_check


def _print_type_check(type_check, expr):
    if len(expr.args) != 1:
        raise TypeError('The "print" builtin takes 1 argument')
    print_arg = expr.args[0]
    type_check._walk(print_arg)
    if (
        print_arg.ret_type.kind != ast.TypeKind.INT
        and print_arg.ret_type.kind != ast.TypeKind.STRING
    ):
        raise TypeError(
            'The "print" builtin can take either int or string arguments, got {}'.format(
                print_arg.ret_type.kind
            )
        )


def _print_codegen(codegen, expr):
    # Type check should verified this already.
    assert len(expr.args) == 1
    codegen._walk(expr.args[0])
    codegen.bc.write_op(OpCode.PRINT)


def _push_type_check(type_check, expr):
    if len(expr.args) != 2:
        raise TypeError('The "push" builtin takes 2 arguments')
    vec_arg = expr.args[0]
    push_arg = expr.args[1]
    type_check._walk(vec_arg)
    if vec_arg.ret_type.kind != ast.TypeKind.VECTOR:
        raise TypeError(
            'The "push" builtin requires the first argument to be the vector to push onto'
        )
    type_check._walk(push_arg)
    if push_arg.ret_type.kind != vec_arg.ret_type.container_type.kind:
        raise TypeError(
            'Attempted to "push" argument of type {} onto a vector holding {}'.format(
                push_arg.ret_type.kind, vec_arg.ret_type.container_type.kind
            )
        )


def _push_codegen(codegen, expr):
    assert len(expr.args) == 2
    codegen._walk(expr.args[0])
    codegen._walk(expr.args[1])
    codegen.bc.write_op(OpCode.VEC_PUSH)


def _len_type_check(type_check, expr):
    if len(expr.args) != 1:
        raise TypeError('The "len" builtin takes 1 argument')
    len_arg = expr.args[0]
    type_check._walk(len_arg)
    if len_arg.ret_type.kind != ast.TypeKind.VECTOR:
        raise TypeError(
            'The "len" builtin takes a vector argument, got {}'.format(len_arg.ret_type.kind)
        )
    expr.ret_type = ast.Type(ast.TypeKind.INT)


def _len_codegen(codegen, expr):
    assert len(expr.args) == 1
    codegen._walk(expr.args[0])
    codegen.bc.write_op(OpCode.VEC_LEN)


def _pop_type_check(type_check, expr):
    if len(expr.args) != 1:
        raise TypeError('The "pop" builtin takes 1 argument')
    pop_arg = expr.args[0]
    type_check._walk(pop_arg)
    if pop_arg.ret_type.kind != ast.TypeKind.VECTOR:
        raise TypeError(
            'The "pop" builtin takes a vector argument, got {}'.format(pop_arg.ret_type.kind)
        )


def _pop_codegen(codegen, expr):
    assert len(expr.args) == 1
    codegen._walk(expr.args[0])
    codegen.bc.write_op(OpCode.VEC_POP)


INTRINSICS = [
    IntrinsicFunction("print", _print_codegen, _print_type_check),
    IntrinsicFunction("push", _push_codegen, _push_type_check),
    IntrinsicFunction("len", _len_codegen, _len_type_check),
    IntrinsicFunction("pop", _pop_codegen, _pop_type_check),
]


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
