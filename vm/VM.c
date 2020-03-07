#include "VM.h"

#include "GC.h"
#include "Util.h"

#include <assert.h>
#include <stdio.h>

static int glacierVMStructDef(GlacierVM *vm);
static int glacierVMFunctionDef(GlacierVM *vm);
static int glacierVMInt(GlacierVM *vm);
static int glacierVMString(GlacierVM *vm);
static int glacierVMAdd(GlacierVM *vm);
static int glacierVMSubtract(GlacierVM *vm);
static int glacierVMMultiply(GlacierVM *vm);
static int glacierVMDivide(GlacierVM *vm);
static int glacierVMEq(GlacierVM *vm);
static int glacierVMLt(GlacierVM *vm);
static int glacierVMReturnVal(GlacierVM *vm);
static int glacierVMHeader(GlacierVM *vm);
static int glacierVMFunctionJmp(GlacierVM *vm);
static int glacierVMSetVar(GlacierVM *vm);
static int glacierVMGetVar(GlacierVM *vm);
static int glacierVMCallFunc(GlacierVM *vm);
static int glacierVMPrint(GlacierVM *vm);
static int glacierVMJumpIfFalse(GlacierVM *vm);
static int glacierVMJump(GlacierVM *vm);
static int glacierVMStructAlloc(GlacierVM *vm);
static int glacierVMStructGetMember(GlacierVM *vm);
static int glacierVMStructSetMember(GlacierVM *vm);
static int glacierVMSetArgs(GlacierVM *vm, int numArgs);
static int glacierVMVector(GlacierVM *vm);
static int glacierVMVectorAccess(GlacierVM *vm);
static int glacierVMMap(GlacierVM *vm);
static int glacierVMMapAccess(GlacierVM *vm);

void glacierVMInit(GlacierVM *vm, GlacierByteCode *bc, GlacierStack *stack,
                   GlacierTable *functionTable, GlacierCallStack *cs,
                   GlacierTable *symbolTable) {
  vm->bc = bc;
  vm->stack = stack;
  vm->functionTable = functionTable;
  vm->cs = cs;
  vm->symbolTable = symbolTable;
}

int glacierVMRun(GlacierVM *vm) {
  // Read structs and function offsets.
  GLC_RET(glacierVMHeader(vm));

  // All offsets are relative to the end of the header. Trim everything before
  // where we are now.
  GLC_RET(glacierByteCodeTrim(vm->bc));

  // Jump to main.
  int mainOffset;
  GLC_RET(glacierTableGet(vm->functionTable, 0, &mainOffset));
  GLC_RET(glacierByteCodeJump(vm->bc, mainOffset));
  GLC_RET(glacierCallStackPush(vm->cs, -1));

  // Execute main.
  GLC_RET(glacierVMFunctionDef(vm));

  // If we didn't get a non-zero then we terminated ok.
  return GLC_OK;
}

static int glacierVMStructDef(GlacierVM *vm) {
  uint8_t numMembers, structId;
  GLC_RET(glacierByteCodeRead8(vm->bc, &structId));
  GLC_RET(glacierByteCodeRead8(vm->bc, &numMembers));
  GLC_LOG_DBG("VM: Parsing struct def with id %d and %d members.\n", structId,
              numMembers);
  GLC_RET(glacierTableSet(vm->symbolTable, structId, numMembers));
  for (int i = 0; i < numMembers; ++i) {
    uint8_t typeId;
    GLC_RET(glacierByteCodeRead8(vm->bc, &typeId));
    switch (typeId) {
    case GLC_TYPEID_INT:
      GLC_LOG_DBG("VM: Parsed int member.\n");
      break;
    case GLC_TYPEID_STRING:
      GLC_LOG_DBG("VM: Parsed string member.\n");
      break;
    default:
      GLC_LOG_ERR("VM: Parsed unrecognised member.\n");
      return GLC_INVALID_OP;
    }
  }
  return GLC_OK;
}

