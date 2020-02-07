#ifndef GLACIERVM_VM_H
#define GLACIERVM_VM_H

#include "ByteCode.h"
#include "Stack.h"
#include "Table.h"

typedef struct {
  GlacierByteCode *bc;
  GlacierStack *stack;
  GlacierTable *functionTable;
  GlacierCallStack *cs;
  GlacierTable *symbolTable;
} GlacierVM;

void glacierVMInit(GlacierVM *vm, GlacierByteCode *bc, GlacierStack *stack,
                   GlacierTable *functionTable, GlacierCallStack *cs,
                   GlacierTable *symbolTable);
int glacierVMRun(GlacierVM *vm);

#endif // GLACIERVM_VM_H
