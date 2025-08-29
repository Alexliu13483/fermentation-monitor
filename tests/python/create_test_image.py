#!/usr/bin/env python3
"""
Create a simple test image for testing purposes.
"""

import cv2
import numpy as np
import os

def create_test_images():
    """Create test images for the test suite."""
    
    # Create directory if it doesn't exist
    images_dir = "../images"
    os.makedirs(images_dir, exist_ok=True)
    
    # Create a simple test image for basic testing
    simple_image = np.array([
        [[255, 0, 0], [0, 255, 0], [0, 0, 255]],  # Red, Green, Blue
        [[255, 255, 0], [255, 255, 255], [0, 0, 0]]  # Yellow, White, Black
    ], dtype=np.uint8)
    
    cv2.imwrite(os.path.join(images_dir, "simple_test.jpg"), simple_image)
    print(f"Created simple_test.jpg: 3x2")


if __name__ == "__main__":
    create_test_images()
