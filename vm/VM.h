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
  GlacierFunctionTable *st;
} GlacierVM;

void glacierVMInit(GlacierVM *vm, GlacierByteCode *bc, GlacierStack *stack,
                   GlacierFunctionTable *ft, GlacierCallStack *cs,
                   GlacierFunctionTable *st);
int glacierVMRun(GlacierVM *vm);

#endif // GLACIERVM_VM_H
