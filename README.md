# Fermentation Monitor

A webcam-based dough size monitoring system using OpenCV for image analysis and Flask for web interface.

## System Overview

This project provides a complete dough fermentation monitoring solution, including:

- **Real-time Monitoring**: Webcam-based dough size tracking
- **Image Analysis**: Uses OpenCV to analyze dough size changes and growth patterns
- **Web Interface**: Flask-based responsive web dashboard
- **Data Storage**: SQLite database for historical data
- **Cross-platform**: Works on development machines and can be deployed to embedded systems

## 系統架構

```
fermentation-monitor/
├── meta-fermentation-monitor/    # Yocto meta-layer
├── src/
│   ├── cpp/                     # C++ 影像處理核心
│   ├── python/                  # Python 應用程式
│   └── web/                     # Web 介面
├── scripts/                     # 建置和部署腳本
├── config/                      # 配置檔案
├── docs/                        # 文件
└── tests/                       # 測試程式
```

## Hardware Requirements

- **Camera**: USB webcam or built-in camera
- **Computer**: Any system capable of running Python and OpenCV (Windows, macOS, Linux)
- **Optional**: Raspberry Pi 4 for embedded deployment

## Software Dependencies

### System Requirements
- Python 3.8+
- OpenCV 4.x
- Flask 2.x
- SQLite 3

### Python Packages
- opencv-python>=4.5.0
- numpy>=1.21.0
- flask>=2.0.0
- Pillow>=8.0.0
- pytest>=6.0.0 (development)
- black>=21.0.0 (development)
- flake8>=3.9.0 (development)
- matplotlib>=3.3.0 (visualization)
- pandas>=1.3.0 (data analysis)
- scipy>=1.7.0 (advanced image processing)

## Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/Alexliu13483/fermentation-monitor.git
cd fermentation-monitor
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run the Application

```bash
cd src/python
python main.py
```

The web interface will be available at http://localhost:5000.

### 3. Connect a Webcam

Ensure you have a webcam connected and accessible by OpenCV. The system will automatically detect and use the default camera (usually camera index 0).

## Usage

### Web Interface Features

1. **Dashboard**: Real-time dough size monitoring and charts
2. **Image Analysis**: Live webcam feed with dough detection overlay
3. **Data History**: Historical data visualization and export

### API Endpoints

- `GET /api/current-status` - Get current system status
- `GET /api/image-metrics` - Get image analysis data
- `GET /api/sessions` - Get fermentation sessions list
- `POST /api/sessions` - Create new fermentation session

### Development Commands

```bash
# Run tests
pytest tests/python/

# Code formatting
black src/python/

# Code linting
flake8 src/python/

# Run with coverage
pytest tests/ --cov=src/python --cov-report=html
```

## Configuration

### Camera Configuration

The system automatically detects the default camera. To use a specific camera device, modify the camera index in the `FermentationAnalyzer` class:

```python
# In src/python/image_processing/fermentation_analyzer.py
self.camera = cv2.VideoCapture(0)  # Change 0 to your camera index
```

### Analysis Settings

Configure dough detection parameters by modifying the analysis thresholds in the image processing module.

## Development Guide

### Adding New Image Analysis Features

1. Edit `src/python/image_processing/fermentation_analyzer.py`
2. Implement new analysis functions
3. Update database schema if needed
4. Add corresponding API endpoints

### Web Interface Development

- Frontend: HTML/CSS/JavaScript (Bootstrap + Chart.js)
- Backend: Flask (Python)
- Templates: Jinja2

### Project Structure

```
src/
├── python/
│   ├── main.py                    # Main application entry point
│   ├── web_api/                   # Flask web API
│   │   └── app.py                 # Web application factory
│   ├── image_processing/          # Image analysis modules
│   │   └── fermentation_analyzer.py  # Dough size analysis
│   └── data_storage/              # Database management
│       └── database.py            # SQLite database operations
└── web/                           # Static web assets
    ├── static/                    # CSS, JS, images
    └── templates/                 # HTML templates
```

## Testing

```bash
# Run all Python tests
pytest tests/python/

# Run tests with coverage report
pytest tests/ --cov=src/python --cov-report=html

# Run specific test modules
pytest tests/python/test_fermentation_analyzer.py
```

## Deployment Options

### 1. Development Deployment
Local development and testing on any machine with Python and a webcam.

### 2. Production Deployment
Deploy to a dedicated system (Raspberry Pi, server, etc.) for continuous monitoring.

## Troubleshooting

### Common Issues

1. **Camera Access Failed**
   - Check camera connection and permissions
   - Verify camera is not being used by another application
   - Try different camera indices (0, 1, 2, etc.)

2. **Web Interface Not Accessible**
   - Check if Flask server is running on port 5000
   - Verify firewall settings allow access to port 5000
   - Check if the port is already in use

3. **Installation Issues**
   - Ensure Python 3.8+ is installed
   - Use virtual environment to avoid dependency conflicts
   - Check OpenCV installation: `python -c "import cv2; print(cv2.__version__)"`

### Logging

The application outputs status information to the console. For production deployment, consider redirecting output to log files.

## Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details.

## Author

Alex Liu - GitHub: [@Alexliu13483](https://github.com/Alexliu13483)

## Acknowledgments

- OpenCV community for computer vision tools
- Flask community for web framework
- Python community for excellent libraries