static int glacierVMFunctionDef(GlacierVM *vm) {
  uint8_t op, functionId, numArgs;
  GLC_RET(glacierByteCodeRead8(vm->bc, &op));
  if (op != GLC_BYTECODE_FUNCTION_DEF)
    return GLC_ERROR;
  GLC_RET(glacierByteCodeRead8(vm->bc, &functionId));
  GLC_RET(glacierByteCodeRead8(vm->bc, &numArgs));
  GLC_LOG_DBG("VM: Executing function with id %d and %d args.\n", functionId,
              numArgs);
  GLC_RET(glacierVMSetArgs(vm, numArgs));
  while (!glacierByteCodeEnd(vm->bc)) {
    uint8_t opCode;
    GLC_RET(glacierByteCodeRead8(vm->bc, &opCode));
    switch (opCode) {
    case GLC_BYTECODE_INT:
      GLC_RET(glacierVMInt(vm));
      break;
    case GLC_BYTECODE_STRING:
      GLC_RET(glacierVMString(vm));
      break;
    case GLC_BYTECODE_ADD:
      GLC_RET(glacierVMAdd(vm));
      break;
    case GLC_BYTECODE_SUBTRACT:
      GLC_RET(glacierVMSubtract(vm));
      break;
    case GLC_BYTECODE_MULTIPLY:
      GLC_RET(glacierVMMultiply(vm));
      break;
    case GLC_BYTECODE_DIVIDE:
      GLC_RET(glacierVMDivide(vm));
      break;
    case GLC_BYTECODE_EQ:
      GLC_RET(glacierVMEq(vm));
      break;
    case GLC_BYTECODE_LT:
      GLC_RET(glacierVMLt(vm));
      break;
    case GLC_BYTECODE_RETURN:
    case GLC_BYTECODE_RETURN_VAL: {
      int bcOffset;
      if (opCode == GLC_BYTECODE_RETURN_VAL)
        GLC_RET(glacierVMReturnVal(vm));
      GLC_RET(glacierCallStackGetByteCodeOffset(vm->cs, &bcOffset));
      GLC_RET(glacierCallStackPop(vm->cs));
      if (vm->cs->stackPointer != 0)
        GLC_RET(glacierByteCodeJump(vm->bc, bcOffset));
      else
        assert(bcOffset == -1);
      return GLC_OK;
    }
    case GLC_BYTECODE_SET_VAR:
      GLC_RET(glacierVMSetVar(vm));
      break;
    case GLC_BYTECODE_GET_VAR:
      GLC_RET(glacierVMGetVar(vm));
      break;
    case GLC_BYTECODE_CALL_FUNC:
      GLC_RET(glacierVMCallFunc(vm));
      break;
    case GLC_BYTECODE_PRINT:
      GLC_RET(glacierVMPrint(vm));
      break;
    case GLC_BYTECODE_JUMP_IF_FALSE:
      GLC_RET(glacierVMJumpIfFalse(vm));
      break;
    case GLC_BYTECODE_JUMP:
      GLC_RET(glacierVMJump(vm));
      break;
    case GLC_BYTECODE_STRUCT:
      GLC_RET(glacierVMStructAlloc(vm));
      break;
    case GLC_BYTECODE_GET_STRUCT_MEMBER:
      GLC_RET(glacierVMStructGetMember(vm));
      break;
    case GLC_BYTECODE_SET_STRUCT_MEMBER:
      GLC_RET(glacierVMStructSetMember(vm));
      break;
    case GLC_BYTECODE_VEC:
      GLC_RET(glacierVMVector(vm));
      break;
    case GLC_BYTECODE_VEC_ACCESS:
      GLC_RET(glacierVMVectorAccess(vm));
      break;
    case GLC_BYTECODE_MAP:
      GLC_RET(glacierVMMap(vm));
      break;
    case GLC_BYTECODE_MAP_ACCESS:
      GLC_RET(glacierVMMapAccess(vm));
      break;
    default:
      GLC_LOG_ERR("VM: Parsed unrecognised instruction %d.\n", opCode);
      return GLC_INVALID_OP;
    }
  }
  // At the moment, we're assuming all functions should be terminated by a
  // return. If we run right off the end of the bytecode buffer, that's a nono
  // from the compiler.
  return GLC_OUT_OF_BUFFER;
}

