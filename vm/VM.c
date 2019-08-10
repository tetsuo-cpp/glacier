#include "VM.h"

#include "Util.h"

#include <stdio.h>

static int glacierVMStructDef(GlacierVM *vm);
static int glacierVMFunctionDef(GlacierVM *vm);
static int glacierVMInt(GlacierVM *vm);
static int glacierVMAdd(GlacierVM *vm);
static int glacierVMSubtract(GlacierVM *vm);
static int glacierVMMultiply(GlacierVM *vm);
static int glacierVMDivide(GlacierVM *vm);
static int glacierVMReturnVal(GlacierVM *vm);
static int glacierVMHeader(GlacierVM *vm);
static int glacierVMFunctionJmp(GlacierVM *vm);
static int glacierVMSetVar(GlacierVM *vm);
static int glacierVMGetVar(GlacierVM *vm);

void glacierVMInit(GlacierVM *vm, GlacierByteCode *bc, GlacierStack *stack,
                   GlacierFunctionTable *ft, GlacierCallStack *cs) {
  vm->bc = bc;
  vm->stack = stack;
  vm->ft = ft;
  vm->cs = cs;
}

int glacierVMRun(GlacierVM *vm) {
  // Read structs and function offsets.
  GLC_RET(glacierVMHeader(vm));

  // All offsets are relative to the end of the header. Trim everything before
  // where we are now.
  GLC_RET(glacierByteCodeTrim(vm->bc));

  // Jump to main.
  int mainOffset;
  GLC_RET(glacierFunctionTableGet(vm->ft, 0, &mainOffset));
  GLC_RET(glacierByteCodeJump(vm->bc, mainOffset));

  // Execute main.
  GLC_RET(glacierVMFunctionDef(vm));

  // If we didn't get a non-zero then we terminated ok.
  return GLC_OK;
}

static int glacierVMStructDef(GlacierVM *vm) {
  uint8_t numMembers;
  GLC_RET(glacierByteCodeRead8(vm->bc, &numMembers));
  fprintf(stderr, "Parsing struct def with %d members.\n", numMembers);
  for (int i = 0; i < numMembers; ++i) {
    uint8_t typeId;
    GLC_RET(glacierByteCodeRead8(vm->bc, &typeId));
    switch (typeId) {
    case GLACIER_TYPEID_INT:
      fprintf(stderr, "Parsed int member.\n");
      break;
    case GLACIER_TYPEID_STRING:
      fprintf(stderr, "Parsed string member.\n");
      break;
    default:
      fprintf(stderr, "Parsed unrecognised member.\n");
      return GLC_INVALID_OP;
    }
  }
  return GLC_OK;
}

static int glacierVMFunctionDef(GlacierVM *vm) {
  uint8_t op, functionId, numArgs;
  GLC_RET(glacierByteCodeRead8(vm->bc, &op));
  if (op != GLACIER_BYTECODE_FUNCTION_DEF)
    return GLC_ERROR;
  GLC_RET(glacierByteCodeRead8(vm->bc, &functionId));
  GLC_RET(glacierByteCodeRead8(vm->bc, &numArgs));
  fprintf(stderr, "Executing function with id %d and %d args.\n", functionId,
          numArgs);
  GLC_RET(glacierCallStackPush(vm->cs));
  while (!glacierByteCodeEnd(vm->bc)) {
    uint8_t opCode;
    GLC_RET(glacierByteCodeRead8(vm->bc, &opCode));
    switch (opCode) {
    case GLACIER_BYTECODE_INT:
      GLC_RET(glacierVMInt(vm));
      break;
    case GLACIER_BYTECODE_ADD:
      GLC_RET(glacierVMAdd(vm));
      break;
    case GLACIER_BYTECODE_SUBTRACT:
      GLC_RET(glacierVMSubtract(vm));
      break;
    case GLACIER_BYTECODE_MULTIPLY:
      GLC_RET(glacierVMMultiply(vm));
      break;
    case GLACIER_BYTECODE_DIVIDE:
      GLC_RET(glacierVMDivide(vm));
      break;
    case GLACIER_BYTECODE_RETURN_VAL:
      GLC_RET(glacierVMReturnVal(vm));
      break;
    case GLACIER_BYTECODE_SET_VAR:
      GLC_RET(glacierVMSetVar(vm));
      break;
    case GLACIER_BYTECODE_GET_VAR:
      GLC_RET(glacierVMGetVar(vm));
      break;
    default:
      fprintf(stderr, "Parsed unrecognised instruction %d.\n", opCode);
      return GLC_INVALID_OP;
    }
  }
  return GLC_OK;
}

