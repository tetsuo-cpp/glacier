from .. import ast, bytecode, lexer


class TypeError(Exception):
    pass


# Just fail with assertions for the time being.
# In the future, we should begin raising type errors.
class TypeDeduction(ast.ASTWalker):
    def __init__(self, bc, structs):
        self.bc = bc
        self.structs = structs
        self.variable_types = dict()
        self.functions = dict()

    def _walk_let_statement(self, expr):
        self._walk(expr.rhs)
        if not hasattr(expr.rhs, "ret_type"):
            raise TypeError("rhs of let statement returns void")
        self.variable_types[expr.name] = expr.rhs.ret_type
        expr.ret_type = expr.rhs.ret_type

    def _walk_binary_op(self, expr):
        expr.ret_type = ast.Type(ast.TypeKind.INT)

    def _walk_number(self, expr):
        expr.ret_type = ast.Type(ast.TypeKind.INT)

    def _walk_string(self, expr):
        expr.ret_type = ast.Type(ast.TypeKind.STRING)

    def _walk_vector(self, expr):
        expr.ret_type = ast.Type(ast.TypeKind.VECTOR, None, expr.container_type)
        for e in expr.elements:
            self._walk(e)
            if e.ret_type != expr.container_type:
                raise TypeError(
                    "found element of type {} in array with container type {}".format(
                        e.ret_type.kind, expr.container_type.kind
                    )
                )

    def _walk_map(self, expr):
        expr.ret_type = ast.Type(ast.TypeKind.MAP, None, expr.container_types)
        for (key, value) in expr.elements:
            self._walk(key)
            self._walk(value)
            if key.ret_type != expr.container_types[0]:
                raise TypeError(
                    "found key of type {} in map with key type {}".format(
                        key.ret_type.kind, expr.container_types[0].kind
                    )
                )
            if value.ret_type != expr.container_types[1]:
                raise TypeError(
                    "found value of type {} in map with value type {}".format(
                        value.ret_type.kind, expr.container_types[1].kind
                    )
                )

    def _walk_index(self, expr):
        self._walk(expr.expr)
        self._walk(expr.index)
        # If it's a map, then choose the value type.
        if isinstance(expr.expr.ret_type.container_type, tuple):
            assert len(expr.expr.ret_type.container_type) == 2
            expr.ret_type = expr.expr.ret_type.container_type[1]
        else:
            expr.ret_type = expr.expr.ret_type.container_type

    def _walk_variable(self, expr):
        if expr.name not in self.variable_types:
            raise TypeError("reference to unrecognised variable {}".format(expr.name))
        expr.ret_type = self.variable_types[expr.name]

    def _walk_constructor(self, expr):
        expr.ret_type = ast.Type(ast.TypeKind.USER, expr.struct_name)

    def _walk_function_call(self, expr):
        # Deduce types of each argument.
        for arg in expr.args:
            self._walk(arg)
        # I really need to do this properly one day...
        if expr.name == "print":
            return

        # Now compare against the function parameter types.
        assert expr.name in self.functions
        called_func = self.functions[expr.name]
        i = 0
        for arg, param in zip(expr.args, called_func.args):
            if param[1] != arg.ret_type:
                raise TypeError(
                    "called function {} with arg {} of type {} when we expected {}".format(
                        expr.name, i, arg.ret_type.kind, param[1].kind
                    )
                )
            i += 1
        expr.ret_type = called_func.return_type

    def _walk_structure(self, expr):
        for mf in expr.member_functions:
            self._walk(mf)

    def _walk_function(self, expr):
        if expr.name in self.functions:
            raise TypeError("redefinition of function {}".format(expr.name))
        self.functions[expr.name] = expr
        for s in expr.statements:
            self._walk(s)

    def _walk_member_access(self, expr):
        # Deduce type of expr.
        self._walk(expr.expr)
        assert hasattr(expr.expr, "ret_type")
        assert expr.expr.ret_type.identifier in self.structs

        struct_def = self.structs[expr.expr.ret_type.identifier]
        for member in struct_def.members:
            if member.name == expr.member_name:
                expr.ret_type = member.type
                return
        assert False
