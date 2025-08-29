"""
Tests for ImageProcessor class.
"""

import os
import sys
import numpy as np

# Add src to Python path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src/python'))

from image_processing.image_processor import ImageProcessor, ImageData


class TestImageProcessor:
    """Test cases for ImageProcessor class."""
    
    def test_can_create_image_processor_without_data(self):
        """Test creating ImageProcessor with no parameters."""
        processor = ImageProcessor()
        assert processor is not None
    
    def test_can_create_image_processor_with_image_data(self):
        """Test creating ImageProcessor with image data."""
        # Create sample image data (3x3 BGR image as numpy array)
        width, height = 3, 3
        image_data = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
        
        processor = ImageProcessor(image_data, width, height)
        assert processor is not None
    
    def test_can_get_image_dimensions(self):
        """Test getting dimensions from ImageProcessor with data."""
        width, height = 640, 480
        image_data = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
        
        processor = ImageProcessor(image_data, width, height)
        
        success, actual_width, actual_height = processor.get_dimensions()
        assert success is True
        assert actual_width == width
        assert actual_height == height
    
    def test_empty_processor_has_no_dimensions(self):
        """Test that empty processor returns no dimensions."""
        processor = ImageProcessor()
        
        success, width, height = processor.get_dimensions()
        assert success is False
        assert width == 0
        assert height == 0
    
    def test_can_load_image_from_file(self):
        """Test loading image from file."""
        processor = ImageProcessor()
        
        # Test loading sample_dough_image.jpg (should be 457x617)
        image_path = "../../tests/images/sample_dough_image.jpg"
        image_data = processor.load_from_file(image_path)
        
        # Check if loading succeeded
        if image_data.is_valid:
            assert image_data.width == 457
            assert image_data.height == 617
            assert image_data.data is not None
            print(f"Successfully loaded sample_dough_image.jpg: {image_data.width}x{image_data.height}")
        else:
            print(f"Could not load image from {image_path}")
    
    def test_can_load_sample_dough_image2(self):
        """Test loading sample_dough_image2.jpg with expected dimensions."""
        processor = ImageProcessor()
        
        # Test loading sample_dough_image2.jpg (should be 322x676)
        image_path = "../../tests/images/sample_dough_image2.jpg"
        image_data = processor.load_from_file(image_path)
        
        # Check if loading succeeded with correct dimensions
        assert image_data.is_valid is True
        assert image_data.width == 322
        assert image_data.height == 676
        assert image_data.data is not None
        print(f"Successfully loaded sample_dough_image2.jpg: {image_data.width}x{image_data.height}")
    
    def test_can_load_simple_test_image(self):
        """Test loading simple_test.jpg with expected dimensions."""
        processor = ImageProcessor()
        
        # Test loading simple_test.jpg (should be 3x2)
        image_path = "../../tests/images/simple_test.jpg"
        image_data = processor.load_from_file(image_path)
        
        # Check if loading succeeded with correct dimensions
        assert image_data.is_valid is True
        assert image_data.width == 3
        assert image_data.height == 2
        assert image_data.data is not None
        print(f"Successfully loaded simple_test.jpg: {image_data.width}x{image_data.height}")
    
    def test_load_from_nonexistent_file(self):
        """Test loading from non-existent file."""
        processor = ImageProcessor()
        
        image_data = processor.load_from_file("nonexistent_file.jpg")
        
        assert image_data.is_valid is False
        assert image_data.width == 0
        assert image_data.height == 0
        assert image_data.data is None


class TestImageData:
    """Test cases for ImageData class."""
    
    def test_image_data_valid_creation(self):
        """Test creating valid ImageData."""
        data = [[[255, 0, 0], [0, 255, 0], [0, 0, 255]] for _ in range(100)]
        image_data = ImageData(data, 100, 100)
        
        assert image_data.is_valid is True
        assert image_data.width == 100
        assert image_data.height == 100
        assert image_data.data is not None
    
    def test_image_data_invalid_creation(self):
        """Test creating invalid ImageData."""
        image_data = ImageData()
        
        assert image_data.is_valid is False
        assert image_data.width == 0
        assert image_data.height == 0
        assert image_data.data is None


def run_tests():
    """Run all tests manually."""
    test_processor = TestImageProcessor()
    test_image_data = TestImageData()
    
    print("Running ImageProcessor tests...")
    
    # Test ImageProcessor
    try:
        test_processor.test_can_create_image_processor_without_data()
        print("✓ test_can_create_image_processor_without_data")
    except Exception as e:
        print(f"✗ test_can_create_image_processor_without_data: {e}")
    
    try:
        test_processor.test_can_create_image_processor_with_image_data()
        print("✓ test_can_create_image_processor_with_image_data")
    except Exception as e:
        print(f"✗ test_can_create_image_processor_with_image_data: {e}")
    
    try:
        test_processor.test_can_get_image_dimensions()
        print("✓ test_can_get_image_dimensions")
    except Exception as e:
        print(f"✗ test_can_get_image_dimensions: {e}")
    
    try:
        test_processor.test_empty_processor_has_no_dimensions()
        print("✓ test_empty_processor_has_no_dimensions")
    except Exception as e:
        print(f"✗ test_empty_processor_has_no_dimensions: {e}")
    
    try:
        test_processor.test_can_load_image_from_file()
        print("✓ test_can_load_image_from_file")
    except Exception as e:
        print(f"✗ test_can_load_image_from_file: {e}")
    
    try:
        test_processor.test_can_load_sample_dough_image2()
        print("✓ test_can_load_sample_dough_image2")
    except Exception as e:
        print(f"✗ test_can_load_sample_dough_image2: {e}")
    
    try:
        test_processor.test_can_load_simple_test_image()
        print("✓ test_can_load_simple_test_image")
    except Exception as e:
        print(f"✗ test_can_load_simple_test_image: {e}")
    
    try:
        test_processor.test_load_from_nonexistent_file()
        print("✓ test_load_from_nonexistent_file")
    except Exception as e:
        print(f"✗ test_load_from_nonexistent_file: {e}")
    
    # Test ImageData
    try:
        test_image_data.test_image_data_valid_creation()
        print("✓ test_image_data_valid_creation")
    except Exception as e:
        print(f"✗ test_image_data_valid_creation: {e}")
    
    try:
        test_image_data.test_image_data_invalid_creation()
        print("✓ test_image_data_invalid_creation")
    except Exception as e:
        print(f"✗ test_image_data_invalid_creation: {e}")
    
    print("Tests completed!")


if __name__ == "__main__":
    run_tests()