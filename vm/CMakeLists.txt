include(ExternalProject)

set(GLACIER_BDWGC_DIR ${CMAKE_CURRENT_SOURCE_DIR}/ext/bdwgc)

ExternalProject_Add(
  libgc
  PREFIX ${GLACIER_BDWGC_DIR}/bin
  SOURCE_DIR ${GLACIER_BDWGC_DIR}
  DOWNLOAD_COMMAND git submodule update && cd ${GLACIER_BDWGC_DIR} && ./autogen.sh
  CONFIGURE_COMMAND ${GLACIER_BDWGC_DIR}/configure --prefix=${GLACIER_BDWGC_DIR}/bin --enable-static --disable-shared
  BUILD_COMMAND make
  BUILD_IN_SOURCE 1
  )

set(GLACIER_BDWGC_STATIC_LIB ${CMAKE_CURRENT_SOURCE_DIR}/ext/bdwgc/bin/lib/libgc.a)
set(GLACIER_BDWGC_INCLUDES ${CMAKE_CURRENT_SOURCE_DIR}/ext/bdwgc/bin/include)
add_library(gc STATIC IMPORTED GLOBAL)
add_dependencies(gc libgc)
set_target_properties(gc PROPERTIES IMPORTED_LOCATION ${GLACIER_BDWGC_STATIC_LIB})
set_target_properties(gc PROPERTIES INTERFACE_INCLUDE_DIRECTORIES ${GLACIER_BDWGC_INCLUDES})

set(
  GLACIER_FILES
  ByteCode.c
  ByteCode.h
  GC.c
  GC.h
  Table.c
  Table.h
  Stack.c
  Stack.h
  VM.c
  VM.h
  ds/Vector.c
  ds/Vector.h
  ds/Map.c
  ds/Map.h
  )

add_library(glaciervm_lib ${GLACIER_FILES})
target_link_libraries(glaciervm_lib gc)
