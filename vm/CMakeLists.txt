cmake_minimum_required(VERSION 3.13)
project(glaciervm C)

set(CMAKE_C_STANDARD 11)

set(
  GLACIER_FILES
  ByteCode.c
  ByteCode.h
  Stack.c
  Stack.h
  VM.c
  VM.h
  )

add_executable(glaciervm main.c ${GLACIER_FILES})
