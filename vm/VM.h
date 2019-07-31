#ifndef GLACIERVM_VM_H
#define GLACIERVM_VM_H

#include "ByteCode.h"
#include "Stack.h"

typedef struct {
  GlacierByteCode *bc;
  GlacierStack *stack;
} GlacierVM;

void glacierVMInit(GlacierVM *vm, GlacierByteCode *bc, GlacierStack *stack);
int glacierVMRun(GlacierVM *vm);
int glacierVMStructDef(GlacierVM *vm);
int glacierVMFunctionDef(GlacierVM *vm);
int glacierVMInt(GlacierVM *vm);
int glacierVMAdd(GlacierVM *vm);
int glacierVMReturnVal(GlacierVM *vm);

#endif // GLACIERVM_VM_H
