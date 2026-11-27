# Define minimal required version of CMake.
cmake_minimum_required(VERSION "3.25")

# Project definition
project(
	aiml_soc_voice_control_light_blink_concurrent_efr32_micriumos
	VERSION 1.0
	LANGUAGES C CXX ASM
)

# Include the definition of the slc_aiml_soc_voice_control_light_blink_concurrent_efr32_micriumos target,
# which contains the content of the SLC project
include(aiml_soc_voice_control_light_blink_concurrent_efr32_micriumos.cmake)

add_executable(aiml_soc_voice_control_light_blink_concurrent_efr32_micriumos
    # Add additional sources here
)

target_include_directories(aiml_soc_voice_control_light_blink_concurrent_efr32_micriumos PUBLIC
    # Add additional include paths here
)

target_compile_definitions(aiml_soc_voice_control_light_blink_concurrent_efr32_micriumos PUBLIC
    # Add additional macros here
)

target_compile_options(aiml_soc_voice_control_light_blink_concurrent_efr32_micriumos PUBLIC
    # Set additional compiler flags here
)

target_link_options(aiml_soc_voice_control_light_blink_concurrent_efr32_micriumos PUBLIC
    # Set additional linker flags here
)

# Link with the content defined in the SLC project
target_link_libraries(aiml_soc_voice_control_light_blink_concurrent_efr32_micriumos PRIVATE
    slc
)

# Include managed project content if available
include(aiml_soc_voice_control_light_blink_concurrent_efr32_micriumos_project.cmake OPTIONAL RESULT_VARIABLE managed_project)
if(managed_project)
    message(STATUS "Using managed project content from ${managed_project}")
endif()

# Force the gcc linker command
set_target_properties(aiml_soc_voice_control_light_blink_concurrent_efr32_micriumos PROPERTIES LINKER_LANGUAGE C)

# Create .bin, .hex and .s37 artifacts after building the project
add_custom_command(TARGET aiml_soc_voice_control_light_blink_concurrent_efr32_micriumos
    POST_BUILD
    COMMAND ${CMAKE_OBJCOPY} ${OBJCOPY_SREC_CMD} "$<TARGET_FILE:aiml_soc_voice_control_light_blink_concurrent_efr32_micriumos>" "$<TARGET_FILE_DIR:aiml_soc_voice_control_light_blink_concurrent_efr32_micriumos>/$<TARGET_FILE_BASE_NAME:aiml_soc_voice_control_light_blink_concurrent_efr32_micriumos>.s37"
    COMMAND ${CMAKE_OBJCOPY} ${OBJCOPY_IHEX_CMD} "$<TARGET_FILE:aiml_soc_voice_control_light_blink_concurrent_efr32_micriumos>" "$<TARGET_FILE_DIR:aiml_soc_voice_control_light_blink_concurrent_efr32_micriumos>/$<TARGET_FILE_BASE_NAME:aiml_soc_voice_control_light_blink_concurrent_efr32_micriumos>.hex"
    COMMAND ${CMAKE_OBJCOPY} ${OBJCOPY_BIN_CMD}  "$<TARGET_FILE:aiml_soc_voice_control_light_blink_concurrent_efr32_micriumos>" "$<TARGET_FILE_DIR:aiml_soc_voice_control_light_blink_concurrent_efr32_micriumos>/$<TARGET_FILE_BASE_NAME:aiml_soc_voice_control_light_blink_concurrent_efr32_micriumos>.bin" 
)

# Run post-build pipeline to perform additional post-processing
if(post_build_command)
add_custom_command(TARGET aiml_soc_voice_control_light_blink_concurrent_efr32_micriumos
    POST_BUILD
    WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}/..
    COMMAND ${post_build_command}
)
endif()