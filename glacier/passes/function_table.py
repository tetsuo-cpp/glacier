from .. import ast, bytecode


class FunctionTable(ast.ASTWalker):
    def __init__(self, bc):
        self.bc = bc

    def _walk_function(self, expr):
        assert hasattr(expr, "function_id") and hasattr(expr, "offset")
        print(
            "Writing function table entry for id {0} and offset {1}".format(
                expr.function_id, expr.offset
            )
        )
        self.bc.write_header(bytecode.OpCode.FUNCTION_JMP, [expr.function_id, expr.offset])
