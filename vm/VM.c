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

void glacierVMInit(GlacierVM *vm, GlacierByteCode *bc, GlacierStack *stack) {
  vm->bc = bc;
  vm->stack = stack;
}

int glacierVMRun(GlacierVM *vm) {
  while (!glacierByteCodeEnd(vm->bc)) {
    uint8_t byteVal;
    GLC_RET(glacierByteCodeRead8(vm->bc, &byteVal));
    fprintf(stderr, "Read byte %c.\n", byteVal);
    switch (byteVal) {
    case GLACIER_BYTECODE_STRUCT_DEF:
      glacierVMStructDef(vm);
      break;
    case GLACIER_BYTECODE_FUNCTION_DEF:
      glacierVMFunctionDef(vm);
      break;
    default:
      fprintf(stderr, "Unrecognised opcode.\n");
      break;
    }
  }
  fprintf(stderr, "Reached end of bytecode. Exiting.\n");
  return 0;
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
      break;
    }
  }
  return 0;
}

static int glacierVMFunctionDef(GlacierVM *vm) {
  uint8_t functionId, numArgs;
  GLC_RET(glacierByteCodeRead8(vm->bc, &functionId));
  GLC_RET(glacierByteCodeRead8(vm->bc, &numArgs));
  fprintf(stderr, "Parsing function with id %d and %d args.\n", functionId,
          numArgs);
  while (!glacierByteCodeEnd(vm->bc)) {
    uint8_t opCode;
    GLC_RET(glacierByteCodeRead8(vm->bc, &opCode));
    switch (opCode) {
    case GLACIER_BYTECODE_INT:
      glacierVMInt(vm);
      break;
    case GLACIER_BYTECODE_ADD:
      glacierVMAdd(vm);
      break;
    case GLACIER_BYTECODE_SUBTRACT:
      glacierVMSubtract(vm);
      break;
    case GLACIER_BYTECODE_MULTIPLY:
      glacierVMMultiply(vm);
      break;
    case GLACIER_BYTECODE_DIVIDE:
      glacierVMDivide(vm);
      break;
    case GLACIER_BYTECODE_RETURN_VAL:
      glacierVMReturnVal(vm);
      break;
    default:
      fprintf(stderr, "Parsed unrecognised instruction.\n");
      break;
    }
  }
  return 0;
}

static int glacierVMInt(GlacierVM *vm) {
  uint8_t value;
  GLC_RET(glacierByteCodeRead8(vm->bc, &value));
  GLC_RET(glacierStackPush(vm->stack, value));
  fprintf(stderr, "Pushing an int of %d.\n", value);
  return 0;
}

static int glacierVMAdd(GlacierVM *vm) {
  int lhs, rhs;
  GLC_RET(glacierStackPop(vm->stack, &lhs));
  GLC_RET(glacierStackPop(vm->stack, &rhs));
  int result = lhs + rhs;
  GLC_RET(glacierStackPush(vm->stack, result));
  fprintf(stderr, "Adding %d and %d to get %d.\n", lhs, rhs, result);
  return 0;
}

static int glacierVMSubtract(GlacierVM *vm) {
  int lhs, rhs;
  GLC_RET(glacierStackPop(vm->stack, &lhs));
  GLC_RET(glacierStackPop(vm->stack, &rhs));
  int result = lhs - rhs;
  GLC_RET(glacierStackPush(vm->stack, result));
  fprintf(stderr, "Subtracting %d and %d to get %d.\n", lhs, rhs, result);
  return 0;
}

static int glacierVMMultiply(GlacierVM *vm) {
  int lhs, rhs;
  GLC_RET(glacierStackPop(vm->stack, &lhs));
  GLC_RET(glacierStackPop(vm->stack, &rhs));
  int result = lhs * rhs;
  GLC_RET(glacierStackPush(vm->stack, result));
  fprintf(stderr, "Multiplying %d and %d to get %d.\n", lhs, rhs, result);
  return 0;
}

static int glacierVMDivide(GlacierVM *vm) {
  int lhs, rhs;
  GLC_RET(glacierStackPop(vm->stack, &lhs));
  GLC_RET(glacierStackPop(vm->stack, &rhs));
  int result = lhs / rhs;
  GLC_RET(glacierStackPush(vm->stack, result));
  fprintf(stderr, "Dividing %d and %d to get %d.\n", lhs, rhs, result);
  return 0;
}

static int glacierVMReturnVal(GlacierVM *vm) {
  int top;
  GLC_RET(glacierStackPop(vm->stack, &top));
  fprintf(stderr, "Returned with value %d.\n", top);
  return 0;
}
