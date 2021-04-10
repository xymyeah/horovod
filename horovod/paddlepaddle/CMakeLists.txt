if("$ENV{HOROVOD_WITHOUT_PADDLEPADDLE}" STREQUAL "1")
    return()
endif()

set(PADDLE_TARGET_LIB "paddlepaddle")

# Find PaddlePaddle
set(PADDLEPADDLE_REQUIRED "")
if ("$ENV{HOROVOD_WITH_PADDLEPADDLE}" STREQUAL "1")
    set(PADDLEPADDLE_REQUIRED "REQUIRED")
endif ()
find_package(PaddlePaddle "2.0.1" ${PADDLEPADDLE_REQUIRED})
if(NOT PADDLEPADDLE_FOUND)
    return()
endif()

# Append version number into metadata
file(APPEND "${CMAKE_LIBRARY_OUTPUT_DIRECTORY_ROOT}/metadata.json" "\"paddlepaddle\": \"${PaddlePaddle_VERSION}\",\n")

if (HAVE_CUDA AND NOT PaddlePaddle_CUDA)
    message(FATAL_ERROR "Horovod build with GPU support was requested but this PaddlePaddle installation does not support CUDA.")
elseif (PaddlePaddle_CUDA AND NOT HAVE_CUDA)
    add_cuda()
endif()

include_directories(SYSTEM ${PaddlePaddle_INCLUDE_DIRS})
execute_process(COMMAND ${PY_EXE} -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())"
                OUTPUT_VARIABLE PYTHON_INCLUDE_PATH OUTPUT_STRIP_TRAILING_WHITESPACE)
include_directories(SYSTEM ${PYTHON_INCLUDE_PATH})
set(CMAKE_CXX_FLAGS "${PaddlePaddle_COMPILE_FLAGS} ${CMAKE_CXX_FLAGS}")
list(APPEND PADDLEPADDLE_LINKER_LIBS ${PaddlePaddle_LIBRARIES})
if(HAVE_GLOO)
    if (PaddlePaddle_CXX11)
        list(APPEND PADDLEPADDLE_LINKER_LIBS gloo)
    else()
        list(APPEND PADDLEPADDLE_LINKER_LIBS compatible_gloo)
    endif()
endif()
if(HAVE_CUDA)
    if (PaddlePaddle_CXX11)
        list(APPEND PADDLEPADDLE_LINKER_LIBS horovod_cuda_kernels)
    else()
        list(APPEND PADDLEPADDLE_LINKER_LIBS compatible_horovod_cuda_kernels)
    endif()
endif()

set(PaddlePaddle_CXX11 ${PaddlePaddle_CXX11} PARENT_SCOPE)

# PaddlePaddle SOURCES
list(APPEND PADDLEPADDLE_SOURCES "${PROJECT_SOURCE_DIR}/horovod/paddlepaddle/handle_manager.cc"
                            "${PROJECT_SOURCE_DIR}/horovod/paddlepaddle/ready_event.cc"
                            "${PROJECT_SOURCE_DIR}/horovod/paddlepaddle/cuda_util.cc"
                            "${PROJECT_SOURCE_DIR}/horovod/paddlepaddle/mpi_ops_v2.cc"
                            "${PROJECT_SOURCE_DIR}/horovod/paddlepaddle/adapter_v2.cc")

# Create library
set_output_dir()
add_library(${PADDLEPADDLE_TARGET_LIB} SHARED ${SOURCES} ${PADDLEPADDLE_SOURCES})
target_include_directories(${PADDLEPADDLE_TARGET_LIB} PRIVATE "${EIGEN_INCLUDE_PATH}")
target_include_directories(${PADDLEPADDLE_TARGET_LIB} PRIVATE "${FLATBUFFERS_INCLUDE_PATH}")
target_link_libraries(${PADDLEPADDLE_TARGET_LIB} ${LINKER_LIBS} ${PADDLEPADDLE_LINKER_LIBS})
set_target_properties(${PADDLEPADDLE_TARGET_LIB} PROPERTIES SUFFIX "${Python_SUFFIX}")
set_target_properties(${PADDLEPADDLE_TARGET_LIB} PROPERTIES PREFIX "")
set_target_properties(${PADDLEPADDLE_TARGET_LIB} PROPERTIES OUTPUT_NAME "mpi_lib_v2")
