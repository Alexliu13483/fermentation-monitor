cmake_minimum_required(VERSION 3.16)
project(fermentation_monitor_cpp)

set(CMAKE_CXX_STANDARD 17)

# Find packages
find_package(OpenCV REQUIRED)
find_package(PkgConfig REQUIRED)

# Include directories
include_directories(include)
include_directories(${OpenCV_INCLUDE_DIRS})

# Source files
set(SOURCES
    src/image_processor.cpp
    src/sensor_interface.cpp
    src/fermentation_analyzer.cpp
    src/main.cpp
)

# Create executable
add_executable(fermentation_monitor ${SOURCES})

# Link libraries
target_link_libraries(fermentation_monitor ${OpenCV_LIBS})

# Install target
install(TARGETS fermentation_monitor DESTINATION /opt/fermentation-monitor/bin)