cmake_minimum_required(VERSION 3.13)
project(glaciervm C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_BUILD_TYPE Debug)
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -Wextra -Werror")

# Toggle to get verbose logging.
# add_definitions(-DLOG_DBG)

add_subdirectory(vm)

add_executable(glaciervm vm/main.c)
target_link_libraries(glaciervm glaciervm_lib)
target_include_directories(glaciervm PRIVATE vm)
