#ifndef GLACIERVM_VM_H
#define GLACIERVM_VM_H

#include "ByteCode.h"

typedef struct {
  GlacierByteCode *bc;
} GlacierVM;

void glacierVMInit(GlacierVM *vm, GlacierByteCode *bc);
void glacierVMRun(GlacierVM *vm);
void glacierVMStructDef(GlacierVM *vm);

#endif // GLACIERVM_VM_H
