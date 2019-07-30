#include "VM.h"

#include "Util.h"

#include <stdio.h>

void glacierVMInit(GlacierVM *vm, GlacierByteCode *bc) { vm->bc = bc; }

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

int glacierVMStructDef(GlacierVM *vm) {
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

int glacierVMFunctionDef(GlacierVM *vm) {
  uint8_t functionId, numArgs;
  GLC_RET(glacierByteCodeRead8(vm->bc, &functionId));
  GLC_RET(glacierByteCodeRead8(vm->bc, &numArgs));
  return 0;
}
