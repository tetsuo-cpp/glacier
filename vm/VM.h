#ifndef GLACIERVM_VM_H
#define GLACIERVM_VM_H

#include "ByteCode.h"
#include "Stack.h"
#include "Table.h"

typedef struct {
  GlacierByteCode *bc;
  GlacierStack *stack;
  GlacierTable *ft;
  GlacierCallStack *cs;
  GlacierTable *st;
} GlacierVM;

void glacierVMInit(GlacierVM *vm, GlacierByteCode *bc, GlacierStack *stack,
                   GlacierTable *ft, GlacierCallStack *cs, GlacierTable *st);
int glacierVMRun(GlacierVM *vm);

#endif // GLACIERVM_VM_H
