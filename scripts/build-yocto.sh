#!/bin/bash

# Fermentation Monitor - Yocto Build Script
# Target: Raspberry Pi 4

set -e

# Configuration
YOCTO_VERSION="scarthgap"
BUILD_DIR="build-rpi4"
MACHINE="raspberrypi4-64"
DISTRO="poky"
IMAGE_NAME="fermentation-monitor-image"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running from correct directory
if [ ! -d "meta-fermentation-monitor" ]; then
    log_error "Please run this script from the fermentation-monitor root directory"
    exit 1
fi

log_info "Starting Yocto build for Fermentation Monitor"
log_info "Target: $MACHINE"
log_info "Image: $IMAGE_NAME"

# Initialize Yocto environment
if [ ! -d "poky" ]; then
    log_info "Cloning Yocto poky repository..."
    git clone -b $YOCTO_VERSION https://git.yoctoproject.org/poky.git
fi

if [ ! -d "meta-openembedded" ]; then
    log_info "Cloning meta-openembedded..."
    git clone -b $YOCTO_VERSION https://github.com/openembedded/meta-openembedded.git
fi

if [ ! -d "meta-raspberrypi" ]; then
    log_info "Cloning meta-raspberrypi..."
    git clone -b $YOCTO_VERSION https://github.com/agherzan/meta-raspberrypi.git
fi

# Source the environment
log_info "Setting up build environment..."
cd poky
source oe-init-build-env ../$BUILD_DIR

# Configure bblayers.conf
log_info "Configuring layers..."
cat > conf/bblayers.conf << EOF
# POKY_BBLAYERS_CONF_VERSION is increased each time build/conf/bblayers.conf
# changes incompatibly
POKY_BBLAYERS_CONF_VERSION = "2"

BBPATH = "\${TOPDIR}"
BBFILES ?= ""

BBLAYERS ?= " \\
  \${TOPDIR}/../poky/meta \\
  \${TOPDIR}/../poky/meta-poky \\
  \${TOPDIR}/../poky/meta-yocto-bsp \\
  \${TOPDIR}/../meta-openembedded/meta-oe \\
  \${TOPDIR}/../meta-openembedded/meta-python \\
  \${TOPDIR}/../meta-openembedded/meta-networking \\
  \${TOPDIR}/../meta-openembedded/meta-multimedia \\
  \${TOPDIR}/../meta-raspberrypi \\
  \${TOPDIR}/../meta-fermentation-monitor \\
"
EOF

# Configure local.conf
log_info "Configuring build settings..."
cat >> conf/local.conf << EOF

# Fermentation Monitor specific settings
MACHINE = "$MACHINE"
DISTRO = "$DISTRO"

# Enable camera support
GPU_MEM = "128"
ENABLE_UART = "1"
ENABLE_I2C = "1" 
ENABLE_SPI = "1"

# Package management
EXTRA_IMAGE_FEATURES += "package-management"

# Enable systemd
DISTRO_FEATURES:append = " systemd"
VIRTUAL-RUNTIME_init_manager = "systemd"

# WiFi support
IMAGE_INSTALL:append = " linux-firmware-rpidistro-bcm43430 linux-firmware-rpidistro-bcm43455"

# Development tools (optional, remove for production)
EXTRA_IMAGE_FEATURES += "tools-debug tools-profile ssh-server-openssh"

# Parallel build settings
BB_NUMBER_THREADS = "$(nproc)"
PARALLEL_MAKE = "-j $(nproc)"

# Disk space monitoring
BB_DISKMON_DIRS = "\\
    STOPTASKS,\${TMPDIR},1G,100K \\
    STOPTASKS,\${DL_DIR},1G,100K \\
    STOPTASKS,\${SSTATE_DIR},1G,100K \\
    STOPTASKS,/tmp,100M,100K \\
    ABORT,\${TMPDIR},100M,1K \\
    ABORT,\${DL_DIR},100M,1K \\
    ABORT,\${SSTATE_DIR},100M,1K \\
    ABORT,/tmp,10M,1K"
EOF

# Start the build
log_info "Starting bitbake build..."
log_warn "This may take several hours depending on your system"

bitbake $IMAGE_NAME

if [ $? -eq 0 ]; then
    log_info "Build completed successfully!"
    log_info "Image location: tmp/deploy/images/$MACHINE/"
    log_info "Flash to SD card with:"
    log_info "sudo dd if=tmp/deploy/images/$MACHINE/$IMAGE_NAME-$MACHINE.rootfs.wic.bz2 of=/dev/sdX bs=1M status=progress"
else
    log_error "Build failed!"
    exit 1
fi