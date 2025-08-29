#!/bin/bash

# Development Environment Setup Script
# Sets up local development environment for fermentation monitor

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    log_error "Please don't run this script as root"
    exit 1
fi

log_info "Setting up Fermentation Monitor development environment..."

# Update system packages
log_step "Updating system packages..."
sudo apt-get update

# Install build essentials
log_step "Installing build essentials..."
sudo apt-get install -y \
    build-essential \
    cmake \
    git \
    pkg-config \
    wget \
    curl \
    gawk \
    diffstat \
    unzip \
    texinfo \
    gcc-multilib \
    chrpath \
    socat \
    cpio \
    python3 \
    python3-pip \
    python3-pexpect \
    xz-utils \
    debianutils \
    iputils-ping \
    python3-git \
    python3-jinja2 \
    libegl1-mesa \
    libsdl1.2-dev \
    pylint3 \
    xterm \
    python3-subunit \
    mesa-common-dev \
    zstd \
    liblz4-tool

# Install OpenCV dependencies
log_step "Installing OpenCV dependencies..."
sudo apt-get install -y \
    libopencv-dev \
    python3-opencv \
    libopencv-contrib-dev \
    libgtk-3-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    gfortran \
    openexr \
    libatlas-base-dev \
    python3-dev \
    python3-numpy \
    libtbb2 \
    libtbb-dev \
    libdc1394-22-dev

# Install Python dependencies
log_step "Installing Python dependencies..."
pip3 install --user \
    flask \
    opencv-python \
    numpy \
    pillow \
    sqlite3 \
    RPi.GPIO \
    w1thermsensor \
    Adafruit-DHT

# Create virtual environment for development
log_step "Creating Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip

# Install Python packages in virtual environment
pip install \
    flask \
    opencv-python \
    numpy \
    pillow \
    pytest \
    pytest-cov \
    black \
    flake8

# Create development directories
log_step "Creating development directories..."
mkdir -p /tmp/fermentation-monitor/data
mkdir -p logs

# Set up git hooks (if in git repo)
if [ -d ".git" ]; then
    log_step "Setting up git hooks..."
    cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Run Python code formatting and linting
source venv/bin/activate 2>/dev/null || true
black src/python/ --check --diff
flake8 src/python/ --max-line-length=88
EOF
    chmod +x .git/hooks/pre-commit
fi

# Create development configuration
log_step "Creating development configuration..."
cat > config/dev.conf << EOF
# Development Configuration
[database]
path = /tmp/fermentation-monitor/data/fermentation.db

[camera]
device = 0
width = 1920
height = 1080
fps = 30

[sensors]
temperature_enabled = false
humidity_enabled = false

[web]
host = 127.0.0.1
port = 5000
debug = true

[logging]
level = DEBUG
file = logs/fermentation-monitor.log
EOF

# Create systemd service for development
log_step "Creating systemd service template..."
mkdir -p systemd
cat > systemd/fermentation-monitor.service << EOF
[Unit]
Description=Fermentation Monitor Service
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/opt/fermentation-monitor
Environment=PYTHONPATH=/opt/fermentation-monitor/python
ExecStart=/usr/bin/python3 /opt/fermentation-monitor/python/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Make scripts executable
chmod +x scripts/*.sh

# Build C++ components for development
log_step "Building C++ components..."
if [ ! -d "build" ]; then
    mkdir build
fi

cd build
cmake ../src/cpp
make -j$(nproc)
cd ..

log_info "Development environment setup completed!"
log_info ""
log_info "To activate the virtual environment: source venv/bin/activate"
log_info "To run the application: python3 src/python/main.py"
log_info "To build Yocto image: ./scripts/build-yocto.sh"
log_info ""
log_warn "For Raspberry Pi GPIO access, you may need to:"
log_warn "1. Add your user to the gpio group: sudo usermod -a -G gpio \$USER"
log_warn "2. Install Raspberry Pi specific packages on target device"