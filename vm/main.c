#include "ByteCode.h"
#include "Util.h"
#include "VM.h"

#include <stdio.h>
#include <string.h>

#define BUF_SIZE 1024

int main(int arg, char **argv) {
  GLC_UNUSED(arg);
  GLC_UNUSED(argv);

  char buf[BUF_SIZE];
  FILE *inputFile = fopen("test.bc", "r");
  int len = fread(buf, sizeof(char), BUF_SIZE, inputFile);
  if (ferror(inputFile))
    return -1;

  GlacierByteCode bc;
  glacierByteCodeInit(&bc, buf, len);

  GlacierFunctionTable ft;
  glacierFunctionTableInit(&ft);

  GlacierStack stack;
  glacierStackInit(&stack);

  GlacierVM vm;
  glacierVMInit(&vm, &bc, &stack, &ft);
  int ret = glacierVMRun(&vm);
  if (ret != 0)
    fprintf(stderr, "terminated unsuccessfully.\n");
  return 0;
}
