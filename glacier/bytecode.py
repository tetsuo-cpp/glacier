import enum


class OpCode(enum.Enum):
    """
    A structure definition.
    - The STRUCT_DEF opcode (1 byte).
    - The type id of the struct (1 byte).
    - The number of members (1 byte).
    - The type id of each member (num members bytes).
    """

    STRUCT_DEF = 0x00
    """
    A function definition.
    - The FUNCTION_DEF opcode (1 byte).
    - The function id (1 byte).
    - The number of args (1 byte).
    - Instructions.
    """
    FUNCTION_DEF = 0x01
    """
    Set a variable binding. Binds the top of the stack to the given variable id.
    - The SET_VAR opcode (1 byte).
    - The variable id (1 byte).
    """
    SET_VAR = 0x02
    """
    Get a variable binding. Retrieves a binding previously set with the SET_VAR op and places it at
    at top of the stack.
    - The GET_VAR opcode (1 byte).
    - The variable id (1 byte).
    """
    GET_VAR = 0x03
    """
    Call a function.
    - The CALL_FUNC opcode (1 byte).
    - The function id (1 byte).
    """
    CALL_FUNC = 0x04
    """
    Returns out of the current function.
    - The RETURN opcode (1 byte).
    """
    RETURN = 0x05
    """
    Returns out of the current function and preserves the topmost element of the stack.
    - The RETURN_VAL opcode (1 byte).
    """
    RETURN_VAL = 0x06
    """
    Pops and adds the top two elements of the stack and pushes the result.
    - The ADD opcode (1 byte).
    """
    ADD = 0x07
    """
    Pushes an integer object onto the stack.
    - The INT opcode (1 byte).
    - The integer value (8 bytes).
    """
    INT = 0x08
    """
    Pushes a string object onto the stack.
    - The STRING opcode (1 byte).
    - The string length. (1 byte).
    - The string data (length bytes).
    """
    STRING = 0x09
    """
    Pops and subtracts the top two elements of the stack and pushes the result.
    - The SUBTRACT opcode (1 byte).
    """
    SUBTRACT = 0x0A
    """
    Pops and multiplies the top two elements of the stack and pushes the result.
    - The MULTIPLY opcode (1 byte).
    """
    MULTIPLY = 0x0B
    """
    Pops and divides the top two elements of the stack and pushes the result.
    - The DIVIDE opcode (1 byte).
    """
    DIVIDE = 0x0C
    """
    An entry in the function table.
    - The FUNCTION_JMP opcode (1 byte).
    - The function id (1 byte).
    - The offset of the corresponding FUNCTION_DEF in bytes (1 byte).
    """
    FUNCTION_JMP = 0x0D
    """
    The end of the header portion of the bytecode.
    - The HEADER_END opcode (1 byte).
    """
    HEADER_END = 0x0F
    """
    Print an integer at the top of the stack.
    - The PRINT opcode (1 byte).
    """
    PRINT = 0x10
    """
    Compare equality of two integers at the top of the stack and place the result on the top of the
    stack (1 for true, 0 for false).
    - The EQ opcode (1 byte).
    """
    EQ = 0x11
    """
    Jump to a given offset if the top of the stack is 1.
    - The JUMP_IF_TRUE opcode (1 byte).
    - The offset to jump to in bytes (1 byte).
    """
    JUMP_IF_TRUE = 0x12
    """
    Jump to a given offset if the top of the stack is 0.
    - The JUMP_IF_FALSE opcode (1 byte).
    - The offset to jump to in bytes (1 byte).
    """
    JUMP_IF_FALSE = 0x13
    """
    Jump to a given offset.
    - The JUMP opcode (1 byte).
    - The offset to jump to in bytes (1 byte).
    """
    JUMP = 0x14
    """
    Construct an object with a given struct id.
    - The STRUCT opcode (1 byte).
    - The struct id (1 byte).
    """
    STRUCT = 0x15
    """
    Get a struct member.
    - The GET_STRUCT_MEMBER opcode (1 byte).
    - The member index (1 byte).
    """
    GET_STRUCT_MEMBER = 0x16
    """
    Set a struct member.
    - The SET_STRUCT_MEMBER opcode (1 byte).
    - The member index (1 byte).
    """
    SET_STRUCT_MEMBER = 0x17


class ByteCode:
    def __init__(self):
        self.header = bytearray()
        self.buf = bytearray()

    def write_header(self, op, args=list()):
        self.header.append(op.value)
        self.header.extend(args)

    def write_op(self, op, args=list()):
        self.buf.append(op.value)
        self.buf.extend(args)

    def edit_op(self, offset, op, args=list()):
        self.buf[offset] = op.value
        for i in range(1, len(args) + 1):
            self.buf[offset + i] = args[i - 1]

    def current_offset(self):
        return len(self.buf)

    def construct(self):
        return self.header + bytearray([OpCode.HEADER_END.value]) + self.buf
