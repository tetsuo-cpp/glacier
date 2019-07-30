from .. import ast, bytecode


class CodeGenerator(ast.AstWalker):
    def __init__(self, bc):
        self.bc = bc
        self.function_id = 1
        self.variables = dict()
        self.variable_id = 0

    def _walk_function(self, expr):
        args = list()
        args.append(self.function_id)
        args.append(len(expr.args))

        for s in expr.statements:
            self._walk(s)

        self.bc.write_op(bytecode.OpCode.FUNCTION_DEF, args)
        self.function_id += 1

    def _walk_return_statement(self, expr):
        if expr.expr is None:
            self.bc.write_op(bytecode.OpCode.RETURN, list())
            return
        self._walk(expr.expr)
        self.bc.write_op(bytecode.OpCode.RETURN_VAL, list())

    def _walk_number(self, expr):
        self.bc.write_op(bytecode.OpCode.INT, [expr.value])

    def _walk_string(self, expr):
        args = list()
        args.append(len(expr.value))
        args.extend([c for c in expr.value])
        self.bc.write_op(bytecode.OpCode.STRING, args)

    def _walk_let_statement(self, expr):
        if expr.name in self.variables:
            raise RuntimeError("variable {0} declared twice".format(expr.name))
        self.variables[expr.name] = self.variable_id
        self.bc.write_op(bytecode.OpCode.SET_VAR, [self.variable_id])
        self.variable_id += 1

    def _walk_variable(self, expr):
        if expr.name not in self.variables:
            raise RuntimeError("reference to unrecognised variable {0}".format(expr.name))
        self.bc.write_op(bytecode.OpCode.GET_VAR, [self.variables[expr.name]])
