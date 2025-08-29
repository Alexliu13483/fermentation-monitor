#pragma once

#include <string>

class Camera {
public:
    Camera();
    ~Camera();
    
    bool open(int camera_id = 0);
    void close();
    bool is_open() const;
    
    // Capture image data - returns raw data size
    int capture(unsigned char* buffer, int buffer_size, int& width, int& height);
    
private:
    bool m_is_open;
    int m_camera_id;
};