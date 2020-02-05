# add_subdirectory(
#   "${PROJECT_SOURCE_DIR}/vm/ext/bdwgc"
#   "ext/bdwgc"
#   )

set(
  GLACIER_FILES
  ByteCode.c
  ByteCode.h
  Array.c
  Array.h
  Stack.c
  Stack.h
  VM.c
  VM.h
  ds/Vector.c
  ds/Vector.h
  )

add_library(glaciervm_lib ${GLACIER_FILES})
