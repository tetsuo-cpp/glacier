class LetStatement:
    def __init__(self, name, rhs):
        self.name = name
        self.rhs = rhs


class ExprStatement:
    def __init__(self, expr):
        self.expr = expr


class BinaryOp:
    def __init__(self, lhs, rhs, operator):
        self.lhs = lhs
        self.rhs = rhs
        self.operator = operator


class Function:
    def __init__(self, name, statements):
        self.name = name
        self.statements = statements
