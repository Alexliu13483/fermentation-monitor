import cv2
import numpy as np
import time
import subprocess
import json
from pathlib import Path

class FermentationAnalyzer:
    def __init__(self, cpp_executable_path="/opt/fermentation-monitor/bin/fermentation_monitor"):
        self.cpp_executable = cpp_executable_path
        self.reference_image_path = "/opt/fermentation-monitor/data/reference.jpg"
        self.current_image_path = "/opt/fermentation-monitor/data/current.jpg"
        
        # Create data directory if it doesn't exist
        Path("/opt/fermentation-monitor/data").mkdir(parents=True, exist_ok=True)
        
    def capture_reference_image(self):
        """Capture and save reference image for comparison"""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Failed to open camera")
            return False
            
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(self.reference_image_path, frame)
            cap.release()
            return True
        
        cap.release()
        return False
        
    def analyze(self):
        """Analyze current fermentation state"""
        try:
            # Capture current image
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print("Failed to open camera for analysis")
                return None
                
            ret, frame = cap.read()
            cap.release()
            
            if not ret:
                print("Failed to capture frame")
                return None
                
            # Save current frame
            cv2.imwrite(self.current_image_path, frame)
            
            # If no reference image exists, use current as reference
            if not Path(self.reference_image_path).exists():
                cv2.imwrite(self.reference_image_path, frame)
                
            # Use Python OpenCV for analysis (fallback if C++ not available)
            return self._analyze_with_python(frame)
            
        except Exception as e:
            print(f"Error in fermentation analysis: {e}")
            return None
            
    def _analyze_with_python(self, current_frame):
        """Python-based image analysis"""
        try:
            reference = cv2.imread(self.reference_image_path)
            if reference is None:
                return {
                    'volume_change': 0.0,
                    'surface_activity': 0.0,
                    'bubble_count': 0,
                    'texture_variance': self._calculate_texture_variance(current_frame),
                    'timestamp': int(time.time())
                }
                
            # Calculate metrics
            volume_change = self._calculate_volume_change(current_frame, reference)
            bubble_count = self._detect_bubbles(current_frame)
            texture_variance = self._calculate_texture_variance(current_frame)
            surface_activity = self._calculate_surface_activity(current_frame, reference)
            
            return {
                'volume_change': volume_change,
                'surface_activity': surface_activity,
                'bubble_count': bubble_count,
                'texture_variance': texture_variance,
                'timestamp': int(time.time())
            }
            
        except Exception as e:
            print(f"Error in Python image analysis: {e}")
            return None
            
    def _calculate_volume_change(self, current, reference):
        gray_current = cv2.cvtColor(current, cv2.COLOR_BGR2GRAY)
        gray_reference = cv2.cvtColor(reference, cv2.COLOR_BGR2GRAY)
        
        diff = cv2.absdiff(gray_current, gray_reference)
        return np.sum(diff) / (current.shape[0] * current.shape[1])
        
    def _detect_bubbles(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (9, 9), 2)
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        bubble_count = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            if 10 < area < 1000:
                bubble_count += 1
                
        return bubble_count
        
    def _calculate_texture_variance(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return np.var(gray)
        
    def _calculate_surface_activity(self, current, reference):
        diff = cv2.absdiff(current, reference)
        mean_diff = np.mean(diff)
        return float(mean_diff)