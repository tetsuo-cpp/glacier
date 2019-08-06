#ifndef GLACIERVM_VM_H
#define GLACIERVM_VM_H

#include "ByteCode.h"
#include "FunctionTable.h"
#include "Stack.h"

typedef struct {
  GlacierByteCode *bc;
  GlacierStack *stack;
  GlacierFunctionTable *ft;
  GlacierCallStack *cs;
} GlacierVM;

void glacierVMInit(GlacierVM *vm, GlacierByteCode *bc, GlacierStack *stack,
                   GlacierFunctionTable *ft, GlacierCallStack *cs);
int glacierVMRun(GlacierVM *vm);

#endif // GLACIERVM_VM_H
