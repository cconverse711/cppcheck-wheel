cmake_minimum_required(VERSION 3.28...4.0)
project(${SKBUILD_PROJECT_NAME} VERSION ${SKBUILD_PROJECT_VERSION})

message(STATUS "cppcheck-wheel version: ${SKBUILD_PROJECT_VERSION}")
string(
    REGEX MATCH "^([0-9]+)\.([0-9]+)\.([0-9]+)"
    CPPCHECK_VERSION
    "${SKBUILD_PROJECT_VERSION}"
)
message(STATUS "cppcheck version: ${CPPCHECK_VERSION}")

# Check if the current compiler/linker toolchain supports IPO
include(CheckIPOSupported)
check_ipo_supported(RESULT ipo_supported OUTPUT ipo_error)

if(ipo_supported)
    set(CMAKE_INTERPROCEDURAL_OPTIMIZATION TRUE)
    message(STATUS "IPO/LTO enabled")
else()
    message(WARNING "IPO/LTO not supported: ${ipo_error}")
endif()

# Check for the execinfo header, needed for backtraces support.
include(CheckIncludeFileCXX)
check_include_file_cxx("execinfo.h" HAVE_EXECINFO_H)

# Values cppcheck's own CMakeLists.txt will pick up as already-set variables
# (equivalent to the old -DFOO=... CMAKE_ARGS passed to the nested build).
if(NOT HAVE_EXECINFO_H)
    message(STATUS "execinfo.h not found, disabling backtrace support")
    set(NO_UNIX_BACKTRACE_SUPPORT ON)
endif()

set(CMAKE_POLICY_VERSION_MINIMUM 3.5)
set(DISABLE_DMAKE ON)
set(FILESDIR "" CACHE STRING "" FORCE)

set(CPPCHECK_ARCHIVE
    "${CMAKE_CURRENT_SOURCE_DIR}/third_party/cppcheck-${CPPCHECK_VERSION}.tar.gz"
)
if(NOT EXISTS "${CPPCHECK_ARCHIVE}")
    message(
        FATAL_ERROR
        "${CPPCHECK_ARCHIVE} not found; run scripts/vendor_cppcheck.py "
        "(the PEP 517 backend wrapper normally does this for you)"
    )
endif()

include(FetchContent)
FetchContent_Declare(cppcheck URL "${CPPCHECK_ARCHIVE}" EXCLUDE_FROM_ALL)
FetchContent_MakeAvailable(cppcheck)

# Force the cppcheck target to build even though its subdirectory is
# EXCLUDE_FROM_ALL (mirrors the old build-cppcheck ExternalProject step).
add_custom_target(build-cppcheck ALL DEPENDS cppcheck)

# Reduce the size of the executable by executing strip if it is present on the system
find_program(STRIP_EXECUTABLE strip)
if(STRIP_EXECUTABLE)
    add_custom_target(
        strip-cppcheck
        ALL
        COMMAND ${STRIP_EXECUTABLE} $<TARGET_FILE:cppcheck>
        COMMENT "Stripping cppcheck executable for size reduction"
    )
    add_dependencies(strip-cppcheck build-cppcheck)
endif()

# Define an installation rule that copies the executable to our Python package
install(
    PROGRAMS
        $<TARGET_FILE:cppcheck>
        ${cppcheck_SOURCE_DIR}/htmlreport/cppcheck-htmlreport
    DESTINATION cppcheck/data
)

install(
    DIRECTORY ${cppcheck_SOURCE_DIR}/addons
    DESTINATION cppcheck/data
    FILES_MATCHING
    PATTERN "*.py"
    PATTERN "test" EXCLUDE
)

install(
    DIRECTORY ${cppcheck_SOURCE_DIR}/cfg
    DESTINATION cppcheck/data
    FILES_MATCHING
    PATTERN "*.cfg"
)

install(
    DIRECTORY ${cppcheck_SOURCE_DIR}/platforms
    DESTINATION cppcheck/data
    FILES_MATCHING
    PATTERN "*.xml"
)

install(
    FILES ${cppcheck_SOURCE_DIR}/COPYING
    DESTINATION cppcheck
    RENAME COPYING-cppcheck
)
