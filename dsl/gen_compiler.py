from dsl import ops
from dsl.source_writer import SourceWriter

HEADER = "# Generated by glacierdsl - DO NOT EDIT."
IMPORTS = """
from enum import Enum
"""


# Convert names_like_this to NamesLikeThis.
def _convert_snake_to_pascal(snake_str):
    convert_str = str()
    to_upper = True
    for c in snake_str:
        if to_upper:
            convert_str += c.upper()
            to_upper = False
        elif c == "_":
            to_upper = True
        else:
            convert_str += c
    return convert_str


def _gen_bc(writer, op, value):
    hex_string = hex(value)
    uc_name = op.name.upper()
    writer.write_line("{} = {}".format(uc_name, hex_string))


def _gen_op(writer, op):
    writer.write_line("class {}:".format(_convert_snake_to_pascal(op.name)))
    writer.indent()

    # Generate constructor.
    ctor_source = "def __init__(self"
    for arg in op.args:
        ctor_source += ", {} = None".format(arg.name)
    ctor_source += "):"
    writer.write_line(ctor_source)
    writer.indent()

    if op.args:
        writer.write_line("self._offset = None")
        for arg in op.args:
            writer.write_line("self.{0} = {0}".format(arg.name))
    else:
        writer.write_line("pass")
    writer.unindent()

    header_op = isinstance(op, ops.GlacierVMHeaderOp)

    # Generate serialise function.
    writer.write_line("def serialise(self, bc):")
    writer.indent()
    writer.write_line("args = list()")

    # Now supply arguments.
    for arg in op.args:
        if isinstance(arg, ops.GlacierVMArg):
            writer.write_line("args.append(self.{})".format(arg.name))
        else:
            assert isinstance(arg, ops.GlacierVMEnumeratedArg)
            writer.write_line("args.append(len(self.{}))".format(arg.name))
            if arg.size == ops.GlacierVMArgType.CHAR:
                writer.write_line("args.extend(bytes(self.{}, 'utf-8'))".format(arg.name))
            else:
                writer.write_line("args.extend(self.{})".format(arg.name))
    # Write the actual opcode.
    if op.args and not header_op:
        writer.write_line("if self._offset is not None:")
        writer.indent()
        writer.write_line("bc.edit_op(self._offset, OpCode.{}, args)".format(op.name.upper()))
        writer.unindent()
        writer.write_line("else:")
        writer.indent()
        writer.write_line("bc.write_op(OpCode.{}, args)".format(op.name.upper()))
        writer.unindent()
    else:
        if not header_op:
            writer.write_line("bc.write_op(OpCode.{}, args)".format(op.name.upper()))
        else:
            writer.write_line("bc.write_header(OpCode.{}, args)".format(op.name.upper()))
    writer.write_line("return self")
    writer.unindent()

    # Generate reserve and assign function if we have arguments.
    reserve_source = str()
    assign_source = str()
    if op.args and not header_op:
        writer.write_line("def reserve(self, bc):")
        writer.indent()
        writer.write_line("self._offset = bc.current_offset()")
        array_source = "args = ["
        for arg in op.args:
            if arg != op.args[0]:
                array_source += ", "
            array_source += "0xFF"
        array_source += "]"
        writer.write_line(array_source)
        writer.write_line("bc.write_op(OpCode.{}, args)".format(op.name.upper()))
        writer.write_line("return self")
        writer.unindent()

        assign_source = "def assign(self"
        for arg in op.args:
            assign_source += ", {}".format(arg.name)
        assign_source += "):"
        writer.write_line(assign_source)
        writer.indent()
        for arg in op.args:
            writer.write_line("self.{0} = {0}".format(arg.name))
        writer.write_line("return self")
        writer.unindent()


def gen_compiler(op_list):
    writer = SourceWriter()
    writer.write_line(HEADER)
    writer.write_line(IMPORTS)
    # Generate op enumeration.
    writer.write_line("class OpCode(Enum):")
    writer.indent()
    i = 0
    for op in op_list:
        _gen_bc(writer, op, i)
        i += 1
    writer.unindent()
    # Generate operation classes.
    for op in op_list:
        _gen_op(writer, op)
        writer.reset_indent()
    return writer.get_source()
