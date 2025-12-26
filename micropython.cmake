# micropython.cmake
# Create an interface library for our module
add_library(usermod_photopainter INTERFACE)

# Add source files to the library
target_sources(usermod_photopainter INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}/photopainter.c
    ${CMAKE_CURRENT_LIST_DIR}/EPD_7in3f.c
    ${CMAKE_CURRENT_LIST_DIR}/DEV_Config.c
)

# Add include directories
target_include_directories(usermod_photopainter INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}
)

# Link the library to the main usermod target
target_link_libraries(usermod INTERFACE usermod_photopainter)
