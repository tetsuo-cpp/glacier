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
    def __init__(self, name, args, statements, return_type):
        self.name = name
        self.args = args
        self.statements = statements
        self.return_type = return_type

    def __eq__(self, other):
        return (self.name == other.name and self.args == other.args and
                self.statements == other.statements)


class Structure:
    def __init__(self, name, members, member_functions):
        self.name = name
        self.members = members
        self.member_functions = member_functions

    def __eq__(self, other):
        return (self.name == other.name and self.members == other.members and
                self.member_functions == other.member_functions)


class Type(Enum):
    INT = 1,
    STRING = 2,
    USER = 3


class Member:
    def __init__(self, name, m_type, m_type_name, default_value=None):
        self.name = name
        self.type = m_type
        self.type_name = m_type_name
        self.default_value = default_value

    def __eq__(self, other):
        return (self.name == other.name and self.type == other.type and
                self.type_name == other.type_name and self.default_value == other.default_value)


class ReturnStatement:
    def __init__(self, expr):
        self.expr = expr

    def __eq__(self, other):
        return self.expr == other.expr
