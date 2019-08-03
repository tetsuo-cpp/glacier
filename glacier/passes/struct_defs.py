from .. import ast, bytecode


def _get_type_id(expr):
    if expr.type == ast.Type.INT:
        return 0
    elif expr.type == ast.Type.STRING:
        return 1
    else:
        if not hasattr(expr, "type_id"):
            raise RuntimeError("tried to get type_id on invalid type: {0}".format(expr))
        return expr.type_id


class StructureDefinitions(ast.ASTWalker):
    def __init__(self, bc):
        self.structs = dict()
        self.bc = bc

        # Integer and string occupy 0 and 1.
        self.current_type_id = 2

    def _walk_structure(self, expr):
        expr.type_id = self.current_type_id
        self.current_type_id += 1
        self.structs[expr.name] = expr

        # First arg is the number of members.
        args = [len(expr.members)]

        # The remaining args are the type ids of the members.
        for m in expr.members:
            args.append(_get_type_id(m))

        self.bc.write_header(bytecode.OpCode.STRUCT_DEF, args)
