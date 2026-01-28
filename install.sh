#!/bin/bash
# KeyMeter installation script for Ubuntu

set -e

echo "KeyMeter Installation Script"
echo "============================"
echo

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo "Please do not run this script as root or with sudo."
    echo "The script will ask for sudo password when needed."
    exit 1
fi

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oP '(?<=Python )\d+\.\d+')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 6 ]); then
    echo "Error: Python 3.6 or higher is required. Found: $PYTHON_VERSION"
    exit 1
fi

echo "Python version OK: $PYTHON_VERSION"
echo

# Install system dependencies
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv

# Create installation directory
INSTALL_DIR="/opt/keymeter"
echo "Creating installation directory: $INSTALL_DIR"
sudo mkdir -p $INSTALL_DIR
sudo cp keymeter.py $INSTALL_DIR/
sudo cp requirements.txt $INSTALL_DIR/

# Install Python dependencies
echo "Installing Python dependencies..."
sudo pip3 install -r requirements.txt

# Create output directory for current user
OUTPUT_DIR="$HOME/keymeter_logs"
mkdir -p $OUTPUT_DIR
echo "Created output directory: $OUTPUT_DIR"

# Install systemd service
echo "Installing systemd service..."
SERVICE_FILE="/etc/systemd/system/keymeter@.service"
sudo cp keymeter.service $SERVICE_FILE

# Set permissions
sudo chmod 755 $INSTALL_DIR/keymeter.py
sudo chmod 644 $SERVICE_FILE

echo
echo "Installation complete!"
echo
echo "To start KeyMeter for your user, run:"
echo "  sudo systemctl enable keymeter@$USER"
echo "  sudo systemctl start keymeter@$USER"
echo
echo "To check status:"
echo "  sudo systemctl status keymeter@$USER"
echo
echo "Keyboard strokes will be saved to: $OUTPUT_DIR"
echo
echo "Note: KeyMeter requires appropriate permissions to capture keyboard events."
echo "You may need to add your user to the 'input' group:"
echo "  sudo usermod -a -G input $USER"
echo "  (then log out and log back in)"
echo
