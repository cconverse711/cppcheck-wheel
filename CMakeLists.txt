cmake_minimum_required(VERSION 3.16...4.0)
project(${SKBUILD_PROJECT_NAME} VERSION ${SKBUILD_PROJECT_VERSION})

message(STATUS "cppcheck-wheel version: ${SKBUILD_PROJECT_VERSION}")
string(REGEX MATCH "^([0-9]+)\.([0-9]+)\.([0-9]+)" CPPCHECK_VERSION "${SKBUILD_PROJECT_VERSION}")
message(STATUS "cppcheck version: ${CPPCHECK_VERSION}")

# Define a build rule for cppcheck
set(CPPCHECK_DOWNLOAD_URL "https://github.com/danmar/cppcheck/archive/refs/tags/${CPPCHECK_VERSION}.tar.gz")
include(ExternalProject)
ExternalProject_add(build-cppcheck
  URL "${CPPCHECK_DOWNLOAD_URL}"
  SOURCE_DIR ${CMAKE_BINARY_DIR}/cppcheck
  BINARY_DIR ${CMAKE_BINARY_DIR}/cppcheck-build
  UPDATE_COMMAND ""
  INSTALL_COMMAND ""
  USES_TERMINAL_DOWNLOAD 1
  USES_TERMINAL_CONFIGURE 1
  USES_TERMINAL_BUILD 1
  CMAKE_ARGS -DCMAKE_BUILD_TYPE=Release -DCMAKE_POLICY_VERSION_MINIMUM=3.5
  BUILD_COMMAND ${CMAKE_COMMAND} --build . --target cppcheck --config Release
)
set(config-subfolder "")
if(CMAKE_GENERATOR MATCHES "Visual Studio")
  set(config-subfolder "Release")
endif()
set(cppcheck-executable ${CMAKE_BINARY_DIR}/cppcheck-build/${config-subfolder}/bin/cppcheck${CMAKE_EXECUTABLE_SUFFIX})

# Reduce the size of the executable by executing strip if it is present on the system
find_program(STRIP_EXECUTABLE strip)
if(STRIP_EXECUTABLE)
  add_custom_target(
    strip-cppcheck
    ALL
    COMMAND ${STRIP_EXECUTABLE} ${cppcheck-executable}
    COMMENT "Stripping cppcheck executable for size reduction"
  )
  add_dependencies(strip-cppcheck build-cppcheck)
endif()

# Define an installation rule that copies the executable to our Python package
install(
  PROGRAMS
  ${cppcheck-executable}
  ${CMAKE_BINARY_DIR}/cppcheck/htmlreport/cppcheck-htmlreport
  DESTINATION cppcheck/data/bin
)

install(DIRECTORY
  ${CMAKE_BINARY_DIR}/cppcheck/addons
  DESTINATION cppcheck/data
  FILES_MATCHING PATTERN "*.py"
  PATTERN "test" EXCLUDE
)

install(DIRECTORY
  ${CMAKE_BINARY_DIR}/cppcheck/cfg
  DESTINATION cppcheck/data
  FILES_MATCHING PATTERN "*.cfg"
)

install(DIRECTORY
  ${CMAKE_BINARY_DIR}/cppcheck/platforms
  DESTINATION cppcheck/data
  FILES_MATCHING PATTERN "*.xml"
)

install(
  DIRECTORY
  ${CMAKE_BINARY_DIR}/cppcheck/
  DESTINATION cppcheck/source
)
