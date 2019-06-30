from enum import Enum


class LetStatement:
    def __init__(self, name, rhs):
        self.name = name
        self.rhs = rhs

    def __eq__(self, other):
        return self.name == other.name and self.rhs == other.rhs


class ExprStatement:
    def __init__(self, expr):
        self.expr = expr

    def __eq__(self, other):
        return self.expr == other.expr


class BinaryOp:
    def __init__(self, lhs, rhs, operator):
        self.lhs = lhs
        self.rhs = rhs
        self.operator = operator

    def __eq__(self, other):
        return self.lhs == other.lhs and self.rhs == other.rhs and self.operator == other.operator


class Function:
    def __init__(self, name, statements):
        self.name = name
        self.statements = statements

    def __eq__(self, other):
        return self.name == other.name and self.statements == other.statements


class Structure:
    def __init__(self, name, members):
        self.name = name
        self.members = members

    def __eq__(self, other):
        return self.name == other.name and self.members == other.members


class Type(Enum):
    INT = 1,
    STRING = 2,
    USER = 3


class Member:
    def __init__(self, name, m_type, default_value=None):
        self.name = name
        self.type = m_type
        self.default_value = default_value

    def __eq__(self, other):
        return (self.name == other.name and self.type == other.type and
                self.default_value == other.default_value)
