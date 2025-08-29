# 麵團發酵監控系統 (Fermentation Monitor)

基於 Raspberry Pi 4 的嵌入式 Linux 麵團發酵監控系統，使用 OpenCV 進行視覺分析和 Flask 提供 Web 介面。

## 系統概述

這個專案提供完整的麵團發酵監控解決方案，包括：

- **即時監控**: 溫度、濕度和視覺發酵活動監控
- **影像分析**: 使用 OpenCV 分析麵團表面變化、氣泡數量和體積變化
- **Web 介面**: 基於 Flask 的響應式 Web 儀表板
- **資料儲存**: SQLite 資料庫儲存歷史資料
- **嵌入式部署**: 使用 Yocto 建構的自訂 Linux 映像

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

## 硬體需求

- **主板**: Raspberry Pi 4 (4GB RAM 推薦)
- **攝影機**: Raspberry Pi Camera Module V2 或 USB 攝影機
- **感測器**: 
  - DS18B20 溫度感測器 (1-Wire)
  - DHT22 溫濕度感測器
- **儲存**: microSD 卡 (32GB 以上)
- **電源**: 5V/3A USB-C 電源供應器

## 軟體依賴

### 系統層級
- Yocto Linux (Scarthgap 版本)
- OpenCV 4.x
- Python 3.8+
- Flask 2.x
- SQLite 3

### Python 套件
- opencv-python
- numpy
- flask
- RPi.GPIO (Raspberry Pi)
- w1thermsensor
- Adafruit-DHT

## 快速開始

### 1. 開發環境設定

```bash
git clone <repository-url> fermentation-monitor
cd fermentation-monitor
make dev-setup
```

### 2. 建置應用程式

```bash
make build
```

### 3. 運行開發伺服器

```bash
make dev-run
```

Web 介面將在 http://localhost:5000 可用。

### 4. 建置完整系統映像

```bash
make yocto-build
```

### 5. 部署到 Raspberry Pi

```bash
make deploy TARGET_HOST=192.168.1.100
```

## 使用說明

### Web 介面功能

1. **首頁**: 系統概覽和即時狀態
2. **儀表板**: 詳細監控資料和圖表
3. **發酵階段管理**: 建立和管理不同的發酵階段

### API 端點

- `GET /api/current-status` - 取得目前狀態
- `GET /api/sensor-data` - 取得感測器歷史資料
- `GET /api/image-metrics` - 取得影像分析資料
- `GET /api/sessions` - 取得發酵階段列表
- `POST /api/sessions` - 建立新的發酵階段

### 命令列工具

```bash
# 建置系統
make build

# 清理建置檔案
make clean

# 運行測試
make test

# 程式碼格式化
make format

# 程式碼檢查
make lint

# 製作 SD 卡映像
make sdcard SD_DEVICE=/dev/sdX
```

## 配置

### 感測器配置

編輯 `config/sensors.conf` 來配置感測器參數：

```ini
[temperature]
enabled = true
sensor_type = DS18B20
pin = 4

[humidity]
enabled = true
sensor_type = DHT22
pin = 18
```

### 攝影機配置

編輯 `config/camera.conf` 來配置攝影機參數：

```ini
[camera]
device = 0
width = 1920
height = 1080
fps = 30
```

## 開發指南

### 新增感測器

1. 在 `src/python/sensors/` 建立新的感測器模組
2. 實作 `read()` 和 `is_available()` 方法
3. 在 `main.py` 中註冊新感測器

### 新增影像分析演算法

1. 編輯 `src/cpp/src/image_processor.cpp` 或 `src/python/image_processing/fermentation_analyzer.py`
2. 實作新的分析函數
3. 更新資料庫結構 (如需要)

### Web 介面開發

- 前端: HTML/CSS/JavaScript (Bootstrap + Chart.js)
- 後端: Flask (Python)
- 範本: Jinja2

## 測試

```bash
# 運行所有測試
make test

# 僅運行 Python 測試
pytest tests/python/

# 產生覆蓋率報告
pytest tests/ --cov=src/python --cov-report=html
```

## 部署選項

### 1. 開發部署
本機開發和測試

### 2. 手動部署
使用部署腳本到現有 Raspberry Pi OS

### 3. Yocto 部署
建構完整的自訂 Linux 映像

## 疑難排解

### 常見問題

1. **攝影機無法存取**
   - 檢查攝影機模組連接
   - 確認 `sudo raspi-config` 中啟用攝影機

2. **感測器讀取失敗**
   - 檢查接線
   - 確認感測器驅動程式已載入

3. **Web 介面無法存取**
   - 檢查 Flask 服務狀態
   - 確認防火牆設定

### 日誌查看

```bash
# 查看服務日誌
sudo journalctl -u fermentation-monitor.service -f

# 查看應用程式日誌
tail -f /opt/fermentation-monitor/logs/app.log
```

## 貢獻指南

1. Fork 專案
2. 建立功能分支
3. 提交變更
4. 建立 Pull Request

## 授權條款

MIT License - 詳見 LICENSE 檔案

## 作者

[作者資訊]

## 致謝

- OpenCV 社群
- Yocto Project
- Raspberry Pi Foundation