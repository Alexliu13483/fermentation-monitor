#include "camera.hpp"
#include <cstring>

Camera::Camera() : m_is_open(false), m_camera_id(-1) {
}

Camera::~Camera() {
    close();
}

bool Camera::open(int camera_id) {
    // Mock implementation: simulate USB camera on Raspberry Pi
    // Camera ID -1 always fails (for testing)
    if (camera_id < 0) {
        m_is_open = false;
        return false;
    }
    
    // Camera ID 0 (default) always succeeds
    m_camera_id = camera_id;
    m_is_open = true;
    return true;
}

void Camera::close() {
    m_is_open = false;
    m_camera_id = -1;
}

bool Camera::is_open() const {
    return m_is_open;
}

int Camera::capture(unsigned char* buffer, int buffer_size, int& width, int& height) {
    if (!m_is_open) {
        return -1; // Camera not open
    }
    
    // Mock capture: simulate loading sample_dough_image.jpg
    width = 640;
    height = 480;
    
    // Simulate minimal raw image data (3 bytes per pixel for RGB)
    int required_size = width * height * 3;
    
    if (buffer == nullptr || buffer_size < required_size) {
        return required_size; // Return required buffer size
    }
    
    // Fill buffer with mock image data
    for (int i = 0; i < required_size; i += 3) {
        // Simple pattern: alternate between light and dark pixels
        unsigned char value = ((i / 3) % 2 == 0) ? 200 : 100;
        buffer[i] = value;     // R
        buffer[i + 1] = value; // G  
        buffer[i + 2] = value; // B
    }
    
    return required_size;
}