static int glacierVMInt(GlacierVM *vm) {
  uint8_t value;
  GLC_RET(glacierByteCodeRead8(vm->bc, &value));
  GLC_RET(glacierStackPush(vm->stack, glacierValueFromInt(value)));
  GLC_LOG_DBG("VM: Pushing an int of %d.\n", value);
  return GLC_OK;
}

static int glacierVMString(GlacierVM *vm) {
  GLC_DECL_RET;
  uint8_t length;
  GLC_RET(glacierByteCodeRead8(vm->bc, &length));
  char *stringVal;
  GLC_RET(glacierGCAlloc(sizeof(char) * (length + 1), &stringVal));
  for (int i = 0; i < length; ++i) {
    uint8_t val;
    GLC_ERR(glacierByteCodeRead8(vm->bc, &val));
    stringVal[i] = val;
  }
  stringVal[length] = '\0';
  GLC_ERR(glacierStackPush(vm->stack, glacierValueFromString(stringVal)));
  GLC_LOG_DBG("VM: Pushing a string of \"%s\".\n", stringVal);
  return GLC_OK;

err:
  glacierGCFree((char **)&stringVal);
  return ret;
}

static int glacierVMAdd(GlacierVM *vm) {
  GlacierValue lhs, rhs;
  GLC_RET(glacierStackPop(vm->stack, &rhs));
  GLC_RET(glacierStackPop(vm->stack, &lhs));
  assert(lhs.typeId == GLC_TYPEID_INT && rhs.typeId == GLC_TYPEID_INT);
  GlacierValue result = glacierValueFromInt(lhs.intValue + rhs.intValue);
  GLC_RET(glacierStackPush(vm->stack, result));
  GLC_LOG_DBG("VM: Adding %llu and %llu to get %llu.\n", lhs.intValue,
              rhs.intValue, result.intValue);
  return GLC_OK;
}

static int glacierVMSubtract(GlacierVM *vm) {
  GlacierValue lhs, rhs;
  GLC_RET(glacierStackPop(vm->stack, &rhs));
  GLC_RET(glacierStackPop(vm->stack, &lhs));
  assert(lhs.typeId == GLC_TYPEID_INT && rhs.typeId == GLC_TYPEID_INT);
  GlacierValue result = glacierValueFromInt(lhs.intValue - rhs.intValue);
  GLC_RET(glacierStackPush(vm->stack, result));
  GLC_LOG_DBG("VM: Subtracting %llu and %llu to get %llu.\n", lhs.intValue,
              rhs.intValue, result.intValue);
  return GLC_OK;
}

static int glacierVMMultiply(GlacierVM *vm) {
  GlacierValue lhs, rhs;
  GLC_RET(glacierStackPop(vm->stack, &rhs));
  GLC_RET(glacierStackPop(vm->stack, &lhs));
  assert(lhs.typeId == GLC_TYPEID_INT && rhs.typeId == GLC_TYPEID_INT);
  GlacierValue result = glacierValueFromInt(lhs.intValue * rhs.intValue);
  GLC_RET(glacierStackPush(vm->stack, result));
  GLC_LOG_DBG("VM: Multiplying %llu and %llu to get %llu.\n", lhs.intValue,
              rhs.intValue, result.intValue);
  return GLC_OK;
}

static int glacierVMDivide(GlacierVM *vm) {
  GlacierValue lhs, rhs;
  GLC_RET(glacierStackPop(vm->stack, &rhs));
  GLC_RET(glacierStackPop(vm->stack, &lhs));
  assert(lhs.typeId == GLC_TYPEID_INT && rhs.typeId == GLC_TYPEID_INT);
  GlacierValue result = glacierValueFromInt(lhs.intValue / rhs.intValue);
  GLC_RET(glacierStackPush(vm->stack, result));
  GLC_LOG_DBG("VM: Dividing %llu and %llu to get %llu.\n", lhs.intValue,
              rhs.intValue, result.intValue);
  return GLC_OK;
}

