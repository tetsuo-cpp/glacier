set(
  GLACIER_FILES
  ByteCode.c
  ByteCode.h
  FunctionTable.c
  FunctionTable.h
  Stack.c
  Stack.h
  VM.c
  VM.h
  )

add_library(glaciervm_lib ${GLACIER_FILES})
