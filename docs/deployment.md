# 部署指南

本文件詳細說明如何部署麵團發酵監控系統到 Raspberry Pi 4 環境。

## 部署選項

### 1. 開發部署 (Development Deployment)
適用於本機開發和測試

### 2. 生產部署 (Production Deployment)
使用現有 Raspberry Pi OS 系統

### 3. Yocto 映像部署 (Yocto Image Deployment)
建構完整的自訂 Linux 映像

## 準備工作

### 硬體準備

1. **Raspberry Pi 4** (4GB RAM 推薦)
2. **microSD 卡** (32GB 以上，Class 10)
3. **Raspberry Pi Camera Module V2** 或 USB 攝影機
4. **溫度感測器** DS18B20
5. **濕度感測器** DHT22
6. **跳線和麵包板**

### 軟體準備

1. **開發電腦** (Ubuntu 18.04+ 或類似)
2. **Git** 版本控制
3. **SSH 客戶端**
4. **SD 卡讀卡機**

## 選項 1: 開發部署

### 1.1 環境設定

```bash
# 複製專案
git clone <repository-url> fermentation-monitor
cd fermentation-monitor

# 設定開發環境
make dev-setup
```

### 1.2 本機執行

```bash
# 建置 C++ 元件
make build

# 啟動開發伺服器
make dev-run
```

### 1.3 存取介面

開啟瀏覽器至 `http://localhost:5000`

## 選項 2: 生產部署

### 2.1 準備 Raspberry Pi

```bash
# 更新系統
sudo apt update && sudo apt upgrade -y

# 安裝系統依賴
sudo apt install -y python3 python3-pip cmake build-essential \
    libopencv-dev python3-opencv git

# 啟用攝影機
sudo raspi-config
# 選擇 Interface Options > Camera > Enable

# 啟用 1-Wire (溫度感測器)
echo 'dtoverlay=w1-gpio' | sudo tee -a /boot/config.txt
echo 'dtoverlay=w1-therm' | sudo tee -a /boot/config.txt

# 重啟系統
sudo reboot
```

### 2.2 部署應用程式

在開發電腦上執行：

```bash
# 使用部署腳本
make deploy TARGET_HOST=192.168.1.100

# 或手動部署
./scripts/deploy.sh -h 192.168.1.100 -u pi
```

### 2.3 驗證部署

```bash
# SSH 連線到 Raspberry Pi
ssh pi@192.168.1.100

# 檢查服務狀態
sudo systemctl status fermentation-monitor.service

# 查看日誌
sudo journalctl -u fermentation-monitor.service -f
```

### 2.4 存取介面

開啟瀏覽器至 `http://192.168.1.100:5000`

## 選項 3: Yocto 映像部署

### 3.1 建置環境準備

```bash
# 安裝 Yocto 依賴套件
sudo apt install -y gawk wget git diffstat unzip texinfo gcc-multilib \
    build-essential chrpath socat cpio python3 python3-pip python3-pexpect \
    xz-utils debianutils iputils-ping python3-git python3-jinja2 libegl1-mesa \
    libsdl1.2-dev pylint3 xterm python3-subunit mesa-common-dev zstd liblz4-tool
```

### 3.2 建置 Yocto 映像

```bash
# 建置完整系統映像
make yocto-build
```

建置過程需要 2-8 小時，取決於硬體效能。

### 3.3 燒錄 SD 卡

```bash
# 燒錄映像到 SD 卡 (請小心選擇正確的裝置)
make sdcard SD_DEVICE=/dev/sdX
```

**警告**: 這會完全覆寫 SD 卡上的所有資料。

### 3.4 首次啟動

1. 插入 SD 卡到 Raspberry Pi
2. 連接攝影機和感測器
3. 接上電源開機
4. 系統會自動啟動服務

## 硬體連線

### 溫度感測器 (DS18B20)

```
DS18B20    Raspberry Pi 4
VDD    →   3.3V (Pin 1)
GND    →   GND (Pin 6)
DQ     →   GPIO 4 (Pin 7)
```

需要 4.7kΩ 上拉電阻在 DQ 和 VDD 之間。

### 濕度感測器 (DHT22)

```
DHT22      Raspberry Pi 4
VCC    →   5V (Pin 2)
GND    →   GND (Pin 6)
DATA   →   GPIO 18 (Pin 12)
```

### 攝影機模組

連接到 Camera Serial Interface (CSI) 連接器。

## 網路設定

### WiFi 設定 (Raspberry Pi OS)

```bash
# 編輯 WiFi 設定
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

# 新增網路設定
network={
    ssid="YourWiFiName"
    psk="YourWiFiPassword"
}

# 重啟網路服務
sudo systemctl restart dhcpcd
```

### 靜態 IP 設定

```bash
# 編輯 dhcpcd.conf
sudo nano /etc/dhcpcd.conf

# 新增靜態 IP 設定
interface wlan0
static ip_address=192.168.1.100/24
static routers=192.168.1.1
static domain_name_servers=8.8.8.8 8.8.4.4
```

