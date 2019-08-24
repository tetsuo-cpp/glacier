#include "ByteCode.h"
#include "Util.h"
#include "VM.h"

#include <stdio.h>
#include <string.h>

#define BUF_SIZE 1024

int main(int argc, char **argv) {
  if (argc != 2) {
    GLC_LOG_ERR("Usage: glaciervm [BYTECODE_FILE]\n");
    return -1;
  }

  char buf[BUF_SIZE];
  FILE *inputFile = fopen(argv[1], "r");
  int len = fread(buf, sizeof(char), BUF_SIZE, inputFile);
  if (ferror(inputFile))
    return -1;

  GlacierByteCode bc;
  glacierByteCodeInit(&bc, buf, len);

  GlacierFunctionTable ft;
  glacierFunctionTableInit(&ft);

  GlacierStack stack;
  glacierStackInit(&stack);

  GlacierCallStack cs;
  glacierCallStackInit(&cs);

  GlacierVM vm;
  glacierVMInit(&vm, &bc, &stack, &ft, &cs);
  int ret = glacierVMRun(&vm);
  if (ret != 0) {
    GLC_LOG_ERR("glaciervm: Terminated unsuccessfully with %s.\n",
                glacierUtilErrorToString(ret));
    glacierByteCodePrint(&bc, stderr);
  }
  return ret;
}
