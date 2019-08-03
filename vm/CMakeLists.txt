cmake_minimum_required(VERSION 3.13)
project(glaciervm C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -Wextra -Werror")

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

add_executable(glaciervm main.c ${GLACIER_FILES})
