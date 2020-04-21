from compiler import ops


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
        return self.header + bytearray([ops.OpCode.HEADER_END.value]) + self.buf
