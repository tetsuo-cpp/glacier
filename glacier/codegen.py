import glacier.ast as ast


class CodeGenerator(ast.AstWalker):
    def _walk_structure(self, structure):
        print("calling _walk_structure")

    def _walk_let_statement(self, let):
        print("calling _walk_let statement")

    def _walk_binary_op(self, binop):
        print("calling _walk_binary op")

    def _walk_function(self, function):
        print("calling _walk_function")