static int glacierVMEq(GlacierVM *vm) {
  GlacierValue lhs, rhs;
  GLC_RET(glacierStackPop(vm->stack, &rhs));
  GLC_RET(glacierStackPop(vm->stack, &lhs));
  assert(lhs.typeId == GLC_TYPEID_INT && rhs.typeId == GLC_TYPEID_INT);
  GlacierValue result =
      glacierValueFromInt(lhs.intValue == rhs.intValue ? 1 : 0);
  GLC_RET(glacierStackPush(vm->stack, result));
  GLC_LOG_DBG("VM: Equating %llu and %llu to got %llu.\n", lhs.intValue,
              rhs.intValue, result.intValue);
  return GLC_OK;
}

static int glacierVMLt(GlacierVM *vm) {
  GlacierValue lhs, rhs;
  GLC_RET(glacierStackPop(vm->stack, &rhs));
  GLC_RET(glacierStackPop(vm->stack, &lhs));
  assert(lhs.typeId == GLC_TYPEID_INT && rhs.typeId == GLC_TYPEID_INT);
  GlacierValue result =
      glacierValueFromInt(lhs.intValue < rhs.intValue ? 1 : 0);
  GLC_RET(glacierStackPush(vm->stack, result));
  GLC_LOG_DBG("VM: Comparing if %llu is less than %llu to got %llu.\n",
              lhs.intValue, rhs.intValue, result.intValue);
  return GLC_OK;
}

static int glacierVMReturnVal(GlacierVM *vm) {
  GlacierValue top;
  GLC_RET(glacierStackTop(vm->stack, &top));
  assert(top.typeId == GLC_TYPEID_INT || top.typeId == GLC_TYPEID_STRING);
  if (top.typeId == GLC_TYPEID_INT)
    GLC_LOG_DBG("VM: Returned with value %llu.\n", top.intValue);
  else if (top.typeId == GLC_TYPEID_STRING)
    GLC_LOG_DBG("VM: Returned with value %s.\n", top.stringValue);
  else
    assert(false);
  return GLC_OK;
}

static int glacierVMHeader(GlacierVM *vm) {
  GLC_LOG_DBG("VM: Reading bytecode header.\n");
  uint8_t val;
  while (true) {
    GLC_RET(glacierByteCodeRead8(vm->bc, &val));
    if (val == GLC_BYTECODE_HEADER_END)
      return GLC_OK;
    switch (val) {
    case GLC_BYTECODE_FUNCTION_JMP:
      GLC_RET(glacierVMFunctionJmp(vm));
      break;
    case GLC_BYTECODE_STRUCT_DEF:
      GLC_RET(glacierVMStructDef(vm));
      break;
    default:
      GLC_LOG_ERR("VM: Unrecognised header op %d.\n", val);
      return GLC_INVALID_OP;
    }
  }
}

static int glacierVMFunctionJmp(GlacierVM *vm) {
  uint8_t functionId, offset;
  GLC_RET(glacierByteCodeRead8(vm->bc, &functionId));
  GLC_RET(glacierByteCodeRead8(vm->bc, &offset));
  GLC_RET(glacierTableSet(vm->functionTable, functionId, offset));
  GLC_LOG_DBG("VM: Jump func for id %d at offset %d.\n", functionId, offset);
  return GLC_OK;
}

static int glacierVMSetVar(GlacierVM *vm) {
  uint8_t varId;
  GlacierValue val;
  GLC_RET(glacierByteCodeRead8(vm->bc, &varId));
  GLC_RET(glacierStackPop(vm->stack, &val));
  GLC_RET(glacierCallStackSet(vm->cs, varId, val));

  GLC_LOG_DBG("VM: Just set %d to ", varId);
  glacierValueLog(&val);
  GLC_LOG_DBG("\n");
  return GLC_OK;
}

