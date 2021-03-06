from enum import Enum


def list_to_string(l):
    s = "["
    for element in l:
        if len(s) != 1:
            s += ", "
        if isinstance(element, tuple):
            s += tuple_to_string(element)
        else:
            s += str(element)
    s += "]"
    return s


def tuple_to_string(p):
    s = "("
    for element in p:
        if len(s) != 1:
            s += ", "
        s += str(element)
    s += ")"
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


class IfStatement:
    def __init__(self, cond, then_statements, else_statements):
        self.cond = cond
        self.then_statements = then_statements
        self.else_statements = else_statements

    def __eq__(self, other):
        if not isinstance(other, IfStatement):
            return False
        return (
            self.cond == other.cond
            and self.then_statements == other.then_statements
            and self.else_statements == other.else_statements
        )

    def __str__(self):
        return "IfStatement(Cond={0}, ThenStatements={1}, ElseStatements={2})".format(
            self.cond, list_to_string(self.then_statements), list_to_string(self.else_statements)
        )


class WhileLoop:
    def __init__(self, cond, loop_body):
        self.cond = cond
        self.loop_body = loop_body

    def __eq__(self, other):
        if not isinstance(other, WhileLoop):
            return False
        return self.cond == other.cond and self.loop_body == other.loop_body

    def __str__(self):
        return "WhileLoop(Cond={0}, LoopBody={1})".format(self.cond, list_to_string(self.loop_body))


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
        return "BinaryOp(Lhs={0}, Rhs={1}, Operator={2})".format(self.lhs, self.rhs, self.operator)


class Function:
    def __init__(self, name, args, statements, return_type):
        self.name = name
        self.args = args
        self.statements = statements
        self.return_type = return_type

    def __eq__(self, other):
        if not isinstance(other, Function):
            return False
        return (
            self.name == other.name
            and self.args == other.args
            and self.statements == other.statements
        )

    def __str__(self):
        return "Function(Name={0}, Args={1}, Statements={2}, ReturnType={3})".format(
            self.name, list_to_string(self.args), list_to_string(self.statements), self.return_type
        )


class Structure:
    def __init__(self, name, members, member_functions):
        self.name = name
        self.members = members
        self.member_functions = member_functions

    def __eq__(self, other):
        if not isinstance(other, Structure):
            return False
        return (
            self.name == other.name
            and self.members == other.members
            and self.member_functions == other.member_functions
        )

    def __str__(self):
        return "Structure(Name={0}, Members={1}, MemberFunctions={2})".format(
            self.name, list_to_string(self.members), list_to_string(self.member_functions)
        )


class TypeKind(Enum):
    INT = 1
    STRING = 2
    VECTOR = 3
    MAP = 4
    VOID = 5
    USER = 6


class Type:
    def __init__(self, kind, identifier=None, container_type=None):
        self.kind = kind
        self.identifier = identifier
        # Only used for vectors and maps.
        self.container_type = container_type

    def __eq__(self, other):
        return (
            self.kind == other.kind
            and self.identifier == other.identifier
            and self.container_type == other.container_type
        )

    def __str__(self):
        return "(Kind={}, Identifier={}, ContainerType={})".format(
            self.kind, self.identifier, self.container_type
        )


class Member:
    def __init__(self, name, m_type, default_value=None):
        self.name = name
        self.type = m_type
        self.default_value = default_value

    def __eq__(self, other):
        if not isinstance(other, Member):
            return False
        return (
            self.name == other.name
            and self.type == other.type
            and self.default_value == other.default_value
        )

    def __str__(self):
        return "Member(Name={0}, Type={1}, Default={2})".format(
            self.name, self.type, self.default_value
        )


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


class Vector:
    def __init__(self, elements, container_type):
        self.elements = elements
        self.container_type = container_type

    def __eq__(self, other):
        if not isinstance(other, Vector):
            return False
        return self.elements == other.elements and self.container_type == other.container_type

    def __str__(self):
        return "Vector(Elements={0}, ContainerType={1})".format(
            list_to_string(self.elements), self.container_type
        )


