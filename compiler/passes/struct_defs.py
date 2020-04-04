from .. import ast, ops


def _get_type_id(expr):
    if expr.type.kind == ast.TypeKind.INT:
        return 0
    elif expr.type.kind == ast.TypeKind.STRING:
        return 1
    else:
        if not hasattr(expr, "type_id"):
            raise RuntimeError("tried to get type_id on invalid type: {0}".format(expr))
        return expr.type_id


class StructureDefinitions(ast.ASTWalker):
    def __init__(self, bc, structs):
        self.structs = structs
        self.bc = bc

        # Integer and string occupy 0 and 1.
        self.current_type_id = 2

    def _walk_structure(self, expr):
        expr.type_id = self.current_type_id
        self.current_type_id += 1
        self.structs[expr.name] = expr

        # The remaining args are the type ids of the members.
        types = list()
        for m in expr.members:
            types.append(_get_type_id(m))

        ops.StructDef(expr.type_id, types).serialise(self.bc)
