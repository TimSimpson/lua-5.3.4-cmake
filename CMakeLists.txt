project(Lua-5.3.4 C CXX)
cmake_minimum_required(VERSION 3.2 FATAL_ERROR)

add_library(lua
    ${CMAKE_CURRENT_SOURCE_DIR}/include/lua.h
    ${CMAKE_CURRENT_SOURCE_DIR}/include/lua.hpp
    ${CMAKE_CURRENT_SOURCE_DIR}/include/luaconf.h

    ${CMAKE_CURRENT_SOURCE_DIR}/src/lapi.c
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lapi.h
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lauxlib.c
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lauxlib.h
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lbaselib.c
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lbitlib.c
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lcode.c
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lcode.h
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lcorolib.c
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lctype.c
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lctype.h
    ${CMAKE_CURRENT_SOURCE_DIR}/src/ldblib.c
    ${CMAKE_CURRENT_SOURCE_DIR}/src/ldebug.c
    ${CMAKE_CURRENT_SOURCE_DIR}/src/ldebug.h
    ${CMAKE_CURRENT_SOURCE_DIR}/src/ldo.c
    ${CMAKE_CURRENT_SOURCE_DIR}/src/ldo.h
    ${CMAKE_CURRENT_SOURCE_DIR}/src/ldump.c
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lfunc.c
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lfunc.h
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lgc.c
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lgc.h
    ${CMAKE_CURRENT_SOURCE_DIR}/src/linit.c
    ${CMAKE_CURRENT_SOURCE_DIR}/src/liolib.c
    ${CMAKE_CURRENT_SOURCE_DIR}/src/llex.c
    ${CMAKE_CURRENT_SOURCE_DIR}/src/llex.h
    ${CMAKE_CURRENT_SOURCE_DIR}/src/llimits.h
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lmathlib.c
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lmem.c
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lmem.h
    ${CMAKE_CURRENT_SOURCE_DIR}/src/loadlib.c
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lobject.c
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lobject.h
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lopcodes.c
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lopcodes.h
    ${CMAKE_CURRENT_SOURCE_DIR}/src/loslib.c
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lparser.c
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lparser.h
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lprefix.h
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lstate.c
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lstate.h
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lstring.c
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lstring.h
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lstrlib.c
    ${CMAKE_CURRENT_SOURCE_DIR}/src/ltable.c
    ${CMAKE_CURRENT_SOURCE_DIR}/src/ltable.h
    ${CMAKE_CURRENT_SOURCE_DIR}/src/ltablib.c
    ${CMAKE_CURRENT_SOURCE_DIR}/src/ltm.c
    ${CMAKE_CURRENT_SOURCE_DIR}/src/ltm.h
    ${CMAKE_CURRENT_SOURCE_DIR}/src/luac.c
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lualib.h
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lundump.c
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lundump.h
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lutf8lib.c
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lvm.c
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lvm.h
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lzio.c
    ${CMAKE_CURRENT_SOURCE_DIR}/src/lzio.h
)

if (BUILD_SHARED_LIBS)
    target_compile_definitions(lua
        PUBLIC
            LUA_BUILD_AS_DLL=1
    )
endif()

target_include_directories(lua
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>
    PRIVATE
        $<INSTALL_INTERFACE:src>
)

install(TARGETS lua EXPORT lua_config
    ARCHIVE  DESTINATION lib
    LIBRARY  DESTINATION lib
    RUNTIME  DESTINATION bin)
install(DIRECTORY include/ DESTINATION include)

install(EXPORT lua_config DESTINATION share/lua/cmake)

export(TARGETS lua FILE lua_config.cmake)

# Probably missing something obvious but it seems like luac requires
# non-exported functions to compile correctly.
if (NOT BUILD_SHARED_LIBS)
    add_executable(luac ${CMAKE_CURRENT_SOURCE_DIR}/src/luac.c)
    target_link_libraries(luac lua)
endif()

add_executable(lua_interpretter ${CMAKE_CURRENT_SOURCE_DIR}/src/lua.c)
target_link_libraries(lua_interpretter lua)
set_property(TARGET lua_interpretter PROPERTY OUTPUT_NAME "lua")
