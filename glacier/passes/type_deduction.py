from .. import ast, bytecode, lexer

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
        assert hasattr(expr.rhs, "ret_type")
        self.variable_types[expr.name] = expr.rhs.ret_type
        expr.ret_type = expr.rhs.ret_type

    def _walk_binary_op(self, expr):
        expr.ret_type = ast.Type(ast.TypeKind.INT)

    def _walk_number(self, expr):
        expr.ret_type = ast.Type(ast.TypeKind.INT)

    def _walk_string(self, expr):
        expr.ret_type = ast.Type(ast.TypeKind.STRING)

    def _walk_variable(self, expr):
        assert expr.name in self.variable_types
        expr.ret_type = self.variable_types[expr.name]

    def _walk_constructor(self, expr):
        expr.ret_type = ast.Type(ast.Type.USER, expr.struct_name)

    def _walk_function_call(self, expr):
        # Deduce types of each argument.
        for arg in expr.args:
            self._walk(arg)

        # Now compare against the function parameter types.
        assert expr.name in self.functions
        called_func = self.functions[expr.name]
        for arg, param in zip(expr.args, called_func.args):
            assert param[1] == arg.ret_type

    def _walk_function(self, expr):
        assert expr.name not in self.functions
        self.functions[expr.name] = expr
        for s in expr.statements:
            self._walk(s)

    def _walk_member_access(self, expr):
        # Deduce type of expr.
        self._walk(expr.expr)
        assert hasattr(expr.expr, "ret_type")
        assert ret_type.identifier in self.structs

        struct_def = self.structs[ret_type.identifier]
        for member in struct_def.members:
            if member.name == expr.member_name:
                expr.ret_type = member[1]
                return
        assert False
