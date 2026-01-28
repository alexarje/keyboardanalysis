#!/bin/bash
# KeyMeter uninstallation script

set -e

echo "KeyMeter Uninstallation Script"
echo "=============================="
echo

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo "Please do not run this script as root or with sudo."
    echo "The script will ask for sudo password when needed."
    exit 1
fi

# Stop and disable service
echo "Stopping and disabling KeyMeter service..."
sudo systemctl stop keymeter@$USER 2>/dev/null || true
sudo systemctl disable keymeter@$USER 2>/dev/null || true

# Remove systemd service file
echo "Removing systemd service file..."
sudo rm -f /etc/systemd/system/keymeter@.service

# Reload systemd
sudo systemctl daemon-reload

# Remove installation directory
echo "Removing installation directory..."
sudo rm -rf /opt/keymeter

echo
echo "Uninstallation complete!"
echo
echo "Note: Your captured keyboard logs in ~/keymeter_logs have NOT been deleted."
echo "If you want to remove them, run: rm -rf ~/keymeter_logs"
echo
