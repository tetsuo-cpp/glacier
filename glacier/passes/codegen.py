from .. import ast, bytecode, lexer


class VariableStore:
    def __init__(self):
        self.clear()

    def clear(self):
        self.bindings = dict()
        self.current_id = 0

    def register_variable(self, name):
        if name in self.bindings:
            raise RuntimeError("variable {0} declared twice".format(name))
        new_id = self.current_id
        self.bindings[name] = new_id
        self.current_id += 1
        return new_id

    def get_variable(self, name):
        if name not in self.bindings:
            raise RuntimeError("reference to unrecognised variable {0}".format(name))
        return self.bindings[name]


class CodeGenerator(ast.ASTWalker):
    def __init__(self, bc, structs):
        self.bc = bc
        self.structs = structs
        self.functions = dict()
        self.function_id = 1
        self.variables = VariableStore()
        self.seen_main = False

    def _walk_function(self, expr):
        expr.function_id = self._allocate_function_id(expr.name)
        self.functions[expr.name] = expr
        expr.offset = self.bc.current_offset()
        args = list()
        args.append(expr.function_id)
        args.append(len(expr.args))
        for a in expr.args:
            self.variables.register_variable(a[0])
        self.bc.write_op(bytecode.OpCode.FUNCTION_DEF, args)
        for s in expr.statements:
            self._walk(s)
        self.variables.clear()

    def _allocate_function_id(self, name):
        if name in self.functions:
            raise RuntimeError("duplicate function def {}".format(name))
        if name == "main":
            return 0
        else:
            new_id = self.function_id
            self.function_id += 1
            return new_id

    def _walk_return_statement(self, expr):
        if expr.expr is None:
            self.bc.write_op(bytecode.OpCode.RETURN)
        else:
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

        # Jump to "else" branch if the cond was false.
        skip_then_offset = self.bc.current_offset()
        self.bc.write_op(bytecode.OpCode.JUMP_IF_FALSE, [0xFF])

        for statement in expr.then_statements:
            self._walk(statement)

        # Skip the else branch if we're executing "then".
        skip_else_offset = self.bc.current_offset()
        self.bc.write_op(bytecode.OpCode.JUMP, [0xFF])

        # Go back and edit the "else" jump.
        after_then = self.bc.current_offset()
        self.bc.edit_op(skip_then_offset, bytecode.OpCode.JUMP_IF_FALSE, [after_then])

        for statement in expr.else_statements:
            self._walk(statement)

        after_else = self.bc.current_offset()
        self.bc.edit_op(skip_else_offset, bytecode.OpCode.JUMP, [after_else])

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

    def _walk_constructor(self, expr):
        # Get the struct id.
        if expr.struct_name not in self.structs:
            raise RuntimeError("unrecognised struct name {0}".format(expr.struct_name))
        struct_def = self.structs[expr.struct_name]
        # Codegen each argument to the ctor.
        for p in expr.params:
            self._walk(p)
        self.bc.write_op(bytecode.OpCode.STRUCT, [struct_def.type_id])

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

    def _walk_member_access(self, expr):
        # Codegen to push the struct to the stack.
        self._walk(expr.expr)
        assert isinstance(expr.expr, ast.VariableRef)
        # Just a temporary hack. I want to check that this works.
        for _, s in self.structs.items():
            i = 0
            for m in s.members:
                if m.name == expr.member_name:
                    self.bc.write_op(bytecode.OpCode.GET_STRUCT_MEMBER, [i])
                    return
                i += 1
        raise RuntimeError("couldn't find the right struct")
