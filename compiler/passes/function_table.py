from .. import ast, ops


class FunctionTable(ast.ASTWalker):
    def __init__(self, bc):
        self.bc = bc

    def _walk_structure(self, expr):
        for mf in expr.member_functions:
            self._walk(mf)

    def _walk_function(self, expr):
        assert hasattr(expr, "function_id") and hasattr(expr, "offset")
        ops.FunctionJmp(expr.function_id, expr.offset).serialise(self.bc)
