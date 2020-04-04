from .. import ast, bytecode, lexer, ops


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
    def __init__(self, bc, structs, intrinsics):
        self.bc = bc
        self.structs = structs
        self.intrinsics = intrinsics
        self.functions = dict()
        self.function_id = 1
        self.variables = VariableStore()
        self.seen_main = False

    def _walk_structure(self, expr):
        for mf in expr.member_functions:
            self._walk(mf)

    def _walk_function(self, expr):
        expr.function_id = self._allocate_function_id(expr.name)
        self.functions[expr.name] = expr
        expr.offset = self.bc.current_offset()
        for a in expr.args:
            self.variables.register_variable(a[0])
        ops.FunctionDef(expr.function_id, len(expr.args)).serialise(self.bc)
        for s in expr.statements:
            self._walk(s)
        self.variables.clear()
        # For functions returning void, there's an implicit return at the end of the function.
        assert expr.return_type is not None
        if expr.return_type.kind:
            ops.Return().serialise(self.bc)

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
            ops.Return().serialise(self.bc)
        else:
            self._walk(expr.expr)
            ops.ReturnVal().serialise(self.bc)

    def _walk_number(self, expr):
        ops.Int(expr.value).serialise(self.bc)

    def _walk_string(self, expr):
        args = list()
        args.append(len(expr.value))
        args.extend(bytes(expr.value, "utf-8"))
        self.bc.write_op(bytecode.OpCode.STRING, args)

    def _walk_vector(self, expr):
        for e in reversed(expr.elements):
            self._walk(e)
        ops.Vec(len(expr.elements)).serialise(self.bc)

    def _walk_map(self, expr):
        for (key, value) in expr.elements:
            self._walk(key)
            self._walk(value)
        ops.Map(len(expr.elements)).serialise(self.bc)

    def _walk_index(self, expr):
        # Walk the expr.
        self._walk(expr.expr)
        # Now push the index to the stack.
        self._walk(expr.index)
        if expr.expr.ret_type.kind == ast.TypeKind.VECTOR:
            ops.VecAccess().serialise(self.bc)
        else:
            assert expr.expr.ret_type.kind == ast.TypeKind.MAP
            ops.MapAccess().serialise(self.bc)

    def _walk_let_statement(self, expr):
        self._walk(expr.rhs)
        variable_id = self.variables.register_variable(expr.name)
        ops.SetVar(variable_id).serialise(self.bc)

    def _walk_if_statement(self, expr):
        self._walk(expr.cond)

        # Jump to "else" branch if the cond was false.
        skip_then = ops.JumpIfFalse().reserve(self.bc)

        for statement in expr.then_statements:
            self._walk(statement)

        # Skip the else branch if we're executing "then".
        skip_else = ops.Jump().reserve(self.bc)

        # Go back and edit the "else" jump.
        after_then = self.bc.current_offset()
        skip_then.assign(after_then).serialise(self.bc)

        for statement in expr.else_statements:
            self._walk(statement)

        after_else = self.bc.current_offset()
        skip_else.assign(after_else).serialise(self.bc)

    def _walk_while_loop(self, expr):
        # Every loop iteration is going to jump back up here.
        before_loop = self.bc.current_offset()

        # Eval the cond.
        self._walk(expr.cond)

        # Jump out of the loop if the cond is false.
        # Come back and edit this when we know what bytecode offset the loop ends at.
        skip_loop = ops.JumpIfFalse().reserve(self.bc)

        for statement in expr.loop_body:
            self._walk(statement)

        # Jump back to the beginning of the loop and eval the cond again.
        ops.Jump(before_loop).serialise(self.bc)

        after_loop_body = self.bc.current_offset()
        skip_loop.assign(after_loop_body).serialise(self.bc)

    def _walk_binary_op(self, expr):
        # If we're assigning to a variable, don't evaluate it.
        if expr.operator.type != lexer.TokenType.ASSIGN:
            self._walk(expr.lhs)
        self._walk(expr.rhs)
        if expr.operator.type == lexer.TokenType.ADD:
            ops.Add().serialise(self.bc)
        elif expr.operator.type == lexer.TokenType.SUBTRACT:
            ops.Subtract().serialise(self.bc)
        elif expr.operator.type == lexer.TokenType.MULTIPLY:
            ops.Multiply().serialise(self.bc)
        elif expr.operator.type == lexer.TokenType.DIVIDE:
            ops.Divide().serialise(self.bc)
        elif expr.operator.type == lexer.TokenType.EQUALS:
            ops.Eq().serialise(self.bc)
        elif expr.operator.type == lexer.TokenType.LESS_THAN:
            ops.Lt().serialise(self.bc)
        elif expr.operator.type == lexer.TokenType.ASSIGN:
            self._walk_assignment(expr)
        else:
            raise RuntimeError("invalid token type for binop: {0}".format(expr.operator))

    def _walk_assignment(self, expr):
        assert expr.operator.type == lexer.TokenType.ASSIGN
        if isinstance(expr.lhs, ast.VariableRef):
            ops.SetVar(self.variables.get_variable(expr.lhs.name)).serialise(self.bc)
        elif isinstance(expr.lhs, ast.MemberAccess):
            self._walk(expr.lhs.expr)
            # We've already done type deduction so we can do this properly later.
            for _, s in self.structs.items():
                i = 0
                for m in s.members:
                    if m.name == expr.lhs.member_name:
                        ops.SetStructMember(i).serialise(self.bc)
                        return
                    i += 1
            raise RuntimeError("couldn't find the right struct")
        else:
            raise RuntimeError(
                "lhs of an assignment must be either a variable ref or a struct member access: {}".format(
                    expr
                )
            )

    def _walk_variable(self, expr):
        ops.GetVar(self.variables.get_variable(expr.name)).serialise(self.bc)

    def _walk_constructor(self, expr):
        # Get the struct id.
        if expr.struct_name not in self.structs:
            raise RuntimeError("unrecognised struct name {0}".format(expr.struct_name))
        struct_def = self.structs[expr.struct_name]
        # Codegen each argument to the ctor.
        for i in range(0, len(struct_def.members)):
            if i < len(expr.params):
                self._walk(expr.params[i])
            else:
                default_value = struct_def.members[i].default_value
                assert default_value is not None
                self._walk(default_value)
        ops.Struct(struct_def.type_id).serialise(self.bc)

    def _walk_function_call(self, expr):
        if self.intrinsics.is_intrinsic(expr.name):
            self.intrinsics.codegen(expr, self)
            return
        if expr.name not in self.functions:
            raise RuntimeError("reference to unrecognised function {0}.".format(expr.name))
        for arg in expr.args:
            self._walk(arg)
        ops.CallFunc(self.functions[expr.name].function_id).serialise(self.bc)

    def _walk_member_access(self, expr):
        # Codegen to push the struct to the stack.
        self._walk(expr.expr)
        assert isinstance(expr.expr, ast.VariableRef)
        # Just a temporary hack. I want to check that this works.
        for _, s in self.structs.items():
            i = 0
            for m in s.members:
                if m.name == expr.member_name:
                    ops.GetStructMember(i).serialise(self.bc)
                    return
                i += 1
        raise RuntimeError("couldn't find the right struct")