class Map:
    def __init__(self, elements, container_types):
        self.elements = elements
        self.container_types = container_types

    def __eq__(self, other):
        if not isinstance(other, Map):
            return False
        return self.elements == other.elements and self.container_types == other.container_types

    def __str__(self):
        return "Map(Elements={0}, ContainerType={1})".format(
            list_to_string(self.elements), tuple_to_string(self.container_types)
        )


class VariableRef:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        if not isinstance(other, VariableRef):
            return False
        return self.name == other.name

    def __str__(self):
        return "VariableRef(Name={0})".format(self.name)


class FunctionCall:
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __eq__(self, other):
        if not isinstance(other, FunctionCall):
            return False
        return self.name == other.name and self.args == other.args

    def __str__(self):
        return "FunctionCall(Name={0}, Args={1})".format(self.name, list_to_string(self.args))


class Constructor:
    def __init__(self, struct_name, params):
        self.struct_name = struct_name
        self.params = params

    def __eq__(self, other):
        if not isinstance(other, Constructor):
            return False
        return self.struct_name == other.struct_name and self.params == other.params

    def __str__(self):
        return "Constructor(StructName={0}, Params={1})".format(
            self.struct_name, list_to_string(self.params)
        )


class MemberAccess:
    def __init__(self, expr, member_name):
        self.expr = expr
        self.member_name = member_name

    def __eq__(self, other):
        if not isinstance(other, MemberAccess):
            return False
        return self.expr == other.expr and self.member_name == other.member_name

    def __str__(self):
        return "MemberAccess(Expr={0}, MemberName={1})".format(self.expr, self.member_name)


class Index:
    def __init__(self, expr, index):
        self.expr = expr
        self.index = index

    def __eq__(self, other):
        if not isinstance(other, Index):
            return False
        return self.expr == other.expr and self.index == other.index

    def __str__(self):
        return "Index(Expr={0}, Index={1})".format(self.expr, self.index)


class ASTWalker:
    def walk_ast(self, top_level_exprs):
        for expr in top_level_exprs:
            self._walk(expr)

    def _walk(self, expr):
        if isinstance(expr, Structure):
            self._walk_structure(expr)
        elif isinstance(expr, LetStatement):
            self._walk_let_statement(expr)
        elif isinstance(expr, IfStatement):
            self._walk_if_statement(expr)
        elif isinstance(expr, WhileLoop):
            self._walk_while_loop(expr)
        elif isinstance(expr, ExprStatement):
            self._walk(expr.expr)
        elif isinstance(expr, BinaryOp):
            self._walk_binary_op(expr)
        elif isinstance(expr, Function):
            self._walk_function(expr)
        elif isinstance(expr, ReturnStatement):
            self._walk_return_statement(expr)
        elif isinstance(expr, Number):
            self._walk_number(expr)
        elif isinstance(expr, String):
            self._walk_string(expr)
        elif isinstance(expr, Vector):
            self._walk_vector(expr)
        elif isinstance(expr, Map):
            self._walk_map(expr)
        elif isinstance(expr, Index):
            self._walk_index(expr)
        elif isinstance(expr, VariableRef):
            self._walk_variable(expr)
        elif isinstance(expr, Constructor):
            self._walk_constructor(expr)
        elif isinstance(expr, FunctionCall):
            self._walk_function_call(expr)
        elif isinstance(expr, MemberAccess):
            self._walk_member_access(expr)
        else:
            raise RuntimeError("unexpected ast type: Ast=({0})".format(expr))

    def _walk_structure(self, expr):
        pass

    def _walk_let_statement(self, expr):
        pass

    def _walk_if_statement(self, expr):
        pass

    def _walk_while_loop(self, expr):
        pass

    def _walk_binary_op(self, expr):
        pass

    def _walk_function(self, expr):
        pass

    def _walk_return_statement(self, expr):
        pass

    def _walk_number(self, expr):
        pass

    def _walk_string(self, expr):
        pass

    def _walk_vector(self, expr):
        pass

    def _walk_map(self, expr):
        pass

    def _walk_index(self, expr):
        pass

    def _walk_variable(self, expr):
        pass

    def _walk_constructor(self, expr):
        pass

    def _walk_function_call(self, expr):
        pass

    def _walk_member_access(self, expr):
        pass
