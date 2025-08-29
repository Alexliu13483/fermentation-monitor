#pragma once

#include <opencv2/opencv.hpp>
#include <string>
#include <vector>

struct FermentationMetrics {
    double volume_change;
    double surface_activity;
    double bubble_count;
    double texture_variance;
    uint64_t timestamp;
};

class ImageProcessor {
public:
    ImageProcessor();
    ~ImageProcessor();
    
    bool initialize_camera(int camera_id = 0);
    cv::Mat capture_frame();
    FermentationMetrics analyze_fermentation(const cv::Mat& current_frame, const cv::Mat& reference_frame);
    bool save_image(const cv::Mat& image, const std::string& filename);
    
private:
    cv::VideoCapture camera;
    cv::Mat reference_image;
    
    double calculate_volume_change(const cv::Mat& current, const cv::Mat& reference);
    int detect_bubbles(const cv::Mat& image);
    double calculate_texture_variance(const cv::Mat& image);
};