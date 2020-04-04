import enum


# FIXME: Use this in the DSL generation.
class GlacierVMArgType(enum.Enum):
    CHAR = enum.auto()
    BIT_8 = enum.auto()
    BIT_16 = enum.auto()
    BIT_32 = enum.auto()
    BIT_64 = enum.auto()


class GlacierVMOp:
    def __init__(self, name, args):
        self.name = name
        self.args = args


class GlacierVMHeaderOp:
    def __init__(self, name, args):
        self.name = name
        self.args = args


class GlacierVMArg:
    def __init__(self, name, size):
        self.name = name
        self.size = size


class GlacierVMEnumeratedArg:
    def __init__(self, name, size):
        self.name = name
        self.size = size
