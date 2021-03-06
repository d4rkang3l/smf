# packaging
include(CMake/git_version.cmake)
set(INSTALL_LIB_DIR lib CACHE PATH "Installation directory for libraries")
set(INSTALL_BIN_DIR bin CACHE PATH "Installation directory for executables")
set(INSTALL_INCLUDE_DIR include CACHE PATH
  "Installation directory for header files")

set(CPACK_SET_DESTDIR ON)
set(CPACK_PACKAGE_VENDOR  "Alexander Gallego")
set(CPACK_PACKAGE_CONTACT "gallego.alexx@gmail.com")
set(CPACK_PACKAGE_VERSION "${SMF_VERSION}")
set(CPACK_STRIP_FILES "ON")
set(CPACK_PACKAGE_NAME "smf")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "Fastest durable log broker on the west")

#deb
set(CPACK_DEB_COMPONENT_INSTALL TRUE)
set(CPACK_DEBIAN_PACKAGE_SECTION "utilities")
set(CPACK_DEBIAN_PACKAGE_HOMEPAGE "http://senior7515.github.io/smf/")

#rpm
set(CPACK_RPM_PACKAGE_LICENSE "Apache 2.0")
set(CPACK_RPM_PACKAGE_GROUP "utilities")
set(CPACK_RPM_PACKAGE_URL "http://senior7515.github.io/smf/")
set(CPACK_RPM_PACKAGE_AUTOREQ YES)
set(CPACK_RPM_PACKAGE_DEBUG YES)

if(X86)
  set(CPACK_DEBIAN_ARCHITECTURE "i386")
  set(CPACK_RPM_PACKAGE_ARCHITECTURE "i686")
elseif(X86_64)
  set(CPACK_DEBIAN_ARCHITECTURE "amd64")
  set(CPACK_RPM_PACKAGE_ARCHITECTURE "x86_64")
else()
  set(CPACK_DEBIAN_ARCHITECTURE ${CMAKE_SYSTEM_PROCESSOR})
  set(CPACK_RPM_PACKAGE_ARCHITECTURE ${CMAKE_SYSTEM_PROCESSOR})
endif()

if(CPACK_GENERATOR STREQUAL "DEB")
  set(SMF_PACKAGE_ARCH_SUFFIX ${CPACK_DEBIAN_PACKAGE_ARCHITECTURE})
elseif(CPACK_GENERATOR STREQUAL "RPM")
  set(SMF_PACKAGE_ARCH_SUFFIX ${CPACK_RPM_PACKAGE_ARCHITECTURE})
else()
  set(SMF_PACKAGE_ARCH_SUFFIX ${CMAKE_SYSTEM_PROCESSOR})
endif()

set(CPACK_PACKAGE_FILE_NAME
  "${CMAKE_PROJECT_NAME}-${GIT_VERSION}-${SMF_PACKAGE_ARCH_SUFFIX}")
set(CPACK_SOURCE_PACKAGE_FILE_NAME
  "${CMAKE_PROJECT_NAME}-${GIT_VERSION}-${SMF_PACKAGE_ARCH_SUFFIX}")

# must be last
include(CPack)
