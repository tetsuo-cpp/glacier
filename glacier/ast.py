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


class Structure:
    def __init__(self, name, members):
        self.name = name
        self.members = members


class Member:
    def __init__(self, name, m_type, default_value=None):
        self.name = name
        self.type = m_type
        self.default_value = default_value