static int glacierVMGetVar(GlacierVM *vm) {
  uint8_t varId;
  GlacierValue val;
  GLC_RET(glacierByteCodeRead8(vm->bc, &varId));
  GLC_RET(glacierCallStackGet(vm->cs, varId, &val));
  GLC_RET(glacierStackPush(vm->stack, val));

  GLC_LOG_DBG("VM: Got %d and got ", varId);
  glacierValueLog(&val);
  GLC_LOG_DBG("\n");
  return GLC_OK;
}

static int glacierVMCallFunc(GlacierVM *vm) {
  uint8_t functionId;
  int functionOffset;
  GLC_RET(glacierByteCodeRead8(vm->bc, &functionId));
  GLC_RET(glacierTableGet(vm->functionTable, functionId, &functionOffset));

  // We need to jump back here after the function call is done.
  GLC_RET(glacierCallStackPush(vm->cs, vm->bc->offset));
  GLC_RET(glacierByteCodeJump(vm->bc, functionOffset));
  GLC_RET(glacierVMFunctionDef(vm));
  return GLC_OK;
}

static int glacierVMPrint(GlacierVM *vm) {
  GlacierValue value;
  GLC_RET(glacierStackPop(vm->stack, &value));
  switch (value.typeId) {
  case GLC_TYPEID_INT:
    printf("%llu\n", value.intValue);
    break;
  case GLC_TYPEID_STRING:
    printf("%s\n", value.stringValue);
    break;
  default:
    GLC_LOG_ERR("VM: Print on invalid type id %d.\n", value.typeId);
    return GLC_INVALID_OP;
  }
  return GLC_OK;
}

static int glacierVMJumpIfFalse(GlacierVM *vm) {
  uint8_t offset;
  GLC_RET(glacierByteCodeRead8(vm->bc, &offset));
  GlacierValue value;
  GLC_RET(glacierStackPop(vm->stack, &value));
  assert(value.typeId == GLC_TYPEID_INT);
  assert(value.intValue == 0 || value.intValue == 1);
  if (value.intValue == 0)
    GLC_RET(glacierByteCodeJump(vm->bc, offset));
  return GLC_OK;
}

static int glacierVMJump(GlacierVM *vm) {
  uint8_t offset;
  GLC_RET(glacierByteCodeRead8(vm->bc, &offset));
  GLC_RET(glacierByteCodeJump(vm->bc, offset));
  return GLC_OK;
}

static int glacierVMStructAlloc(GlacierVM *vm) {
  GLC_DECL_RET;
  uint8_t structId;
  GLC_RET(glacierByteCodeRead8(vm->bc, &structId));
  int numMembers;
  GLC_RET(glacierTableGet(vm->symbolTable, structId, &numMembers));
  GlacierValue *structVal;
  GLC_RET(
      glacierGCAlloc(sizeof(GlacierValue) * numMembers, (char **)&structVal));
  for (int i = 0; i < numMembers; ++i) {
    GlacierValue memberValue;
    GLC_ERR(glacierStackPop(vm->stack, &memberValue));
    structVal[numMembers - i - 1] = memberValue;
  }
  GLC_ERR(
      glacierStackPush(vm->stack, glacierValueFromStruct(structVal, structId)));
  GLC_LOG_DBG("VM: Pushing a struct of type id %d.\n", structId);
  return GLC_OK;

err:
  glacierGCFree((char **)&structVal);
  return ret;
}

static int glacierVMStructGetMember(GlacierVM *vm) {
  uint8_t memberNumber;
  GLC_RET(glacierByteCodeRead8(vm->bc, &memberNumber));
  GlacierValue structVal;
  GLC_RET(glacierStackPop(vm->stack, &structVal));
  assert(structVal.typeId != GLC_TYPEID_INT &&
         structVal.typeId != GLC_TYPEID_STRING);

  // Now reach into the struct data and get the appropriate member.
  GlacierValue *member = structVal.structValue + memberNumber;
  GLC_RET(glacierStackPush(vm->stack, *member));
  GLC_LOG_DBG("VM: Pushing struct member of value ");
  glacierValueLog(member);
  GLC_LOG_DBG("\n");
  return GLC_OK;
}

