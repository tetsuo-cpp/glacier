class MalformedByteCodeError(Exception):
    pass


class ByteCodeReader:
    def __init__(self, bc):
        self.bc = bc
        self.index = 0

    def read_op(self):
        if self.index >= len(self.bc):
            return None
        op = self.bc[self.index]
        self.index += 1
        return op

    def expect_op(self):
        op = self.read_op()
        if op is None:
            raise MalformedByteCodeError("unexpected end of bytecode")
        return op
