# API 文件

麵團發酵監控系統提供 RESTful API 介面，支援即時資料存取和系統控制。

## 基本資訊

- **基礎 URL**: `http://[device-ip]:5000/api`
- **認證方式**: 無 (區域網路內使用)
- **資料格式**: JSON
- **字元編碼**: UTF-8

## API 端點列表

### 1. 系統狀態 API

#### 取得目前系統狀態
```http
GET /api/current-status
```

**回應範例**:
```json
{
  "temperature": 23.5,
  "humidity": 65.2,
  "fermentation_activity": 12.8,
  "bubble_count": 15,
  "last_update": 1639123456
}
```

**欄位說明**:
- `temperature`: 當前溫度 (°C)
- `humidity`: 當前濕度 (%)
- `fermentation_activity`: 發酵活動指數 (0-100)
- `bubble_count`: 檢測到的氣泡數量
- `last_update`: 最後更新時間 (Unix timestamp)

### 2. 感測器資料 API

#### 取得歷史感測器資料
```http
GET /api/sensor-data?hours={hours}&limit={limit}
```

**參數**:
- `hours` (可選): 查詢過去 N 小時的資料，預設 24
- `limit` (可選): 限制回傳筆數，預設 1000

**回應範例**:
```json
[
  {
    "id": 1,
    "timestamp": 1639123456,
    "temperature": 23.5,
    "humidity": 65.2,
    "created_at": "2021-12-10T10:30:56"
  },
  {
    "id": 2,
    "timestamp": 1639123486,
    "temperature": 23.6,
    "humidity": 65.0,
    "created_at": "2021-12-10T10:31:26"
  }
]
```

#### 取得最新感測器讀數
```http
GET /api/sensor-data/latest
```

**回應範例**:
```json
{
  "id": 100,
  "timestamp": 1639123456,
  "temperature": 23.5,
  "humidity": 65.2,
  "created_at": "2021-12-10T10:30:56"
}
```

### 3. 影像分析 API

#### 取得影像分析結果
```http
GET /api/image-metrics?hours={hours}&limit={limit}
```

**參數**:
- `hours` (可選): 查詢過去 N 小時的資料，預設 24
- `limit` (可選): 限制回傳筆數，預設 100

**回應範例**:
```json
[
  {
    "id": 1,
    "timestamp": 1639123456,
    "volume_change": 5.2,
    "surface_activity": 12.8,
    "bubble_count": 15,
    "texture_variance": 234.5,
    "image_path": "/data/images/2021-12-10_10-30-56.jpg",
    "created_at": "2021-12-10T10:30:56"
  }
]
```

**欄位說明**:
- `volume_change`: 體積變化百分比
- `surface_activity`: 表面活動指數
- `bubble_count`: 氣泡數量
- `texture_variance`: 紋理變化指數
- `image_path`: 分析影像檔案路徑

#### 取得最新影像分析
```http
GET /api/image-metrics/latest
```

#### 觸發手動分析
```http
POST /api/image-metrics/analyze
```

**回應範例**:
```json
{
  "status": "success",
  "analysis_id": 101,
  "message": "Analysis started"
}
```

### 4. 發酵階段管理 API

#### 取得發酵階段列表
```http
GET /api/sessions?status={status}
```

**參數**:
- `status` (可選): 篩選狀態 (`active`, `completed`, `paused`)

**回應範例**:
```json
[
  {
    "id": 1,
    "name": "第一次發酵",
    "start_time": 1639120000,
    "end_time": null,
    "status": "active",
    "notes": "使用新酵母",
    "created_at": "2021-12-10T09:33:20"
  }
]
```

#### 建立新發酵階段
```http
POST /api/sessions
Content-Type: application/json
```

**請求範例**:
```json
{
  "name": "第二次發酵",
  "notes": "增加發酵時間"
}
```

**回應範例**:
```json
{
  "id": 2,
  "status": "created",
  "message": "Session created successfully"
}
```

#### 更新發酵階段
```http
PUT /api/sessions/{session_id}
Content-Type: application/json
```

**請求範例**:
```json
{
  "status": "completed",
  "notes": "發酵完成，效果良好"
}
```

#### 刪除發酵階段
```http
DELETE /api/sessions/{session_id}
```

### 5. 系統控制 API

#### 系統資訊
```http
GET /api/system/info
```

**回應範例**:
```json
{
  "system": {
    "version": "1.0.0",
    "uptime": 86400,
    "cpu_usage": 15.2,
    "memory_usage": 45.6,
    "disk_usage": 23.4,
    "temperature": 42.5
  },
  "hardware": {
    "camera_available": true,
    "temperature_sensor": true,
    "humidity_sensor": true
  }
}
```

#### 重新啟動服務
```http
POST /api/system/restart
```

