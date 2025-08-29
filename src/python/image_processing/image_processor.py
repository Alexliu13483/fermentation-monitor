"""
ImageProcessor class for fermentation monitoring.
Handles image loading and processing.
"""

from typing import Optional, Tuple
import os
import cv2
import numpy as np


class ImageData:
    """Structure to hold image data and metadata."""
    
    def __init__(self, data: Optional[np.ndarray] = None, width: int = 0, height: int = 0):
        self.data = data
        self.width = width
        self.height = height
        self.is_valid = data is not None and width > 0 and height > 0


class ImageProcessor:
    """
    Image processor for fermentation monitoring.
    
    Handles loading images from files and basic image processing operations.
    """
    
    def __init__(self, image_data: Optional[np.ndarray] = None, width: int = 0, height: int = 0):
        """
        Initialize ImageProcessor.
        
        Args:
            image_data: Optional numpy array containing image data
            width: Image width in pixels
            height: Image height in pixels
        """
        self._image_data = image_data
        self._width = width
        self._height = height
    
    def load_from_file(self, file_path: str) -> ImageData:
        """
        Load image from file using OpenCV.
        
        Args:
            file_path: Path to the image file
            
        Returns:
            ImageData object containing image data and metadata
        """
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return ImageData()  # Return invalid ImageData
            
            # Load image using OpenCV
            image_data = cv2.imread(file_path)
            
            if image_data is None:
                print(f"Could not load image from {file_path}")
                return ImageData()  # Return invalid ImageData
            
            # Get image dimensions
            height, width = image_data.shape[:2]
            
            # Update internal state
            self._image_data = image_data
            self._width = width
            self._height = height
            
            return ImageData(image_data, width, height)
            
        except Exception as e:
            print(f"Error loading image from {file_path}: {e}")
            return ImageData()  # Return invalid ImageData
    
    def get_dimensions(self) -> Tuple[bool, int, int]:
        """
        Get image dimensions.
        
        Returns:
            Tuple of (success, width, height)
        """
        if self._image_data is None:
            return False, 0, 0
        
        return True, self._width, self._height