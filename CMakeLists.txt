cmake_minimum_required(VERSION 3.22)
project(mean_calculator)

set(CMAKE_CXX_STANDARD 14)

include(FetchContent)
FetchContent_Declare(
    pybind11
    GIT_REPOSITORY https://github.com/pybind/pybind11.git
    GIT_TAG v2.10.0
)
FetchContent_MakeAvailable(pybind11)

pybind11_add_module(Q2_func MODULE Q2.cpp)