# Try to find Paddle
#
# The following are set after configuration is done:
#  PaddlePaddle_FOUND
#  PaddlePaddle_INCLUDE_DIRS
#  PaddlePaddle_LIBRARY_DIRS
#  PaddlePaddle_LIBRARIES
#  PaddlePaddle_COMPILE_FLAGS
#  PaddlePaddle_VERSION
#  PaddlePaddle_CUDA
#  PaddlePaddle_ROCM
#  PaddlePaddle_CXX11

# Compatible layer for CMake <3.12. PaddlePaddle_ROOT will be accounted in for searching paths and libraries for CMake >=3.12.
list(APPEND CMAKE_PREFIX_PATH ${PaddlePaddle_ROOT})


execute_process(COMMAND ${PY_EXE} -c "import paddle; print(paddle.__version__); print(paddle.sysconfig.get_include()); print(paddle.sysconfig.get_lib()); print(paddle.device.is_compiled_with_cuda())"
                OUTPUT_VARIABLE PaddlePaddle_OUTPUT OUTPUT_STRIP_TRAILING_WHITESPACE ERROR_QUIET)
string(REGEX REPLACE "\n" ";" PaddlePaddle_OUTPUT "${PaddlePaddle_OUTPUT}")
list(LENGTH PaddlePaddle_OUTPUT LEN)
if (LEN EQUAL "3")
    list(GET PaddlePaddle_OUTPUT 0 PaddlePaddle_VERSION)
    list(GET PaddlePaddle_OUTPUT 1 PaddlePaddle_INCLUDE_DIRS)
    list(GET PaddlePaddle_OUTPUT 2 PaddlePaddle_LIBRARIES)
    string(REPLACE " " ";" PaddlePaddle_LIBRARIES "${PaddlePaddle_LIBRARIES}")
    list(GET PaddlePaddle_OUTPUT 3 PaddlePaddle_CUDA)
    set(PaddlePaddle_CXX11 TRUE)
endif()
include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(PaddlePaddle REQUIRED_VARS PaddlePaddle_LIBRARIES VERSION_VAR PaddlePaddle_VERSION)
if (PaddlePaddle_CXX11)
    set(PaddlePaddle_COMPILE_FLAGS " -D_GLIBCXX_USE_CXX11_ABI=1")
else()
    set(PaddlePaddle_COMPILE_FLAGS " -D_GLIBCXX_USE_CXX11_ABI=0")
endif()

mark_as_advanced(PaddlePaddle_INCLUDE_DIRS PaddlePaddle_LIBRARIES PaddlePaddle_COMPILE_FLAGS PaddlePaddle_VERSION PaddlePaddle_CUDA PaddlePaddle_CXX11)