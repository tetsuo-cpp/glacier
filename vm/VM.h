#ifndef GLACIERVM_VM_H
#define GLACIERVM_VM_H

#include "Array.h"
#include "ByteCode.h"
#include "Stack.h"

typedef struct {
  GlacierByteCode *bc;
  GlacierStack *stack;
  GlacierArray *ft;
  GlacierCallStack *cs;
  GlacierArray *st;
} GlacierVM;

void glacierVMInit(GlacierVM *vm, GlacierByteCode *bc, GlacierStack *stack,
                   GlacierArray *ft, GlacierCallStack *cs, GlacierArray *st);
int glacierVMRun(GlacierVM *vm);

#endif // GLACIERVM_VM_H
