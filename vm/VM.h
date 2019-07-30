#ifndef GLACIERVM_VM_H
#define GLACIERVM_VM_H

#include "ByteCode.h"

typedef struct {
  GlacierByteCode *bc;
} GlacierVM;

void glacierVMInit(GlacierVM *vm, GlacierByteCode *bc);
int glacierVMRun(GlacierVM *vm);
int glacierVMStructDef(GlacierVM *vm);
int glacierVMFunctionDef(GlacierVM *vm);

#endif // GLACIERVM_VM_H
