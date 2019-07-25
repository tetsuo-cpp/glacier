#include "ByteCode.h"
#include "VM.h"

#include <stdio.h>
#include <string.h>

int main(int arg, char **argv) {
  char input[1024];
  FILE *f = fopen("test.bc", "r");
  int len = fread(input, sizeof(char), 1024, f);
  if (ferror(f))
    return -1;

  GlacierByteCode bc;
  glacierByteCodeInit(&bc, input, len);

  GlacierVM vm;
  glacierVMInit(&vm, &bc);
  glacierVMRun(&vm);
  return 0;
}
