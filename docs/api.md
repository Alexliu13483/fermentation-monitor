# API Documentation

The Fermentation Monitor provides RESTful API interfaces for real-time data access and system control focused on dough size monitoring.

## Basic Information

- **Base URL**: `http://[device-ip]:5000/api`
- **Authentication**: None (local network use)
- **Data Format**: JSON
- **Character Encoding**: UTF-8

## API Endpoints

### 1. System Status API

#### Get Current System Status
```http
GET /api/current-status
```

**Response Example**:
```json
{
  "dough_size": 125.8,
  "size_change_percent": 25.8,
  "monitoring_active": true,
  "last_update": 1639123456,
  "camera_status": "active"
}
```

**Field Descriptions**:
- `dough_size`: Current dough size measurement (relative units)
- `size_change_percent`: Percentage change from initial size
- `monitoring_active`: Whether monitoring is currently active
- `last_update`: Last update timestamp (Unix timestamp)
- `camera_status`: Camera connection status

### 2. Image Analysis API

#### Get Image Analysis Metrics
```http
GET /api/image-metrics?hours={hours}&limit={limit}
```

**Parameters**:
- `hours` (optional): Query data from past N hours, default 24
- `limit` (optional): Limit number of returned records, default 100

**Response Example**:
```json
[
  {
    "id": 1,
    "timestamp": 1639123456,
    "dough_size": 125.8,
    "size_change": 25.8,
    "contour_area": 15420,
    "detection_confidence": 0.95,
    "image_path": "/data/images/2021-12-10_10-30-56.jpg",
    "created_at": "2021-12-10T10:30:56"
  }
]
```

**Field Descriptions**:
- `dough_size`: Measured dough size (relative units)
- `size_change`: Change from previous measurement (%)
- `contour_area`: Detected contour area in pixels
- `detection_confidence`: Confidence score (0.0-1.0)
- `image_path`: Path to analyzed image file

#### Get Latest Analysis
```http
GET /api/image-metrics/latest
```

#### Trigger Manual Analysis
```http
POST /api/image-metrics/analyze
```

**Response Example**:
```json
{
  "status": "success",
  "analysis_id": 101,
  "message": "Analysis started"
}
```

### 3. Session Management API

#### Get Fermentation Sessions
```http
GET /api/sessions?status={status}
```

**Parameters**:
- `status` (optional): Filter by status (`active`, `completed`, `paused`)

**Response Example**:
```json
[
  {
    "id": 1,
    "name": "First Rise",
    "start_time": 1639120000,
    "end_time": null,
    "status": "active",
    "notes": "Using new yeast strain",
    "created_at": "2021-12-10T09:33:20"
  }
]
```

#### Create New Session
```http
POST /api/sessions
Content-Type: application/json
```

**Request Example**:
```json
{
  "name": "Second Rise",
  "notes": "Extended fermentation time"
}
```

**Response Example**:
```json
{
  "id": 2,
  "status": "created",
  "message": "Session created successfully"
}
```

#### Update Session
```http
PUT /api/sessions/{session_id}
Content-Type: application/json
```

**Request Example**:
```json
{
  "status": "completed",
  "notes": "Fermentation completed successfully"
}
```

#### Delete Session
```http
DELETE /api/sessions/{session_id}
```

### 4. System Control API

#### System Information
```http
GET /api/system/info
```

**Response Example**:
```json
{
  "system": {
    "version": "1.0.0",
    "uptime": 86400,
    "cpu_usage": 15.2,
    "memory_usage": 45.6,
    "disk_usage": 23.4
  },
  "hardware": {
    "camera_available": true,
    "camera_resolution": "1920x1080"
  }
}
```

#### System Configuration
```http
POST /api/system/config
Content-Type: application/json
```

**Request Example**:
```json
{
  "analysis_interval": 300,
  "camera_resolution": "1920x1080",
  "detection_threshold": 0.8
}
```

### 5. Data Export API

#### Export Image Analysis Data
```http
GET /api/export/image-metrics?format={format}&start={start}&end={end}
```

**Parameters**:
- `format`: Export format (`csv`, `json`)
- `start`: Start time (Unix timestamp)
- `end`: End time (Unix timestamp)

#### Export Session Report
```http
GET /api/export/report?session_id={session_id}&format={format}
```

**Parameters**:
- `session_id`: Session ID to export
- `format`: Report format (`json`, `csv`)

## WebSocket API (Real-time Data)

### Connection Endpoint
```
ws://[device-ip]:5000/ws
```

### Message Format

#### Subscribe to Data Stream
```json
{
  "action": "subscribe",
  "channels": ["images", "system"]
}
```