static int glacierVMStructSetMember(GlacierVM *vm) {
  uint8_t memberNumber;
  GLC_RET(glacierByteCodeRead8(vm->bc, &memberNumber));
  GlacierValue structVal, setVal;
  // Nobody knows what type this is.
  GLC_RET(glacierStackPop(vm->stack, &structVal));
  GLC_RET(glacierStackPop(vm->stack, &setVal));

  // Now reach into the struct data and set the appropriate member.
  GlacierValue *member = structVal.structValue + memberNumber;
  *member = setVal;
  return GLC_OK;
}

static int glacierVMSetArgs(GlacierVM *vm, int numArgs) {
  assert(numArgs >= 0);
  GlacierValue val;
  for (int i = 0; i < numArgs; ++i) {
    GLC_RET(glacierStackPop(vm->stack, &val));
    GLC_RET(glacierCallStackSet(vm->cs, numArgs - i - 1, val));

    GLC_LOG_DBG("VM: Just set arg %d to ", i);
    glacierValueLog(&val);
    GLC_LOG_DBG("\n");
  }
  return GLC_OK;
}

static int glacierVMVector(GlacierVM *vm) {
  int ret;
  uint8_t numElements;
  GLC_RET(glacierByteCodeRead8(vm->bc, &numElements));
  GlacierVector vector;
  GLC_RET(glacierVectorInit(&vector));
  for (int i = 0; i < numElements; ++i) {
    GlacierValue element;
    GLC_ERR(glacierStackPop(vm->stack, &element));
    GLC_ERR(glacierVectorPush(&vector, element));
  }
  GlacierValue vectorVal = glacierValueFromVector(vector);
  GLC_ERR(glacierStackPush(vm->stack, vectorVal));
  return GLC_OK;
err:
  glacierVectorDestroy(&vector);
  return ret;
}

static int glacierVMVectorAccess(GlacierVM *vm) {
  GlacierValue index, vector, element;
  GLC_RET(glacierStackPop(vm->stack, &index));
  GLC_RET(glacierStackPop(vm->stack, &vector));
  assert(index.typeId == GLC_TYPEID_INT);
  assert(vector.typeId == GLC_TYPEID_VECTOR);
  uint64_t i = index.intValue;
  GlacierVector *v = &vector.vectorValue;
  GLC_RET(glacierVectorGet(v, i, &element));
  GLC_RET(glacierStackPush(vm->stack, element));
  return GLC_OK;
}

static int glacierVMMap(GlacierVM *vm) {
  uint8_t numElements;
  GLC_RET(glacierByteCodeRead8(vm->bc, &numElements));
  GlacierMap map;
  int ret = GLC_OK;
  GLC_RET(glacierMapInit(&map));
  for (size_t i = 0; i < numElements; ++i) {
    GlacierValue key, value;
    GLC_ERR(glacierStackPop(vm->stack, &value));
    GLC_ERR(glacierStackPop(vm->stack, &key));
    GLC_ERR(glacierMapSet(&map, key, value));
  }
  GlacierValue mapVal = glacierValueFromMap(map);
  GLC_ERR(glacierStackPush(vm->stack, mapVal));
err:
  if (ret != GLC_OK)
    glacierMapDestroy(&map);
  return ret;
}

static int glacierVMMapAccess(GlacierVM *vm) {
  GlacierValue key, map;
  GLC_RET(glacierStackPop(vm->stack, &key));
  assert(key.typeId == GLC_TYPEID_INT || key.typeId == GLC_TYPEID_STRING);
  GLC_RET(glacierStackPop(vm->stack, &map));
  assert(map.typeId == GLC_TYPEID_MAP);
  GlacierMap *m = &map.mapValue;
  GlacierValue value;
  GLC_RET(glacierMapGet(m, key, &value));
  GLC_RET(glacierStackPush(vm->stack, value));
  return GLC_OK;
}
