from enum import Enum


def list_to_string(l):
    s = "["
    for element in l:
        if len(s) != 1:
            s += ", "
        s += str(element)
    s += "]"
    return s


class LetStatement:
    def __init__(self, name, rhs):
        self.name = name
        self.rhs = rhs

    def __eq__(self, other):
        if not isinstance(other, LetStatement):
            return False
        return self.name == other.name and self.rhs == other.rhs

    def __str__(self):
        return "LetStatement(Name={0}, Rhs={1})".format(self.name, self.rhs)


class ExprStatement:
    def __init__(self, expr):
        self.expr = expr

    def __eq__(self, other):
        if not isinstance(other, ExprStatement):
            return False
        return self.expr == other.expr

    def __str__(self):
        return "ExprStatement(Expr={0})".format(self.expr)


class BinaryOp:
    def __init__(self, lhs, rhs, operator):
        self.lhs = lhs
        self.rhs = rhs
        self.operator = operator

    def __eq__(self, other):
        if not isinstance(other, BinaryOp):
            return False
        return self.lhs == other.lhs and self.rhs == other.rhs and self.operator == other.operator

    def __str__(self):
        return "BinaryOp(Lhs={0}, Rhs={1}, Operator={2})".format(
            self.lhs, self.rhs, self.operator)


class Function:
    def __init__(self, name, args, statements, return_type):
        self.name = name
        self.args = args
        self.statements = statements
        self.return_type = return_type

    def __eq__(self, other):
        if not isinstance(other, Function):
            return False
        return (self.name == other.name and self.args == other.args and
                self.statements == other.statements)

    def __str__(self):
        return "Function(Name={0}, Args={1}, Statements={2}, ReturnType={3})".format(
            self.name, list_to_string(self.args), list_to_string(self.statements), self.return_type)


class Structure:
    def __init__(self, name, members, member_functions):
        self.name = name
        self.members = members
        self.member_functions = member_functions

    def __eq__(self, other):
        if not isinstance(other, Structure):
            return False
        return (self.name == other.name and self.members == other.members and
                self.member_functions == other.member_functions)

    def __str__(self):
        return "Structure(Name={0}, Members={1}, MemberFunctions={2})".format(
            self.name, list_to_string(self.members), list_to_string(self.member_functions))


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
        if not isinstance(other, Member):
            return False
        return (self.name == other.name and self.type == other.type and
                self.type_name == other.type_name and self.default_value == other.default_value)

    def __str__(self):
        return "Member(Name={0}, Type={1}, TypeName={2}, Default={3})".format(
            self.name, self.type, self.type_name, self.default_value)


class ReturnStatement:
    def __init__(self, expr):
        self.expr = expr

    def __eq__(self, other):
        if not isinstance(other, ReturnStatement):
            return False
        return self.expr == other.expr

    def __str__(self):
        return "ReturnStatement(Expr={0})".format(self.expr)


class Number:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, Number):
            return False
        return self.value == other.value

    def __str__(self):
        return "Number(Value={0})".format(self.value)


class String:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, String):
            return False
        return self.value == other.value

    def __str__(self):
        return "String(Value={0})".format(self.value)
