#!/bin/bash

# Deployment script for Raspberry Pi 4
# Deploys the fermentation monitor application to target device

set -e

# Default configuration
TARGET_HOST=""
TARGET_USER="pi"
TARGET_PATH="/opt/fermentation-monitor"
SSH_KEY=""

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

usage() {
    echo "Usage: $0 -h <target_host> [-u <user>] [-k <ssh_key>] [-p <path>]"
    echo ""
    echo "Options:"
    echo "  -h <host>     Target Raspberry Pi IP address or hostname"
    echo "  -u <user>     SSH username (default: pi)"
    echo "  -k <key>      SSH private key file"
    echo "  -p <path>     Target installation path (default: /opt/fermentation-monitor)"
    echo ""
    echo "Examples:"
    echo "  $0 -h 192.168.1.100"
    echo "  $0 -h raspberrypi.local -u pi -k ~/.ssh/id_rsa"
}

# Parse command line arguments
while getopts "h:u:k:p:" opt; do
    case $opt in
        h) TARGET_HOST="$OPTARG" ;;
        u) TARGET_USER="$OPTARG" ;;
        k) SSH_KEY="$OPTARG" ;;
        p) TARGET_PATH="$OPTARG" ;;
        *) usage; exit 1 ;;
    esac
done

if [ -z "$TARGET_HOST" ]; then
    log_error "Target host is required"
    usage
    exit 1
fi

# SSH command builder
SSH_CMD="ssh"
SCP_CMD="scp"
if [ -n "$SSH_KEY" ]; then
    SSH_CMD="ssh -i $SSH_KEY"
    SCP_CMD="scp -i $SSH_KEY"
fi

log_info "Deploying Fermentation Monitor to $TARGET_USER@$TARGET_HOST:$TARGET_PATH"

# Test SSH connection
log_step "Testing SSH connection..."
$SSH_CMD -o ConnectTimeout=10 $TARGET_USER@$TARGET_HOST "echo 'Connection successful'" || {
    log_error "Cannot connect to target host"
    exit 1
}

# Create target directories
log_step "Creating target directories..."
$SSH_CMD $TARGET_USER@$TARGET_HOST "sudo mkdir -p $TARGET_PATH/{bin,python,web,data,logs}"
$SSH_CMD $TARGET_USER@$TARGET_HOST "sudo mkdir -p $TARGET_PATH/python/{sensors,image_processing,data_storage,web_api}"
$SSH_CMD $TARGET_USER@$TARGET_HOST "sudo chown -R $TARGET_USER:$TARGET_USER $TARGET_PATH"

# Build C++ components locally
log_step "Building C++ components..."
if [ ! -d "build" ]; then
    mkdir build
fi

cd build
cmake ../src/cpp -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
cd ..

# Deploy C++ binary
log_step "Deploying C++ binary..."
$SCP_CMD build/fermentation_monitor $TARGET_USER@$TARGET_HOST:$TARGET_PATH/bin/

# Deploy Python code
log_step "Deploying Python application..."
$SCP_CMD -r src/python/* $TARGET_USER@$TARGET_HOST:$TARGET_PATH/python/

# Deploy web interface
log_step "Deploying web interface..."
$SCP_CMD -r src/web/* $TARGET_USER@$TARGET_HOST:$TARGET_PATH/web/

# Deploy systemd service
log_step "Deploying systemd service..."
$SCP_CMD systemd/fermentation-monitor.service $TARGET_USER@$TARGET_HOST:/tmp/
$SSH_CMD $TARGET_USER@$TARGET_HOST "sudo mv /tmp/fermentation-monitor.service /etc/systemd/system/"
$SSH_CMD $TARGET_USER@$TARGET_HOST "sudo systemctl daemon-reload"

# Install Python dependencies on target
log_step "Installing Python dependencies on target..."
$SSH_CMD $TARGET_USER@$TARGET_HOST "sudo apt-get update"
$SSH_CMD $TARGET_USER@$TARGET_HOST "sudo apt-get install -y python3-pip python3-opencv python3-flask python3-numpy python3-pil"

# Install Raspberry Pi specific packages
log_step "Installing Raspberry Pi specific packages..."
$SSH_CMD $TARGET_USER@$TARGET_HOST "pip3 install --user RPi.GPIO w1thermsensor Adafruit-DHT" || {
    log_warn "Some Raspberry Pi packages may not be available in this environment"
}

# Set up camera permissions
log_step "Setting up camera permissions..."
$SSH_CMD $TARGET_USER@$TARGET_HOST "sudo usermod -a -G video $TARGET_USER"

# Enable and start service
log_step "Enabling and starting service..."
$SSH_CMD $TARGET_USER@$TARGET_HOST "sudo systemctl enable fermentation-monitor.service"
$SSH_CMD $TARGET_USER@$TARGET_HOST "sudo systemctl restart fermentation-monitor.service"

# Check service status
sleep 3
SERVICE_STATUS=$($SSH_CMD $TARGET_USER@$TARGET_HOST "sudo systemctl is-active fermentation-monitor.service" || echo "failed")

if [ "$SERVICE_STATUS" = "active" ]; then
    log_info "Deployment completed successfully!"
    log_info "Service is running on $TARGET_HOST"
    log_info "Web interface available at: http://$TARGET_HOST:5000"
else
    log_warn "Service deployment completed, but service is not running"
    log_warn "Check logs with: sudo systemctl status fermentation-monitor.service"
fi

# Display useful commands
log_info ""
log_info "Useful commands for managing the service:"
log_info "  Check status: sudo systemctl status fermentation-monitor.service"
log_info "  View logs:    sudo journalctl -u fermentation-monitor.service -f"
log_info "  Restart:      sudo systemctl restart fermentation-monitor.service"
log_info "  Stop:         sudo systemctl stop fermentation-monitor.service"