#### 設定系統參數
```http
POST /api/system/config
Content-Type: application/json
```

**請求範例**:
```json
{
  "sensor_interval": 30,
  "image_analysis_interval": 300,
  "camera_resolution": "1920x1080"
}
```

### 6. 資料匯出 API

#### 匯出感測器資料 (CSV)
```http
GET /api/export/sensor-data?format=csv&start={start}&end={end}
```

**參數**:
- `format`: 匯出格式 (`csv`, `json`)
- `start`: 開始時間 (Unix timestamp)
- `end`: 結束時間 (Unix timestamp)

#### 匯出影像分析結果
```http
GET /api/export/image-metrics?format=json&start={start}&end={end}
```

#### 匯出完整報告
```http
GET /api/export/report?session_id={session_id}&format=pdf
```

## WebSocket API (即時資料)

### 連線端點
```
ws://[device-ip]:5000/ws
```

### 訊息格式

#### 訂閱資料流
```json
{
  "action": "subscribe",
  "channels": ["sensors", "images", "system"]
}
```

#### 即時感測器資料
```json
{
  "type": "sensor_data",
  "data": {
    "timestamp": 1639123456,
    "temperature": 23.5,
    "humidity": 65.2
  }
}
```

#### 即時影像分析
```json
{
  "type": "image_analysis",
  "data": {
    "timestamp": 1639123456,
    "bubble_count": 15,
    "fermentation_activity": 12.8
  }
}
```

## 錯誤處理

### HTTP 狀態碼

- `200`: 成功
- `201`: 建立成功
- `400`: 請求錯誤
- `404`: 資源未找到
- `500`: 伺服器錯誤

### 錯誤回應格式

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

### 常見錯誤碼

- `INVALID_REQUEST`: 請求參數錯誤
- `RESOURCE_NOT_FOUND`: 資源未找到
- `DATABASE_ERROR`: 資料庫錯誤
- `HARDWARE_ERROR`: 硬體存取錯誤
- `SYSTEM_ERROR`: 系統錯誤

## 限制說明

### 請求頻率限制

- 一般 API: 60 requests/minute
- 系統控制 API: 10 requests/minute
- 資料匯出 API: 5 requests/minute

### 資料大小限制

- 單次查詢最大 10,000 筆記錄
- 匯出檔案最大 50MB
- WebSocket 訊息最大 1MB

## 範例程式碼

### Python 客戶端範例

```python
import requests
import json

# 基礎設定
BASE_URL = "http://192.168.1.100:5000/api"

class FermentationAPI:
    def __init__(self, base_url):
        self.base_url = base_url
    
    def get_current_status(self):
        response = requests.get(f"{self.base_url}/current-status")
        return response.json()
    
    def get_sensor_data(self, hours=24):
        response = requests.get(
            f"{self.base_url}/sensor-data", 
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

# 使用範例
api = FermentationAPI(BASE_URL)

# 取得目前狀態
status = api.get_current_status()
print(f"溫度: {status['temperature']}°C")

# 取得過去12小時的感測器資料
data = api.get_sensor_data(hours=12)
print(f"共有 {len(data)} 筆記錄")

# 建立新的發酵階段
session = api.create_session("測試發酵", "使用新配方")
print(f"建立階段 ID: {session['id']}")
```

### JavaScript 客戶端範例

```javascript
class FermentationAPI {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
    }
    
    async getCurrentStatus() {
        const response = await fetch(`${this.baseUrl}/current-status`);
        return response.json();
    }
    
    async getSensorData(hours = 24) {
        const response = await fetch(
            `${this.baseUrl}/sensor-data?hours=${hours}`
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
}

// 使用範例
const api = new FermentationAPI('http://192.168.1.100:5000/api');

// 取得並顯示目前狀態
api.getCurrentStatus().then(status => {
    console.log(`溫度: ${status.temperature}°C`);
    console.log(`濕度: ${status.humidity}%`);
});

// WebSocket 即時資料
const ws = new WebSocket('ws://192.168.1.100:5000/ws');

ws.onopen = () => {
    ws.send(JSON.stringify({
        action: 'subscribe',
        channels: ['sensors', 'images']
    }));
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('即時資料:', data);
};
```

## 安全性建議

1. **網路安全**:
   - 僅在區域網路內使用
   - 考慮實作 HTTPS
   - 使用防火牆限制存取

2. **資料驗證**:
   - 驗證所有輸入參數
   - 實作請求頻率限制
   - 過濾敏感資訊

3. **錯誤處理**:
   - 不洩露系統內部資訊
   - 記錄異常存取
   - 實作適當的錯誤回應

4. **資料保護**:
   - 定期備份資料
   - 實作資料存取權限
   - 考慮敏感資料加密