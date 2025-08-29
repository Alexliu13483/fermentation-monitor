# Deployment Guide

This document details how to deploy the Fermentation Monitor system focused on dough size monitoring using webcam-based image analysis.

## Deployment Options

### 1. Development Deployment
For local development and testing on any machine with a camera

### 2. Production Deployment
Deploy to a dedicated system (Raspberry Pi, server, etc.)

### 3. Cross-Platform Deployment
Compatible with Windows, macOS, and Linux systems

## Prerequisites

### Hardware Requirements

**Minimum Requirements:**
1. **Computer** with camera (built-in or USB)
2. **USB Webcam** (if no built-in camera)
3. **Network connection** (for web interface access)

**For Raspberry Pi Deployment:**
1. **Raspberry Pi 4** (2GB RAM minimum, 4GB recommended)
2. **microSD card** (16GB or larger, Class 10)
3. **USB webcam** or Raspberry Pi Camera Module
4. **Power supply** (5V/3A USB-C)

### Software Requirements

1. **Python 3.8+**
2. **Git** version control
3. **Virtual environment** support
4. **Camera drivers** (usually included with OS)

## Option 1: Development Deployment

### 1.1 Environment Setup

```bash
# Clone the project
git clone https://github.com/Alexliu13483/fermentation-monitor.git
cd fermentation-monitor

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Linux/macOS:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 1.2 Local Execution

```bash
# Navigate to source directory
cd src/python

# Run the application
python main.py
```

### 1.3 Access Interface

Open browser to `http://localhost:5000`

### 1.4 Camera Setup

The system will automatically detect the default camera (usually index 0). If you have multiple cameras, you may need to modify the camera index in the code.

## Option 2: Raspberry Pi Deployment

### 2.1 Prepare Raspberry Pi

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install system dependencies
sudo apt install -y python3 python3-pip python3-venv git \
    python3-opencv libopencv-dev

# Enable camera (if using Raspberry Pi Camera Module)
sudo raspi-config
# Select Interface Options > Camera > Enable

# Reboot system
sudo reboot
```

### 2.2 Deploy Application

SSH into the Raspberry Pi and run:

```bash
# Clone the project
git clone https://github.com/Alexliu13483/fermentation-monitor.git
cd fermentation-monitor

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2.3 Create System Service

```bash
# Create service file
sudo nano /etc/systemd/system/fermentation-monitor.service
```

Add the following content:

```ini
[Unit]
Description=Fermentation Monitor Service
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/fermentation-monitor/src/python
Environment=PATH=/home/pi/fermentation-monitor/.venv/bin
ExecStart=/home/pi/fermentation-monitor/.venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
# Enable service
sudo systemctl enable fermentation-monitor.service

# Start service
sudo systemctl start fermentation-monitor.service

# Check status
sudo systemctl status fermentation-monitor.service
```

### 2.4 Access Interface

Open browser to `http://[raspberry-pi-ip]:5000`

## Option 3: Cross-Platform Deployment

### 3.1 Windows Deployment

**Prerequisites:**
- Windows 10/11
- Python 3.8+ from python.org
- USB camera or built-in webcam

```powershell
# Clone the project
git clone https://github.com/Alexliu13483/fermentation-monitor.git
cd fermentation-monitor

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
cd src\python
python main.py
```

### 3.2 macOS Deployment

**Prerequisites:**
- macOS 10.15+
- Python 3.8+ (via Homebrew recommended)
- Built-in camera or USB camera

```bash
# Install Python (if needed)
brew install python

# Clone the project
git clone https://github.com/Alexliu13483/fermentation-monitor.git
cd fermentation-monitor

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
cd src/python
python main.py
```

### 3.3 Linux Deployment

**Prerequisites:**
- Ubuntu 18.04+, Debian 10+, or equivalent
- Python 3.8+
- USB camera or built-in webcam

```bash
# Install system dependencies
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git python3-opencv

# Clone the project
git clone https://github.com/Alexliu13483/fermentation-monitor.git
cd fermentation-monitor

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
cd src/python
python main.py
```

## Camera Setup

### USB Camera

1. **Connect USB camera** to any available USB port
2. **Verify detection**:
   ```bash
   # Linux:
   ls /dev/video*
   
   # Windows:
   # Check Device Manager under "Cameras" or "Imaging devices"
   
   # macOS:
   # System Preferences > Security & Privacy > Camera
   ```
