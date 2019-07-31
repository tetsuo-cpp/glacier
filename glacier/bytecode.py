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

class ByteCode:
    def __init__(self):
        self.buf = bytearray()

    def write_op(self, op, args=list()):
        self.buf.append(op.value)
        self.buf.extend(args)
