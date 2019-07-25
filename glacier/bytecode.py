import enum


class OpCode(enum.Enum):
    """
    STRUCT_DEF (1 byte)
    TYPE_ID (1 byte)
    NUM_MEMBERS (1 byte)
    MEMBER_0 (1 byte)
    MEMBER_1 (1 byte)
    ...
    """
    STRUCT_DEF = 0x0


class ByteCode:
    def __init__(self):
        self.buf = bytearray()

    def write_op(self, op, args):
        self.buf.append(op.value)
        self.buf.extend(args)