3. **Test camera** (optional):
   ```bash
   # Linux with OpenCV:
   python3 -c "import cv2; cap = cv2.VideoCapture(0); print('Camera works!' if cap.isOpened() else 'Camera failed')"
   ```

### Raspberry Pi Camera Module

1. **Connect camera module** to CSI port
2. **Enable camera interface**:
   ```bash
   sudo raspi-config
   # Interface Options > Camera > Enable
   sudo reboot
   ```
3. **Test camera**:
   ```bash
   libcamera-hello --timeout 2000
   ```

### Camera Configuration

The system automatically detects available cameras. To use a specific camera:

1. **Find camera index**:
   ```python
   import cv2
   for i in range(5):
       cap = cv2.VideoCapture(i)
       if cap.isOpened():
           print(f"Camera {i} available")
           cap.release()
   ```

2. **Modify camera index** in `src/python/image_processing/fermentation_analyzer.py`:
   ```python
   self.camera = cv2.VideoCapture(1)  # Change 0 to desired index
   ```

## Network Configuration

### WiFi Setup (Raspberry Pi OS)

```bash
# Edit WiFi configuration
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

# Add network configuration
network={
    ssid="YourWiFiName"
    psk="YourWiFiPassword"
}

# Restart networking service
sudo systemctl restart dhcpcd
```

### Static IP Setup

```bash
# Edit dhcpcd.conf
sudo nano /etc/dhcpcd.conf

# Add static IP configuration
interface wlan0
static ip_address=192.168.1.100/24
static routers=192.168.1.1
static domain_name_servers=8.8.8.8 8.8.4.4
```

### Firewall Configuration

```bash
# Install UFW (Ubuntu/Debian)
sudo apt install ufw

# Configure basic rules
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH
sudo ufw allow ssh

# Allow web interface
sudo ufw allow 5000

# Enable firewall
sudo ufw enable
```

## Service Management (Linux/Raspberry Pi)

### Start/Stop Service

```bash
# Start service
sudo systemctl start fermentation-monitor.service

# Stop service
sudo systemctl stop fermentation-monitor.service

# Restart service
sudo systemctl restart fermentation-monitor.service

# Enable auto-start on boot
sudo systemctl enable fermentation-monitor.service

# Disable auto-start on boot
sudo systemctl disable fermentation-monitor.service
```

### Check Service Status

```bash
# Service status
sudo systemctl status fermentation-monitor.service

# Real-time logs
sudo journalctl -u fermentation-monitor.service -f

# Historical logs
sudo journalctl -u fermentation-monitor.service --since "1 hour ago"
```

### Manual Execution (All Platforms)

```bash
# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate     # Windows

# Navigate to source directory
cd src/python

# Run application manually
python main.py
```

## Performance Optimization

### System Optimization (Raspberry Pi)

```bash
# GPU memory allocation
echo 'gpu_mem=128' | sudo tee -a /boot/config.txt

# CPU frequency setting
echo 'arm_freq=1800' | sudo tee -a /boot/config.txt

# Enable 64-bit kernel
echo 'arm_64bit=1' | sudo tee -a /boot/config.txt
```

### Application Configuration

Edit configuration in your application code:

```python
# In src/python/image_processing/fermentation_analyzer.py
class FermentationAnalyzer:
    def __init__(self):
        # Adjust camera resolution for performance
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.camera.set(cv2.CAP_PROP_FPS, 15)
        
        # Analysis interval (seconds)
        self.analysis_interval = 300  # 5 minutes
```

## Legacy System Sections (For Reference)

### System Backup (Raspberry Pi)

```bash
# Create system backup
sudo dd if=/dev/mmcblk0 of=/path/to/backup.img bs=1M status=progress

# Compress backup
gzip /path/to/backup.img
```

### Data Backup

```bash
# Backup database
sqlite3 fermentation.db .dump > backup.sql

# Backup configuration
tar -czf config_backup.tar.gz config/
```

### System Recovery

```bash
# Restore from backup
sudo dd if=/path/to/backup.img.gz bs=1M status=progress | gunzip > /dev/mmcblk0
```

## Troubleshooting

### Common Issues

1. **Service Won't Start**
   ```bash
   # Check logs
   sudo journalctl -u fermentation-monitor.service
   
   # Check permissions
   ls -la /home/pi/fermentation-monitor/
   
   # Check Python path
   which python3
   ```

