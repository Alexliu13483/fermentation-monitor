cmake_minimum_required(VERSION 3.16)
project(fermentation-monitor VERSION 1.0.0)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add compile flags
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra")
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -g -O0")
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3")

# Find packages
find_package(OpenCV REQUIRED)
find_package(PkgConfig REQUIRED)

# Include directories
include_directories(src/cpp/include)
include_directories(${OpenCV_INCLUDE_DIRS})

# Source files
set(SOURCES
    src/cpp/src/image_processor.cpp
    src/cpp/src/sensor_interface.cpp
    src/cpp/src/fermentation_analyzer.cpp
    src/cpp/src/main.cpp
)

# Create executable
add_executable(fermentation_monitor ${SOURCES})

# Link libraries
target_link_libraries(fermentation_monitor ${OpenCV_LIBS})

# Install targets
install(TARGETS fermentation_monitor
    RUNTIME DESTINATION bin
)

# Install Python application
install(DIRECTORY src/python/
    DESTINATION lib/fermentation-monitor/python
    FILES_MATCHING PATTERN "*.py"
    PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE
                GROUP_READ GROUP_EXECUTE
                WORLD_READ WORLD_EXECUTE
)

# Install web interface
install(DIRECTORY src/web/
    DESTINATION share/fermentation-monitor/web
)

# Install systemd service
install(FILES systemd/fermentation-monitor.service
    DESTINATION lib/systemd/system
)

# Install scripts
install(PROGRAMS 
    scripts/setup-dev.sh
    scripts/deploy.sh
    DESTINATION bin
)