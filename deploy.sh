#!/bin/bash
#
# AWS GPU Static Server Deployment Script
#
# Usage: sudo ./deploy.sh [port] [project_path]
# Example: sudo ./deploy.sh 3000 /home/ubuntu/Codes/aws-gpu
#

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
DEFAULT_PORT=3000
DEFAULT_PATH="$(cd "$(dirname "$0")" && pwd)"
CURRENT_USER="${SUDO_USER:-$USER}"

# Parse arguments
PORT="${1:-$DEFAULT_PORT}"
PROJECT_PATH="${2:-$DEFAULT_PATH}"
SERVICE_NAME="aws-gpu-server"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}AWS GPU Server Deployment Script${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}❌ Please run as root (use sudo)${NC}"
    exit 1
fi

# Validate project path
if [ ! -f "$PROJECT_PATH/index.html" ]; then
    echo -e "${RED}❌ Error: index.html not found in $PROJECT_PATH${NC}"
    exit 1
fi

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} Python3 found: $(python3 --version)"
echo -e "${GREEN}✓${NC} Project path: $PROJECT_PATH"
echo -e "${GREEN}✓${NC} Port: $PORT"
echo -e "${GREEN}✓${NC} User: $CURRENT_USER"
echo ""

# Stop existing service if running
if systemctl is-active --quiet $SERVICE_NAME; then
    echo -e "${YELLOW}⏸${NC}  Stopping existing service..."
    systemctl stop $SERVICE_NAME
fi

# Create systemd service file
echo -e "${YELLOW}📝${NC} Creating systemd service file..."
cat > /etc/systemd/system/${SERVICE_NAME}.service << EOF
[Unit]
Description=AWS GPU Static Server
After=network.target

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$PROJECT_PATH
ExecStart=/usr/bin/python3 -m http.server $PORT
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

echo -e "${GREEN}✓${NC} Service file created at /etc/systemd/system/${SERVICE_NAME}.service"

# Reload systemd daemon
echo -e "${YELLOW}🔄${NC} Reloading systemd daemon..."
systemctl daemon-reload

# Enable service
echo -e "${YELLOW}⚙${NC}  Enabling service for auto-start on boot..."
systemctl enable $SERVICE_NAME

# Start service
echo -e "${YELLOW}🚀${NC} Starting service..."
systemctl start $SERVICE_NAME

# Wait a moment for service to start
sleep 2

# Check service status
if systemctl is-active --quiet $SERVICE_NAME; then
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}✅ Deployment successful!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "Service is running on port ${GREEN}$PORT${NC}"
    echo ""
    echo -e "Useful commands:"
    echo -e "  • Check status:    ${YELLOW}sudo systemctl status $SERVICE_NAME${NC}"
    echo -e "  • View logs:       ${YELLOW}sudo journalctl -u $SERVICE_NAME -f${NC}"
    echo -e "  • Restart service: ${YELLOW}sudo systemctl restart $SERVICE_NAME${NC}"
    echo -e "  • Stop service:    ${YELLOW}sudo systemctl stop $SERVICE_NAME${NC}"
    echo ""

    # Show current status
    echo -e "${YELLOW}Current status:${NC}"
    systemctl status $SERVICE_NAME --no-pager -l
else
    echo ""
    echo -e "${RED}========================================${NC}"
    echo -e "${RED}❌ Deployment failed!${NC}"
    echo -e "${RED}========================================${NC}"
    echo ""
    echo -e "Service failed to start. Check logs with:"
    echo -e "${YELLOW}sudo journalctl -u $SERVICE_NAME -n 50${NC}"
    exit 1
fi
