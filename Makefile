# Fermentation Monitor Makefile
# Provides convenient build targets for development and deployment

.PHONY: all clean build install dev-setup yocto-build deploy test help

# Default target
all: build

# Build C++ components
build:
	@echo "Building fermentation monitor..."
	@mkdir -p build
	@cd build && cmake -DCMAKE_BUILD_TYPE=Release .. && make -j$(nproc)

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	@rm -rf build/
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Development setup
dev-setup:
	@echo "Setting up development environment..."
	@chmod +x scripts/setup-dev.sh
	@./scripts/setup-dev.sh

# Build Yocto image
yocto-build:
	@echo "Building Yocto image for Raspberry Pi 4..."
	@chmod +x scripts/build-yocto.sh
	@./scripts/build-yocto.sh

# Deploy to Raspberry Pi (requires TARGET_HOST)
deploy:
	@if [ -z "$(TARGET_HOST)" ]; then \
		echo "Usage: make deploy TARGET_HOST=<raspberry-pi-ip>"; \
		echo "Example: make deploy TARGET_HOST=192.168.1.100"; \
		exit 1; \
	fi
	@echo "Deploying to $(TARGET_HOST)..."
	@chmod +x scripts/deploy.sh
	@./scripts/deploy.sh -h $(TARGET_HOST)

# Install locally (requires sudo)
install: build
	@echo "Installing fermentation monitor locally..."
	@sudo mkdir -p /opt/fermentation-monitor
	@sudo cp -r build/fermentation_monitor /opt/fermentation-monitor/bin/
	@sudo cp -r src/python /opt/fermentation-monitor/
	@sudo cp -r src/web /opt/fermentation-monitor/
	@sudo cp systemd/fermentation-monitor.service /etc/systemd/system/
	@sudo systemctl daemon-reload
	@echo "Installation complete. Enable with: sudo systemctl enable fermentation-monitor.service"

# Run Python tests
test:
	@echo "Running tests..."
	@if [ -d "venv" ]; then \
		. venv/bin/activate && python -m pytest tests/ -v; \
	else \
		python3 -m pytest tests/ -v; \
	fi

# Start development server
dev-run:
	@echo "Starting development server..."
	@cd src/python && python3 main.py

# Format Python code
format:
	@echo "Formatting Python code..."
	@if [ -d "venv" ]; then \
		. venv/bin/activate && black src/python/; \
	else \
		python3 -m black src/python/; \
	fi

# Lint Python code
lint:
	@echo "Linting Python code..."
	@if [ -d "venv" ]; then \
		. venv/bin/activate && flake8 src/python/ --max-line-length=88; \
	else \
		python3 -m flake8 src/python/ --max-line-length=88; \
	fi

# Create SD card image (requires Yocto build)
sdcard:
	@if [ ! -f "build-rpi4/tmp/deploy/images/raspberrypi4-64/fermentation-monitor-image-raspberrypi4-64.rootfs.wic.bz2" ]; then \
		echo "Yocto image not found. Run 'make yocto-build' first."; \
		exit 1; \
	fi
	@if [ -z "$(SD_DEVICE)" ]; then \
		echo "Usage: make sdcard SD_DEVICE=/dev/sdX"; \
		echo "Warning: This will overwrite the entire SD card!"; \
		exit 1; \
	fi
	@echo "Flashing SD card $(SD_DEVICE)..."
	@echo "WARNING: This will destroy all data on $(SD_DEVICE)"
	@read -p "Are you sure? (y/N) " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		sudo bmaptool copy build-rpi4/tmp/deploy/images/raspberrypi4-64/fermentation-monitor-image-raspberrypi4-64.rootfs.wic.bz2 $(SD_DEVICE); \
	fi

# Show help
help:
	@echo "Fermentation Monitor Build System"
	@echo ""
	@echo "Available targets:"
	@echo "  all          - Build C++ components (default)"
	@echo "  build        - Build C++ components"
	@echo "  clean        - Clean build artifacts"
	@echo "  dev-setup    - Set up development environment"
	@echo "  yocto-build  - Build complete Yocto image for RPi4"
	@echo "  deploy       - Deploy to Raspberry Pi (TARGET_HOST=ip)"
	@echo "  install      - Install locally (requires sudo)"
	@echo "  test         - Run Python tests"
	@echo "  dev-run      - Start development server"
	@echo "  format       - Format Python code with black"
	@echo "  lint         - Lint Python code with flake8"
	@echo "  sdcard       - Flash SD card (SD_DEVICE=/dev/sdX)"
	@echo "  help         - Show this help"
	@echo ""
	@echo "Examples:"
	@echo "  make dev-setup"
	@echo "  make build"
	@echo "  make deploy TARGET_HOST=192.168.1.100"
	@echo "  make sdcard SD_DEVICE=/dev/sdb"