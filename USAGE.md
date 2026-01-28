# KeyMeter Usage Guide

This guide covers various usage scenarios and advanced configurations for KeyMeter.

## Table of Contents

1. [Basic Usage](#basic-usage)
2. [Service Management](#service-management)
3. [Manual Operation](#manual-operation)
4. [Configuration](#configuration)
5. [Log Management](#log-management)
6. [Advanced Scenarios](#advanced-scenarios)
7. [Integration Examples](#integration-examples)

## Basic Usage

### Running as a System Service (Recommended)

This is the recommended way to run KeyMeter for continuous background capture.

```bash
# Enable service to start on boot
sudo systemctl enable keymeter@$USER

# Start the service
sudo systemctl start keymeter@$USER

# Check status
sudo systemctl status keymeter@$USER
```

### Viewing Captured Data

```bash
# List all capture files
ls -lh ~/keymeter_logs/

# View the latest capture file
tail -f ~/keymeter_logs/keystrokes_*.txt | tail -n 1

# View all captures from today
grep "$(date +%Y-%m-%d)" ~/keymeter_logs/keystrokes_*.txt

# Count keystrokes
wc -l ~/keymeter_logs/keystrokes_*.txt
```

## Service Management

### Starting and Stopping

```bash
# Start
sudo systemctl start keymeter@$USER

# Stop
sudo systemctl stop keymeter@$USER

# Restart
sudo systemctl restart keymeter@$USER

# Status
sudo systemctl status keymeter@$USER
```

### Enabling Auto-Start

```bash
# Enable (start on boot)
sudo systemctl enable keymeter@$USER

# Disable (don't start on boot)
sudo systemctl disable keymeter@$USER

# Check if enabled
systemctl is-enabled keymeter@$USER
```

### Viewing Service Logs

```bash
# View recent logs
sudo journalctl -u keymeter@$USER

# Follow logs in real-time
sudo journalctl -u keymeter@$USER -f

# View logs from today
sudo journalctl -u keymeter@$USER --since today

# View last 100 lines
sudo journalctl -u keymeter@$USER -n 100
```

## Manual Operation

### Running in Foreground

Useful for testing or temporary capture:

```bash
# Default settings (output to ~/keymeter_logs)
python3 keymeter.py

# Custom output directory
python3 keymeter.py --output-dir /tmp/test_capture

# Custom log file
python3 keymeter.py --log-file /tmp/keymeter.log

# Combined
python3 keymeter.py --output-dir /tmp/capture --log-file /tmp/app.log
```

Press Ctrl+C to stop.

### Running as Daemon (Background)

```bash
# Run as daemon
python3 keymeter.py --daemon

# Check if running
ps aux | grep keymeter

# Stop daemon
pkill -f keymeter.py
```

## Configuration

### Changing Output Directory

#### For Service

Edit the service file:

```bash
sudo nano /etc/systemd/system/keymeter@.service
```

Change `ExecStart` line to include output directory:

```ini
ExecStart=/usr/bin/python3 /opt/keymeter/keymeter.py --output-dir /custom/path
```

Reload and restart:

```bash
sudo systemctl daemon-reload
sudo systemctl restart keymeter@$USER
```

#### For Manual Run

```bash
python3 keymeter.py --output-dir /path/to/logs
```

### File Naming

Files are automatically named with timestamps:
- Format: `keystrokes_YYYYMMDD_HHMMSS.txt`
- Example: `keystrokes_20240128_143022.txt`

## Log Management

### Understanding Output Format

Each line in the capture file contains:

```
TIMESTAMP    KEY
```

Example:
```
2024-01-28T14:30:22.123456    h
2024-01-28T14:30:22.234567    e
2024-01-28T14:30:22.345678    l
2024-01-28T14:30:22.456789    l
2024-01-28T14:30:22.567890    o
```

### Analyzing Captured Data

#### Count total keystrokes
```bash
grep -v "^#" ~/keymeter_logs/keystrokes_*.txt | wc -l
```

#### Find specific keys
```bash
grep "enter" ~/keymeter_logs/keystrokes_*.txt
```

#### Extract only timestamps
```bash
awk '{print $1}' ~/keymeter_logs/keystrokes_*.txt
```

#### Extract only keys
```bash
awk '{print $2}' ~/keymeter_logs/keystrokes_*.txt
```

### Cleaning Old Logs

```bash
# Remove logs older than 7 days
find ~/keymeter_logs -name "keystrokes_*.txt" -mtime +7 -delete

# Archive logs older than 30 days
find ~/keymeter_logs -name "keystrokes_*.txt" -mtime +30 -exec gzip {} \;
```

### Setting Up Log Rotation

Create a logrotate configuration:

```bash
sudo nano /etc/logrotate.d/keymeter
```

Add:

```
/home/*/keymeter_logs/keystrokes_*.txt {
    daily
    rotate 7
    compress
    missingok
    notifempty
    create 0600 $USER $USER
}
```

## Advanced Scenarios

### Multi-User Setup

Each user can run their own KeyMeter instance:

```bash
# For user1
sudo systemctl enable keymeter@user1
sudo systemctl start keymeter@user1

# For user2
sudo systemctl enable keymeter@user2
sudo systemctl start keymeter@user2
```

### Custom Analysis Script

Create a script to analyze keystrokes:

```python
#!/usr/bin/env python3
import sys
from collections import Counter
from pathlib import Path

def analyze_keystrokes(filepath):
    """Analyze keystroke file."""
    keys = []
    
    with open(filepath) as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            
            parts = line.strip().split('\t')
            if len(parts) == 2:
                keys.append(parts[1])
    
    # Count keys
    counter = Counter(keys)
    
    print(f"Total keystrokes: {len(keys)}")
    print(f"\nTop 10 keys:")
    for key, count in counter.most_common(10):
        print(f"  {key}: {count}")

if __name__ == '__main__':
    analyze_keystrokes(sys.argv[1])
```

Usage:
```bash
python3 analyze.py ~/keymeter_logs/keystrokes_20240128_143022.txt
```

### Secure Storage

For sensitive environments, encrypt the output directory:

```bash
# Install encfs
sudo apt-get install encfs

# Create encrypted directory
mkdir ~/keymeter_secure
mkdir ~/keymeter_logs_encrypted
encfs ~/keymeter_secure ~/keymeter_logs_encrypted

# Run KeyMeter with encrypted directory
python3 keymeter.py --output-dir ~/keymeter_logs_encrypted
```

### Network Storage

Store logs on a network drive:

```bash
# Mount network share
sudo mount -t cifs //server/share /mnt/keymeter_logs -o credentials=/etc/samba/credentials

# Run KeyMeter
python3 keymeter.py --output-dir /mnt/keymeter_logs
```

## Integration Examples

### With Cron

Schedule analysis tasks:

```bash
# Add to crontab
crontab -e

# Run analysis daily at midnight
0 0 * * * python3 /path/to/analyze.py ~/keymeter_logs/keystrokes_*.txt > ~/keymeter_reports/$(date +\%Y\%m\%d).txt
```

### With Monitoring Tools

Monitor KeyMeter status with Nagios, Zabbix, etc:

```bash
#!/bin/bash
# Check if KeyMeter is running
if systemctl is-active --quiet keymeter@$USER; then
    echo "OK: KeyMeter is running"
    exit 0
else
    echo "CRITICAL: KeyMeter is not running"
    exit 2
fi
```

### With Backup Solutions

Backup logs with rsync:

```bash
# Backup to remote server
rsync -avz ~/keymeter_logs/ backup-server:/backups/keymeter/

# Backup to external drive
rsync -avz ~/keymeter_logs/ /mnt/backup/keymeter/
```

## Programmatic Usage

### Python API

```python
from keymeter import KeyMeter

# Create instance
km = KeyMeter(output_dir="/tmp/logs")

# Start capturing
km.start()

# ... KeyMeter runs in background ...

# Stop capturing
km.stop()

# Or use context manager
with KeyMeter(output_dir="/tmp/logs") as km:
    # Capture happens automatically
    pass  # Auto-stops on exit
```

See [example.py](example.py) for more examples.

## Troubleshooting

### High CPU Usage

If KeyMeter is using too much CPU:

1. Check for errors in logs: `cat ~/keymeter_logs/keymeter.log`
2. Ensure pynput is up to date: `pip3 install --upgrade pynput`
3. Restart the service: `sudo systemctl restart keymeter@$USER`

### Disk Space Issues

Monitor disk usage:

```bash
# Check log directory size
du -sh ~/keymeter_logs

# Set up automatic cleanup (keep last 7 days only)
echo "0 2 * * * find ~/keymeter_logs -name 'keystrokes_*.txt' -mtime +7 -delete" | crontab -
```

### Permission Issues

Fix permissions:

```bash
# Ensure correct ownership
chown -R $USER:$USER ~/keymeter_logs

# Set correct permissions
chmod 700 ~/keymeter_logs
chmod 600 ~/keymeter_logs/*.txt
```

## Best Practices

1. **Regular Backups**: Backup log files regularly
2. **Disk Monitoring**: Monitor disk space usage
3. **Log Rotation**: Set up log rotation to prevent disk fill
4. **Security**: Keep logs secure and encrypted if needed
5. **Compliance**: Ensure usage complies with applicable laws
6. **Testing**: Test recovery procedures regularly
7. **Documentation**: Document any custom configurations

## Additional Resources

- [README.md](README.md) - Main documentation
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [example.py](example.py) - Usage examples
- [test_keymeter.py](test_keymeter.py) - Test suite

For issues and questions, please visit the GitHub repository.
