from .. import ast, bytecode, lexer


class CodeGenerator(ast.ASTWalker):
    def __init__(self, bc):
        self.bc = bc
        self.functions = dict()
        self.function_id = 1
        self.variables = dict()
        self.variable_id = 0
        self.seen_main = False

    def _walk_function(self, expr):
        if expr.name == "main" and not self.seen_main:
            # Function id 0 is reserved for main.
            expr.function_id = 0
            self.main = True
        else:
            expr.function_id = self.function_id
        self.functions[expr.name] = expr.function_id
        expr.offset = self.bc.current_offset()
        args = list()
        args.append(expr.function_id)
        args.append(len(expr.args))
        self.bc.write_op(bytecode.OpCode.FUNCTION_DEF, args)
        self.function_id += 1
        for s in expr.statements:
            self._walk(s)

    def _walk_return_statement(self, expr):
        if expr.expr is None:
            self.bc.write_op(bytecode.OpCode.RETURN)
            return
        self._walk(expr.expr)
        self.bc.write_op(bytecode.OpCode.RETURN_VAL)

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
        self._walk(expr.rhs)
        self.variables[expr.name] = self.variable_id
        self.bc.write_op(bytecode.OpCode.SET_VAR, [self.variable_id])
        self.variable_id += 1

    def _walk_binary_op(self, expr):
        self._walk(expr.lhs)
        self._walk(expr.rhs)
        if expr.operator.type == lexer.TokenType.ADD:
            self.bc.write_op(bytecode.OpCode.ADD)
        elif expr.operator.type == lexer.TokenType.SUBTRACT:
            self.bc.write_op(bytecode.OpCode.SUBTRACT)
        elif expr.operator.type == lexer.TokenType.MULTIPLY:
            self.bc.write_op(bytecode.OpCode.MULTIPLY)
        elif expr.operator.type == lexer.TokenType.DIVIDE:
            self.bc.write_op(bytecode.OpCode.DIVIDE)
        else:
            raise RuntimeError("invalid token type for binop: {0}".format(expr.operator))

    def _walk_variable(self, expr):
        if expr.name not in self.variables:
            raise RuntimeError("reference to unrecognised variable {0}".format(expr.name))
        self.bc.write_op(bytecode.OpCode.GET_VAR, [self.variables[expr.name]])

    def _walk_function_call(self, expr):
        if expr.name not in self.functions:
            raise RuntimeError("reference to unrecognised function {0}.".format(expr.name))
        self.bc.write_op(bytecode.OpCode.CALL_FUNC, [self.functions[expr.name]])