2. **Camera Access Failed**
   ```bash
   # Check camera devices
   ls /dev/video*
   
   # Test camera (Linux)
   python3 -c "import cv2; print('OK' if cv2.VideoCapture(0).isOpened() else 'FAIL')"
   
   # Check camera permissions
   groups $USER
   ```

3. **Python Dependencies Issues**
   ```bash
   # Reinstall dependencies
   pip install --upgrade --force-reinstall -r requirements.txt
   
   # Check OpenCV installation
   python3 -c "import cv2; print(cv2.__version__)"
   ```

4. **Network Connection Issues**
   ```bash
   # Check network status
   ip addr show
   
   # Test connectivity
   ping google.com
   
   # Check if port 5000 is accessible
   netstat -tlnp | grep 5000
   ```

5. **Performance Issues**
   ```bash
   # Check system resources
   top
   free -h
   df -h
   
   # Monitor camera performance
   python3 -c "import cv2; cap=cv2.VideoCapture(0); print(f'FPS: {cap.get(cv2.CAP_PROP_FPS)}, Resolution: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}x{cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}')"
   ```

### Log Analysis

```bash
# Application logs (if using file logging)
tail -f app.log

# System logs (Linux)
sudo journalctl -f

# Kernel messages
dmesg | tail -20
```

### Performance Monitoring

```bash
# CPU usage
top

# Memory usage
free -h

# Disk usage
df -h

# Temperature monitoring (Raspberry Pi)
vcgencmd measure_temp
```

## Security Configuration

### SSH Security (Linux/Raspberry Pi)

```bash
# Change default password
passwd

# Disable password login (use SSH keys)
sudo nano /etc/ssh/sshd_config
# Set: PasswordAuthentication no

# Restart SSH service
sudo systemctl restart ssh
```

### Firewall Configuration

```bash
# Install UFW (Ubuntu/Debian)
sudo apt install ufw

# Basic rules
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH
sudo ufw allow ssh

# Allow web interface
sudo ufw allow 5000

# Enable firewall
sudo ufw enable
```

## Maintenance

### Regular Maintenance Tasks

1. **Weekly**:
   - Check service status
   - Review system logs
   - Clean temporary files
   - Monitor disk space

2. **Monthly**:
   - System updates
   - Database backup
   - Performance monitoring
   - Security updates

3. **Quarterly**:
   - Full system backup
   - Hardware cleaning (for Raspberry Pi)
   - Security review
   - Documentation updates

### Automated Maintenance Script

```bash
#!/bin/bash
# maintenance.sh

# Clean system logs (Linux)
if command -v journalctl &> /dev/null; then
    sudo journalctl --vacuum-time=30d
fi

# Clean temporary files
find /tmp -name "*.tmp" -mtime +7 -delete 2>/dev/null

# Database optimization (if SQLite database exists)
if [ -f "fermentation.db" ]; then
    sqlite3 fermentation.db "VACUUM;"
fi

# Check disk space
df -h | awk '$5 > 80 {print "Warning: " $1 " is " $5 " full"}'

# Update Python packages
source .venv/bin/activate 2>/dev/null || source .venv/Scripts/activate 2>/dev/null
pip list --outdated
```

### Backup and Recovery

```bash
# Backup database
cp fermentation.db fermentation_backup_$(date +%Y%m%d).db

# Backup configuration
tar -czf config_backup_$(date +%Y%m%d).tar.gz config/

# Full project backup
tar -czf fermentation_monitor_backup_$(date +%Y%m%d).tar.gz \
    --exclude='.venv' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    .
```

### Performance Monitoring

```bash
# Monitor system resources
echo "=== System Resources ==="
echo "CPU Usage: $(top -bn1 | grep 'Cpu(s)' | awk '{print $2}' | cut -d'%' -f1)"
echo "Memory: $(free -h | awk 'NR==2{printf "%.1f%%", $3*100/$2 }')"
echo "Disk: $(df -h / | awk 'NR==2{print $5}')"

# Check camera status
echo "=== Camera Status ==="
python3 -c "import cv2; cap=cv2.VideoCapture(0); print('Camera: OK' if cap.isOpened() else 'Camera: FAIL'); cap.release()"

# Check web service
echo "=== Web Service ==="
curl -s -o /dev/null -w "%{http_code}" http://localhost:5000 || echo "Service not responding"
```