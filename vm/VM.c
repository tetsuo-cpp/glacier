#include "VM.h"

#include <stdio.h>

void glacierVMInit(GlacierVM *vm, GlacierByteCode *bc) { vm->bc = bc; }

void glacierVMRun(GlacierVM *vm) {
  while (!glacierByteCodeEnd(vm->bc)) {
    uint8_t byteVal = glacierByteCodeReadByte(vm->bc);
    fprintf(stderr, "Read byte %c.\n", byteVal);
    if (byteVal == GLACIER_BYTECODE_STRUCT_DEF)
      glacierVMStructDef(vm);
  }

  fprintf(stderr, "Reached end of bytecode. Exiting.\n");
}

void glacierVMStructDef(GlacierVM *vm) {
  uint8_t numMembers = glacierByteCodeReadByte(vm->bc);
  fprintf(stderr, "Parsing struct def with %d members.\n", numMembers);
  for (int i = 0; i < numMembers; ++i) {
    uint8_t typeId = glacierByteCodeReadByte(vm->bc);
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
}