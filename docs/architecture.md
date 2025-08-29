# System Architecture Documentation

## Overview

The Fermentation Monitor system uses a layered architecture design focused on dough size monitoring using webcam-based image analysis, providing a complete monitoring solution with Python and OpenCV.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Web Interface                          │
│                   (HTML/CSS/JavaScript)                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                   Flask Web API                             │
│                    (Python)                                 │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                 Application Core                            │
│         ┌───────────────────────────────────────────────┐   │
│         │          Image Processing Engine             │   │
│         │           (Python & OpenCV)                  │   │
│         └───────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                 Data Storage                                │
│                  (SQLite)                                   │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                 Hardware Layer                              │
│                 ┌─────────────────┐                         │
│                 │     Camera      │                         │
│                 │  (USB/Built-in) │                         │
│                 └─────────────────┘                         │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Web Interface Layer (Presentation Layer)

**Technology Stack**: HTML5, CSS3, JavaScript, Bootstrap, Chart.js

**Responsibilities**:
- Provide user interface
- Data visualization
- Real-time status display
- System control interface

**File Structure**:
```
src/web/
├── templates/
│   ├── base.html           # Base template
│   ├── index.html          # Home page
│   └── dashboard.html      # Dashboard
├── static/
│   ├── css/
│   │   └── style.css       # Custom styles
│   └── js/
│       └── dashboard.js    # Frontend logic
```

### 2. API Layer

**Technology Stack**: Flask, Python 3.8+

**Responsibilities**:
- RESTful API provision
- Data serialization/deserialization
- Session management
- Error handling

**Main Endpoints**:
- `/api/current-status` - Real-time status
- `/api/image-metrics` - Image analysis results
- `/api/sessions` - Fermentation session management
- `/api/system/info` - System information

### 3. Application Core Layer

#### 3.1 Image Processing Engine

**Technology Stack**: Python 3.8+, OpenCV 4.x, NumPy

**Functions**:
- Dough size measurement
- Size change detection
- Contour analysis
- Confidence scoring
- Real-time webcam processing

**Class Design**:
```python
class FermentationAnalyzer:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        
    def analyze(self) -> dict:
        """Analyze current dough size from webcam"""
        pass
        
    def calculate_size(self, frame) -> float:
        """Calculate dough size from image frame"""
        pass
        
    def detect_contours(self, frame) -> list:
        """Detect dough contours in frame"""
        pass
```

**Core Algorithms**:
- Dough contour detection using edge detection
- Size calculation based on contour area
- Change tracking over time
- Confidence assessment

### 4. Data Access Layer

**Technology Stack**: SQLite 3, Python sqlite3

**Database Schema**:
```sql
-- Image analysis results
image_metrics (
    id, 
    timestamp, 
    dough_size, 
    size_change, 
    contour_area, 
    detection_confidence,
    image_path
)

-- Fermentation sessions
fermentation_sessions (
    id, 
    name, 
    start_time, 
    end_time, 
    status, 
    notes
)

-- System configuration
system_config (
    key, 
    value, 
    updated_at
)
```

### 5. Hardware Abstraction Layer

**Camera Interface**:
- OpenCV VideoCapture API
- Cross-platform camera support (Windows, Linux, macOS)
- USB camera and built-in camera support
- Configurable resolution and frame rate

**Hardware Requirements**:
- Any USB webcam or built-in camera
- Minimum 640x480 resolution recommended
- USB 2.0 or higher for stable video stream

## Communication Protocols

### 1. Internal Communication

**Thread Communication**:
- Python threading module
- Queue objects for thread-safe data exchange
- Event synchronization for coordinated operations

**Process Communication**:
- Shared memory for image data
- File-based configuration sharing
- Database-mediated data exchange

### 2. External Communication

**Web API**:
- HTTP/1.1 protocol
- JSON data format
- RESTful design principles
- WebSocket for real-time updates

**Hardware Communication**:
- USB protocol for camera communication
- Standard video capture interfaces (V4L2 on Linux, DirectShow on Windows)

## Data Flow

### 1. Image Analysis Data Flow

```
Camera → OpenCV Capture → Image Processing → Size Analysis → Database → Web API → Frontend
```

### 2. Control Flow

```
Frontend → Web API → Python Core → Image Analysis Control
```

### 3. Real-time Updates

```
Image Analysis → WebSocket → Frontend Dashboard (Live Updates)
```

## Performance Considerations

### 1. Python-Based Architecture

**Python Processing**:
- Business logic and API services
- System coordination
- Database operations
- Web interface serving

**OpenCV Optimization**:
- Efficient image processing with NumPy arrays
- Optimized computer vision algorithms
- Memory-efficient operations

### 2. Memory Management

- OpenCV frame object reuse
- Python garbage collection optimization
- Database connection pooling
- Efficient image buffer handling

### 3. Concurrent Processing

- Multi-threaded design
- Non-blocking I/O operations
- Background image analysis
- Asynchronous web requests

## Security Design

### 1. Data Protection

- SQLite database file permission control
- Secure data storage practices
- Optional HTTPS for network transmission
- Input validation and sanitization

### 2. System Security

- Principle of least privilege
- Input validation for all API endpoints
- Error message filtering to prevent information disclosure
- Rate limiting to prevent abuse

### 3. Camera Security

- Camera access permission management
- Secure image storage and cleanup
- Privacy considerations for image data

## Extensibility Design

### 1. Modular Architecture

- Plugin-style image analysis algorithms
- Configurable system behavior
- Modular component design for easy extension

### 2. API Versioning

- RESTful API versioning strategy
- Backward compatibility support
- Progressive feature deployment

### 3. Hardware Abstraction

- Universal camera interface
- Platform-independent design
- Support for multiple camera types and resolutions

## Deployment Architecture

### 1. Development Environment

- Local development on Windows, macOS, or Linux
- Python virtual environment isolation
- Cross-platform compatibility

### 2. Production Environment

- Any system with Python 3.8+ and camera support
- Raspberry Pi 4 for embedded deployment
- Docker containerization support (optional)
- Systemd service management for Linux

### 3. Build Process

- Python package management with pip
- Virtual environment for dependency isolation
- Simple deployment scripts

## Monitoring and Maintenance

### 1. Logging System

- Python logging module integration
- Structured logging with different levels
- Log rotation and management
- Console and file output options

### 2. Health Checks

- Camera status monitoring
- Service availability checks
- Automatic error recovery
- System resource monitoring

### 3. Performance Monitoring

- System resource utilization
- API response times
- Database performance metrics
- Image processing performance tracking