static int glacierVMInt(GlacierVM *vm) {
  uint8_t value;
  GLC_RET(glacierByteCodeRead8(vm->bc, &value));
  GLC_RET(glacierStackPush(vm->stack, value));
  fprintf(stderr, "Pushing an int of %d.\n", value);
  return GLC_OK;
}

static int glacierVMAdd(GlacierVM *vm) {
  int lhs, rhs;
  GLC_RET(glacierStackPop(vm->stack, &lhs));
  GLC_RET(glacierStackPop(vm->stack, &rhs));
  int result = lhs + rhs;
  GLC_RET(glacierStackPush(vm->stack, result));
  fprintf(stderr, "Adding %d and %d to get %d.\n", lhs, rhs, result);
  return GLC_OK;
}

static int glacierVMSubtract(GlacierVM *vm) {
  int lhs, rhs;
  GLC_RET(glacierStackPop(vm->stack, &lhs));
  GLC_RET(glacierStackPop(vm->stack, &rhs));
  int result = lhs - rhs;
  GLC_RET(glacierStackPush(vm->stack, result));
  fprintf(stderr, "Subtracting %d and %d to get %d.\n", lhs, rhs, result);
  return GLC_OK;
}

static int glacierVMMultiply(GlacierVM *vm) {
  int lhs, rhs;
  GLC_RET(glacierStackPop(vm->stack, &lhs));
  GLC_RET(glacierStackPop(vm->stack, &rhs));
  int result = lhs * rhs;
  GLC_RET(glacierStackPush(vm->stack, result));
  fprintf(stderr, "Multiplying %d and %d to get %d.\n", lhs, rhs, result);
  return GLC_OK;
}

static int glacierVMDivide(GlacierVM *vm) {
  int lhs, rhs;
  GLC_RET(glacierStackPop(vm->stack, &lhs));
  GLC_RET(glacierStackPop(vm->stack, &rhs));
  int result = lhs / rhs;
  GLC_RET(glacierStackPush(vm->stack, result));
  fprintf(stderr, "Dividing %d and %d to get %d.\n", lhs, rhs, result);
  return GLC_OK;
}

static int glacierVMReturnVal(GlacierVM *vm) {
  int top;
  GLC_RET(glacierStackPop(vm->stack, &top));
  GLC_RET(glacierCallStackPop(vm->cs));
  fprintf(stderr, "Returned with value %d.\n", top);
  return GLC_OK;
}

static int glacierVMHeader(GlacierVM *vm) {
  fprintf(stderr, "Reading bytecode header.\n");
  uint8_t val;
  while (true) {
    GLC_RET(glacierByteCodeRead8(vm->bc, &val));
    if (val == GLACIER_BYTECODE_HEADER_END)
      return GLC_OK;
    switch (val) {
    case GLACIER_BYTECODE_FUNCTION_JMP:
      GLC_RET(glacierVMFunctionJmp(vm));
      break;
    case GLACIER_BYTECODE_STRUCT_DEF:
      GLC_RET(glacierVMStructDef(vm));
      break;
    default:
      fprintf(stderr, "Unrecognised header op.\n");
      return GLC_INVALID_OP;
    }
  }
}

static int glacierVMFunctionJmp(GlacierVM *vm) {
  uint8_t functionId, offset;
  GLC_RET(glacierByteCodeRead8(vm->bc, &functionId));
  GLC_RET(glacierByteCodeRead8(vm->bc, &offset));
  GLC_RET(glacierFunctionTableSet(vm->ft, functionId, offset));
  fprintf(stderr, "Jump func for id %d at offset %d.\n", functionId, offset);
  return GLC_OK;
}

static int glacierVMSetVar(GlacierVM *vm) {
  uint8_t varId;
  int val;
  GLC_RET(glacierByteCodeRead8(vm->bc, &varId));
  GLC_RET(glacierStackPop(vm->stack, &val));
  GLC_RET(glacierCallStackSet(vm->cs, varId, val));
  fprintf(stderr, "Just set %d to value %d.\n", varId, val);
  return GLC_OK;
}

static int glacierVMGetVar(GlacierVM *vm) {
  uint8_t varId;
  int val;
  GLC_RET(glacierByteCodeRead8(vm->bc, &varId));
  GLC_RET(glacierCallStackGet(vm->cs, varId, &val));
  GLC_RET(glacierStackPush(vm->stack, val));
  fprintf(stderr, "Got %d and found value %d.\n", varId, val);
  return GLC_OK;
}
