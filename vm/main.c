#include "ByteCode.h"
#include "Util.h"
#include "VM.h"

#include <stdio.h>
#include <string.h>

#define BUF_SIZE 1024

int main(int arg, char **argv) {
  char buf[BUF_SIZE];
  FILE *inputFile = fopen("test.bc", "r");
  int len = fread(buf, sizeof(char), BUF_SIZE, inputFile);
  if (ferror(inputFile))
    return -1;

  GlacierByteCode bc;
  glacierByteCodeInit(&bc, buf, len);

  GlacierVM vm;
  glacierVMInit(&vm, &bc);
  GLC_RET(glacierVMRun(&vm));
  return 0;
}
