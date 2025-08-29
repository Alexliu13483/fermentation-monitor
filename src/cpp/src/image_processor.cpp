#include "image_processor.hpp"
#include <chrono>
#include <iostream>

ImageProcessor::ImageProcessor() {
}

ImageProcessor::~ImageProcessor() {
    if (camera.isOpened()) {
        camera.release();
    }
}

bool ImageProcessor::initialize_camera(int camera_id) {
    camera.open(camera_id);
    if (!camera.isOpened()) {
        std::cerr << "Failed to open camera " << camera_id << std::endl;
        return false;
    }
    
    camera.set(cv::CAP_PROP_FRAME_WIDTH, 1920);
    camera.set(cv::CAP_PROP_FRAME_HEIGHT, 1080);
    camera.set(cv::CAP_PROP_FPS, 30);
    
    return true;
}

cv::Mat ImageProcessor::capture_frame() {
    cv::Mat frame;
    camera >> frame;
    return frame;
}

FermentationMetrics ImageProcessor::analyze_fermentation(const cv::Mat& current_frame, const cv::Mat& reference_frame) {
    FermentationMetrics metrics;
    
    auto now = std::chrono::system_clock::now();
    metrics.timestamp = std::chrono::duration_cast<std::chrono::seconds>(now.time_since_epoch()).count();
    
    if (reference_frame.empty()) {
        metrics.volume_change = 0.0;
        metrics.surface_activity = 0.0;
        metrics.bubble_count = 0.0;
        metrics.texture_variance = calculate_texture_variance(current_frame);
        return metrics;
    }
    
    metrics.volume_change = calculate_volume_change(current_frame, reference_frame);
    metrics.bubble_count = detect_bubbles(current_frame);
    metrics.texture_variance = calculate_texture_variance(current_frame);
    
    cv::Mat diff;
    cv::absdiff(current_frame, reference_frame, diff);
    cv::Scalar mean_diff = cv::mean(diff);
    metrics.surface_activity = (mean_diff[0] + mean_diff[1] + mean_diff[2]) / 3.0;
    
    return metrics;
}

double ImageProcessor::calculate_volume_change(const cv::Mat& current, const cv::Mat& reference) {
    cv::Mat gray_current, gray_reference;
    cv::cvtColor(current, gray_current, cv::COLOR_BGR2GRAY);
    cv::cvtColor(reference, gray_reference, cv::COLOR_BGR2GRAY);
    
    cv::Mat diff;
    cv::absdiff(gray_current, gray_reference, diff);
    
    return cv::sum(diff)[0] / (current.rows * current.cols);
}

int ImageProcessor::detect_bubbles(const cv::Mat& image) {
    cv::Mat gray, blurred, thresh;
    cv::cvtColor(image, gray, cv::COLOR_BGR2GRAY);
    cv::GaussianBlur(gray, blurred, cv::Size(9, 9), 2);
    cv::threshold(blurred, thresh, 0, 255, cv::THRESH_BINARY + cv::THRESH_OTSU);
    
    std::vector<std::vector<cv::Point>> contours;
    cv::findContours(thresh, contours, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE);
    
    int bubble_count = 0;
    for (const auto& contour : contours) {
        double area = cv::contourArea(contour);
        if (area > 10 && area < 1000) {
            bubble_count++;
        }
    }
    
    return bubble_count;
}

double ImageProcessor::calculate_texture_variance(const cv::Mat& image) {
    cv::Mat gray;
    cv::cvtColor(image, gray, cv::COLOR_BGR2GRAY);
    
    cv::Scalar mean, stddev;
    cv::meanStdDev(gray, mean, stddev);
    
    return stddev[0] * stddev[0];
}

bool ImageProcessor::save_image(const cv::Mat& image, const std::string& filename) {
    return cv::imwrite(filename, image);
}