#ifndef GLACIERVM_FUNCTIONTABLE_H
#define GLACIERVM_FUNCTIONTABLE_H

// Make this a resizeable vector later.
#define MAX_FUNCTION_NUMBER 1024

// TODO: Give this a more generic name since we're using it for struct defs now.
// Index = function id.
// Value = offset.
typedef struct {
  int data[MAX_FUNCTION_NUMBER];
} GlacierFunctionTable;

void glacierFunctionTableInit(GlacierFunctionTable *ft);
int glacierFunctionTableSet(GlacierFunctionTable *ft, int functionId,
                            int offset);
int glacierFunctionTableGet(GlacierFunctionTable *ft, int functionId,
                            int *offset);

#endif // GLACIERVM_FUNCTIONTABLE_H
