cmake_minimum_required(VERSION 3.14)
project(glaciervm C)

set(CMAKE_C_STANDARD 11)

set(GLACIER_FILES
        ByteCode.c
        ByteCode.h VM.c VM.h)

add_executable(glaciervm main.c ${GLACIER_FILES})