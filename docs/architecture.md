# 系統架構文件

## 概覽

麵團發酵監控系統採用分層架構設計，結合了 C++ 的效能優勢和 Python 的開發便利性，提供完整的嵌入式監控解決方案。

## 整體架構

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
│    ┌──────────────────┬────────────────────────────────────┐│
│    │   Sensor Manager │    Image Processing Engine        ││
│    │    (Python)      │       (C++ & Python)             ││
│    └──────────────────┴────────────────────────────────────┘│
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                 Data Storage                                │
│                  (SQLite)                                   │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                 Hardware Layer                              │
│    ┌──────────────┬──────────────┬─────────────────────────┐│
│    │   Sensors    │   Camera     │      GPIO/I2C          ││
│    └──────────────┴──────────────┴─────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

## 核心元件

### 1. Web 介面層 (Presentation Layer)

**技術棧**: HTML5, CSS3, JavaScript, Bootstrap, Chart.js

**職責**:
- 提供使用者介面
- 資料視覺化
- 即時狀態顯示
- 系統控制介面

**檔案結構**:
```
src/web/
├── templates/
│   ├── base.html           # 基本範本
│   ├── index.html          # 首頁
│   └── dashboard.html      # 儀表板
├── static/
│   ├── css/
│   │   └── style.css       # 自訂樣式
│   └── js/
│       └── dashboard.js    # 前端邏輯
```

### 2. API 層 (API Layer)

**技術棧**: Flask, Python 3.8+

**職責**:
- RESTful API 提供
- 資料序列化/反序列化
- 用戶會話管理
- 錯誤處理

**主要端點**:
- `/api/current-status` - 即時狀態
- `/api/sensor-data` - 感測器資料
- `/api/image-metrics` - 影像分析結果
- `/api/sessions` - 發酵階段管理

### 3. 應用程式核心層 (Application Core)

#### 3.1 感測器管理 (Sensor Manager)

**技術棧**: Python 3.8+, RPi.GPIO, 1-Wire, I2C

**功能**:
- 溫度感測器讀取 (DS18B20)
- 濕度感測器讀取 (DHT22)
- 感測器狀態監控
- 資料驗證和過濾

**類別設計**:
```python
class TemperatureSensor:
    def read() -> float
    def is_available() -> bool

class HumiditySensor:
    def read() -> float
    def is_available() -> bool
```

#### 3.2 影像處理引擎 (Image Processing Engine)

**C++ 核心 (高效能)**:
- OpenCV 4.x
- 即時影像擷取
- 核心演算法實作

**Python 包裝器**:
- 演算法協調
- 資料轉換
- 錯誤處理

**主要功能**:
- 麵團體積變化檢測
- 表面活動分析
- 氣泡計數
- 紋理變化分析

### 4. 資料存取層 (Data Access Layer)

**技術棧**: SQLite 3, Python sqlite3

**資料結構**:
```sql
-- 感測器資料
sensor_data (id, timestamp, temperature, humidity)

-- 影像分析結果
image_metrics (id, timestamp, volume_change, surface_activity, 
               bubble_count, texture_variance)

-- 發酵階段
fermentation_sessions (id, name, start_time, end_time, status, notes)
```

### 5. 硬體抽象層 (Hardware Abstraction Layer)

**感測器介面**:
- 1-Wire 介面 (溫度感測器)
- I2C 介面 (濕度感測器)
- GPIO 控制

**攝影機介面**:
- V4L2 (Video4Linux2)
- OpenCV VideoCapture API

## 通訊協定

### 1. 內部通訊

**Python ↔ C++**:
- 共享記憶體
- Named Pipes
- 檔案 I/O

**執行緒間通訊**:
- Python threading
- Queue 物件
- Event 同步

### 2. 外部通訊

**Web API**:
- HTTP/1.1
- JSON 資料格式
- RESTful 設計原則

**硬體通訊**:
- I2C 協定 (濕度感測器)
- 1-Wire 協定 (溫度感測器)
- SPI 協定 (可擴展)

## 資料流

### 1. 感測器資料流

```
感測器 → GPIO/I2C → Python Sensor Classes → Database → Web API → Frontend
```

### 2. 影像資料流

```
Camera → V4L2 → OpenCV → C++ Processing → Python Interface → Database → Web API → Frontend
```

### 3. 控制流

```
Frontend → Web API → Python Core → Hardware Control
```

## 效能考量

### 1. C++/Python 混合架構

**C++ 處理**:
- 密集運算 (影像處理)
- 即時要求高的任務
- 記憶體效率要求

**Python 處理**:
- 業務邏輯
- API 服務
- 系統協調

### 2. 記憶體管理

- OpenCV Mat 物件重用
- Python 垃圾回收優化
- 資料庫連接池

### 3. 並行處理

- 多執行緒設計
- 非阻塞 I/O
- 任務佇列機制

## 安全性設計

### 1. 資料保護

- SQLite 資料庫檔案權限控制
- 敏感資料加密存儲
- 網路傳輸 HTTPS (可選)

### 2. 系統安全

- 最小權限原則
- 輸入驗證
- 錯誤資訊過濾

### 3. 硬體安全

- GPIO 權限管理
- 裝置存取控制
- 系統資源保護

## 擴展性設計

### 1. 模組化架構

- 插件式感測器支援
- 可擴展的處理演算法
- 配置驅動的系統行為

### 2. API 版本控制

- RESTful API 版本策略
- 向後相容性支援
- 功能漸進式部署

### 3. 硬體抽象

- 通用感測器介面
- 攝影機抽象層
- 平台無關設計

## 部署架構

### 1. 開發環境

- 本機 Ubuntu/Debian
- Docker 容器 (可選)
- 虛擬環境隔離

### 2. 目標環境

- Raspberry Pi 4
- 自訂 Yocto Linux
- Systemd 服務管理

### 3. 建置流程

- CMake 建置系統
- Yocto meta-layer
- 自動化部署腳本

## 監控和維護

### 1. 日誌系統

- Systemd journald 整合
- 分級日誌記錄
- 日誌輪轉管理

### 2. 健康檢查

- 硬體狀態監控
- 服務可用性檢查
- 自動故障恢復

### 3. 效能監控

- 系統資源使用率
- API 回應時間
- 資料庫效能指標