#### Real-time Image Analysis
```json
{
  "type": "image_analysis",
  "data": {
    "timestamp": 1639123456,
    "dough_size": 125.8,
    "size_change": 25.8,
    "detection_confidence": 0.95
  }
}
```

#### System Status Updates
```json
{
  "type": "system_status",
  "data": {
    "timestamp": 1639123456,
    "camera_status": "active",
    "monitoring_active": true
  }
}
```

## Error Handling

### HTTP Status Codes

- `200`: Success
- `201`: Created successfully
- `400`: Bad request
- `404`: Resource not found
- `500`: Server error

### Error Response Format

```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Invalid request parameters",
    "details": {
      "field": "hours",
      "reason": "Value must be between 1 and 168"
    }
  }
}
```

### Common Error Codes

- `INVALID_REQUEST`: Invalid request parameters
- `RESOURCE_NOT_FOUND`: Resource not found
- `DATABASE_ERROR`: Database error
- `CAMERA_ERROR`: Camera access error
- `SYSTEM_ERROR`: System error

## Rate Limits

### Request Rate Limits

- General API: 60 requests/minute
- System Control API: 10 requests/minute
- Data Export API: 5 requests/minute

### Data Size Limits

- Maximum 10,000 records per query
- Maximum export file size: 50MB
- Maximum WebSocket message size: 1MB

## Example Code

### Python Client Example

```python
import requests
import json

# Base configuration
BASE_URL = "http://192.168.1.100:5000/api"

class FermentationAPI:
    def __init__(self, base_url):
        self.base_url = base_url
    
    def get_current_status(self):
        response = requests.get(f"{self.base_url}/current-status")
        return response.json()
    
    def get_image_metrics(self, hours=24):
        response = requests.get(
            f"{self.base_url}/image-metrics", 
            params={"hours": hours}
        )
        return response.json()
    
    def create_session(self, name, notes=""):
        data = {"name": name, "notes": notes}
        response = requests.post(
            f"{self.base_url}/sessions",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        return response.json()
    
    def trigger_analysis(self):
        response = requests.post(f"{self.base_url}/image-metrics/analyze")
        return response.json()

# Usage example
api = FermentationAPI(BASE_URL)

# Get current status
status = api.get_current_status()
print(f"Dough size: {status['dough_size']}")
print(f"Size change: {status['size_change_percent']}%")

# Get past 12 hours of analysis data
data = api.get_image_metrics(hours=12)
print(f"Found {len(data)} analysis records")

# Create new fermentation session
session = api.create_session("Test Batch", "Using new recipe")
print(f"Created session ID: {session['id']}")

# Trigger manual analysis
analysis = api.trigger_analysis()
print(f"Analysis started: {analysis['message']}")
```

### JavaScript Client Example

```javascript
class FermentationAPI {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
    }
    
    async getCurrentStatus() {
        const response = await fetch(`${this.baseUrl}/current-status`);
        return response.json();
    }
    
    async getImageMetrics(hours = 24) {
        const response = await fetch(
            `${this.baseUrl}/image-metrics?hours=${hours}`
        );
        return response.json();
    }
    
    async createSession(name, notes = '') {
        const response = await fetch(`${this.baseUrl}/sessions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, notes }),
        });
        return response.json();
    }
    
    async triggerAnalysis() {
        const response = await fetch(`${this.baseUrl}/image-metrics/analyze`, {
            method: 'POST'
        });
        return response.json();
    }
}

// Usage example
const api = new FermentationAPI('http://192.168.1.100:5000/api');

// Get and display current status
api.getCurrentStatus().then(status => {
    console.log(`Dough size: ${status.dough_size}`);
    console.log(`Size change: ${status.size_change_percent}%`);
});

// WebSocket real-time data
const ws = new WebSocket('ws://192.168.1.100:5000/ws');

ws.onopen = () => {
    ws.send(JSON.stringify({
        action: 'subscribe',
        channels: ['images', 'system']
    }));
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Real-time data:', data);
    
    if (data.type === 'image_analysis') {
        updateDoughSizeChart(data.data);
    }
};

function updateDoughSizeChart(analysisData) {
    // Update your chart/UI with new dough size data
    console.log('New dough size:', analysisData.dough_size);
}
```

## Security Recommendations

1. **Network Security**:
   - Use only within local network
   - Consider implementing HTTPS
   - Use firewall to restrict access

2. **Data Validation**:
   - Validate all input parameters
   - Implement rate limiting
   - Filter sensitive information

3. **Error Handling**:
   - Don't expose system internals
   - Log abnormal access attempts
   - Implement proper error responses

4. **Data Protection**:
   - Regular data backups
   - Implement access controls
   - Consider data encryption for sensitive information