## 服務管理

### 啟動/停止服務

```bash
# 啟動服務
sudo systemctl start fermentation-monitor.service

# 停止服務
sudo systemctl stop fermentation-monitor.service

# 重啟服務
sudo systemctl restart fermentation-monitor.service

# 啟用開機自動啟動
sudo systemctl enable fermentation-monitor.service

# 停用開機自動啟動
sudo systemctl disable fermentation-monitor.service
```

### 查看服務狀態

```bash
# 服務狀態
sudo systemctl status fermentation-monitor.service

# 即時日誌
sudo journalctl -u fermentation-monitor.service -f

# 歷史日誌
sudo journalctl -u fermentation-monitor.service --since "1 hour ago"
```

## 效能調整

### 系統最佳化

```bash
# GPU 記憶體分割
echo 'gpu_mem=128' | sudo tee -a /boot/config.txt

# CPU 頻率設定
echo 'arm_freq=1800' | sudo tee -a /boot/config.txt

# 啟用 64-bit 核心
echo 'arm_64bit=1' | sudo tee -a /boot/config.txt
```

### 應用程式調整

編輯 `/opt/fermentation-monitor/config/app.conf`:

```ini
[performance]
# 影像處理執行緒數
image_processing_threads = 2

# 感測器讀取間隔 (秒)
sensor_read_interval = 30

# 影像分析間隔 (秒)
image_analysis_interval = 300

[camera]
# 降低解析度以提升效能
width = 1280
height = 720
fps = 15
```

## 備份和恢復

### 系統備份

```bash
# 建立系統備份
sudo dd if=/dev/mmcblk0 of=/path/to/backup.img bs=1M status=progress

# 壓縮備份
gzip /path/to/backup.img
```

### 資料備份

```bash
# 備份資料庫
sqlite3 /opt/fermentation-monitor/data/fermentation.db .dump > backup.sql

# 備份設定檔
tar -czf config_backup.tar.gz /opt/fermentation-monitor/config/
```

### 恢復系統

```bash
# 從備份恢復
sudo dd if=/path/to/backup.img.gz bs=1M status=progress | gunzip > /dev/mmcblk0
```

## 疑難排解

### 常見問題

1. **服務無法啟動**
   ```bash
   # 檢查日誌
   sudo journalctl -u fermentation-monitor.service
   
   # 檢查權限
   ls -la /opt/fermentation-monitor/
   ```

2. **攝影機無法存取**
   ```bash
   # 檢查攝影機裝置
   ls /dev/video*
   
   # 測試攝影機
   raspistill -o test.jpg
   ```

3. **感測器讀取失敗**
   ```bash
   # 檢查 1-Wire 裝置
   ls /sys/bus/w1/devices/
   
   # 檢查 GPIO 權限
   groups $USER
   ```

4. **網路連線問題**
   ```bash
   # 檢查網路狀態
   ip addr show
   
   # 測試連線
   ping google.com
   ```

### 日誌分析

```bash
# 應用程式日誌
tail -f /opt/fermentation-monitor/logs/app.log

# 系統日誌
sudo journalctl -f

# 核心訊息
dmesg | tail -20
```

### 效能監控

```bash
# CPU 使用率
top

# 記憶體使用
free -h

# 磁碟使用
df -h

# 溫度監控
vcgencmd measure_temp
```

## 安全性設定

### SSH 安全

```bash
# 變更預設密碼
passwd

# 停用密碼登入 (使用 SSH 金鑰)
sudo nano /etc/ssh/sshd_config
# PasswordAuthentication no

# 重啟 SSH 服務
sudo systemctl restart ssh
```

### 防火牆設定

```bash
# 安裝 UFW
sudo apt install ufw

# 基本規則
sudo ufw default deny incoming
sudo ufw default allow outgoing

# 允許 SSH
sudo ufw allow ssh

# 允許 Web 介面
sudo ufw allow 5000

# 啟用防火牆
sudo ufw enable
```

## 維護計劃

### 定期維護

1. **每週**:
   - 檢查服務狀態
   - 查看系統日誌
   - 清理暫存檔案

2. **每月**:
   - 系統更新
   - 資料庫備份
   - 效能監控

3. **每季**:
   - 完整系統備份
   - 硬體清潔
   - 安全性檢查

### 自動化維護腳本

```bash
#!/bin/bash
# /opt/fermentation-monitor/scripts/maintenance.sh

# 清理日誌
sudo journalctl --vacuum-time=30d

# 清理暫存檔案
find /tmp -name "*.tmp" -mtime +7 -delete

# 資料庫最佳化
sqlite3 /opt/fermentation-monitor/data/fermentation.db "VACUUM;"

# 檢查磁碟空間
df -h | awk '$5 > 80 {print "Warning: " $1 " is " $5 " full"}'
```

設定 cron job:
```bash
# 每週執行維護
echo "0 2 * * 0 /opt/fermentation-monitor/scripts/maintenance.sh" | crontab -
```