from .. import ast, bytecode, lexer


class Frame:
    def __init__(self, last_id):
        self.last_id = last_id
        self.variables = dict()


class FrameStack:
    def __init__(self):
        self.stack = list()
        self.variable_id = 0
        self.push_frame()

    def push_frame(self):
        self.stack.append(Frame(self.variable_id))
        self.variable_id = 0

    def pop_frame(self):
        self.variable_id = self.stack[-1].last_id
        self.stack.pop()

    def register_variable(self, name):
        top = self.stack[-1]
        if name in top.variables:
            raise RuntimeError("variable {0} declared twice".format(name))
        new_id = self.variable_id
        top.variables[name] = self.variable_id
        self.variable_id += 1
        return new_id

    def get_variable(self, name):
        top = self.stack[-1]
        if name not in top.variables:
            raise RuntimeError("reference to unrecognised variable {0}".format(name))
        return top.variables[name]


class CodeGenerator(ast.ASTWalker):
    def __init__(self, bc):
        self.bc = bc
        self.functions = dict()
        self.function_id = 1
        self.variables = FrameStack()
        self.seen_main = False

    def _walk_function(self, expr):
        if expr.name == "main" and not self.seen_main:
            # Function id 0 is reserved for main.
            expr.function_id = 0
            self.main = True
        else:
            expr.function_id = self.function_id
        self.functions[expr.name] = expr
        expr.offset = self.bc.current_offset()
        args = list()
        args.append(expr.function_id)
        args.append(len(expr.args))
        for a in expr.args:
            self.variables.register_variable(a[0])
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
        args.extend(bytes(expr.value, "utf-8"))
        self.bc.write_op(bytecode.OpCode.STRING, args)

    def _walk_let_statement(self, expr):
        self._walk(expr.rhs)
        variable_id = self.variables.register_variable(expr.name)
        self.bc.write_op(bytecode.OpCode.SET_VAR, [variable_id])

    def _walk_if_statement(self, expr):
        self._walk(expr.cond)
        offset = self.bc.current_offset()
        self.bc.write_op(bytecode.OpCode.JUMP_IF_FALSE, [0xFF])
        for statement in expr.statements:
            self._walk(statement)
        after_then = self.bc.current_offset()
        self.bc.edit_op(offset, bytecode.OpCode.JUMP_IF_FALSE, [after_then])

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
        elif expr.operator.type == lexer.TokenType.EQUALS:
            self.bc.write_op(bytecode.OpCode.EQ)
        else:
            raise RuntimeError("invalid token type for binop: {0}".format(expr.operator))

    def _walk_variable(self, expr):
        self.bc.write_op(bytecode.OpCode.GET_VAR, [self.variables.get_variable(expr.name)])

    def _walk_function_call(self, expr):
        if expr.name not in self.functions and expr.name != "print":
            raise RuntimeError("reference to unrecognised function {0}.".format(expr.name))
        for arg in expr.args:
            self._walk(arg)
        # Probably go check some builtins array. For now let's just add a conditional for print.
        if expr.name == "print":
            self.bc.write_op(bytecode.OpCode.PRINT)
            return
        self.bc.write_op(bytecode.OpCode.CALL_FUNC, [self.functions[expr.name].function_id])
