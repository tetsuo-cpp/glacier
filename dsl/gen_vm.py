def _gen_op(op, value):
    hex_string = hex(value)
    uc_name = op.name.upper()
    return "#define GLC_BYTECODE_{} {}\n".format(uc_name, hex_string)


# Generate header containing #define's for each operation.
def gen_vm(ops):
    source = str()
    i = 0
    for op in ops:
        source += _gen_op(op, i)
        i += 1
    return source
