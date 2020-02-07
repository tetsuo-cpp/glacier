#include "ByteCode.h"
#include "Util.h"
#include "VM.h"

#include <stdio.h>
#include <string.h>

#define GLC_BYTECODE_BUF_LEN 1024

int main(int argc, char **argv) {
  if (argc != 2) {
    GLC_LOG_ERR("Usage: glaciervm <bytecode_file>\n");
    return -1;
  }

  char buf[GLC_BYTECODE_BUF_LEN];
  FILE *inputFile = fopen(argv[1], "r");
  int len = fread(buf, sizeof(char), GLC_BYTECODE_BUF_LEN, inputFile);
  if (ferror(inputFile))
    return -1;

  GlacierByteCode bc;
  glacierByteCodeInit(&bc, buf, len);

  GlacierTable functionTable;
  glacierTableInit(&functionTable);

  GlacierStack stack;
  glacierStackInit(&stack);

  GlacierCallStack cs;
  glacierCallStackInit(&cs);

  GlacierTable symbolTable;
  glacierTableInit(&symbolTable);

  GlacierVM vm;
  glacierVMInit(&vm, &bc, &stack, &functionTable, &cs, &symbolTable);
  int ret = glacierVMRun(&vm);
  if (ret != 0) {
    GLC_LOG_ERR("glaciervm: Terminated unsuccessfully with %s.\n",
                glacierUtilErrorToString(ret));
    glacierByteCodePrint(&bc, stderr);
  }
  glacierTableDestroy(&functionTable);
  glacierTableDestroy(&symbolTable);
  return ret;
}
