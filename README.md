# KeyMeter - Keyboard Stroke Capture Tool

A lightweight keyboard stroke capture tool for Ubuntu that runs in the background and logs keyboard events to text files.

## Features

- **Background Operation**: Runs as a systemd service, always capturing in the background
- **Text File Logging**: Saves keyboard events to timestamped text files
- **Automatic Startup**: Configured to start automatically on system boot
- **Graceful Shutdown**: Handles system signals properly for clean exits
- **Timestamped Events**: Each keystroke is logged with ISO format timestamp
- **Low Overhead**: Minimal resource usage

## Requirements

- Ubuntu 18.04 or later (or any Linux distribution with systemd)
- Python 3.6 or higher
- Root/sudo access for installation

## Installation

1. Clone this repository:
```bash
git clone https://github.com/alexarje/keyboardanalysis.git
cd keyboardanalysis
```

2. Run the installation script:
```bash
chmod +x install.sh
./install.sh
```

3. Add your user to the input group (required for keyboard capture):
```bash
sudo usermod -a -G input $USER
```

4. Log out and log back in for the group change to take effect.

5. Enable and start the service:
```bash
sudo systemctl enable keymeter@$USER
sudo systemctl start keymeter@$USER
```

## Usage

### Managing the Service

Start KeyMeter:
```bash
sudo systemctl start keymeter@$USER
```

Stop KeyMeter:
```bash
sudo systemctl stop keymeter@$USER
```

Check status:
```bash
sudo systemctl status keymeter@$USER
```

Enable auto-start on boot:
```bash
sudo systemctl enable keymeter@$USER
```

Disable auto-start:
```bash
sudo systemctl disable keymeter@$USER
```

### Running Manually (Foreground)

You can also run KeyMeter manually without the service:

```bash
# Run in foreground (Ctrl+C to stop)
python3 keymeter.py

# Specify custom output directory
python3 keymeter.py --output-dir /path/to/logs

# Run as daemon (background) manually
python3 keymeter.py --daemon
```

### Command Line Options

- `-o, --output-dir`: Directory to store capture files (default: `~/keymeter_logs`)
- `-l, --log-file`: Path to application log file
- `-d, --daemon`: Run as daemon (background process)
- `-h, --help`: Show help message

## Output Files

KeyMeter creates timestamped text files in the output directory (default: `~/keymeter_logs/`):

- `keystrokes_YYYYMMDD_HHMMSS.txt`: Captured keyboard events
- `keymeter.log`: Application log file

### Output Format

Each line in the keystroke file contains:
```
ISO_TIMESTAMP    KEY
```

Example:
```
2024-01-28T10:30:45.123456    h
2024-01-28T10:30:45.234567    e
2024-01-28T10:30:45.345678    l
2024-01-28T10:30:45.456789    l
2024-01-28T10:30:45.567890    o
2024-01-28T10:30:45.678901    space
2024-01-28T10:30:45.789012    w
2024-01-28T10:30:45.890123    o
2024-01-28T10:30:46.001234    r
2024-01-28T10:30:46.112345    l
2024-01-28T10:30:46.223456    d
2024-01-28T10:30:46.334567    enter
```

## Uninstallation

To remove KeyMeter from your system:

```bash
chmod +x uninstall.sh
./uninstall.sh
```

Note: This will NOT delete your captured log files. To remove them manually:
```bash
rm -rf ~/keymeter_logs
```

## Privacy Notice

⚠️ **Important**: This tool captures ALL keyboard input on your system. Use responsibly and in compliance with applicable laws and regulations. Ensure you have proper authorization before capturing keyboard events.

The captured data includes:
- All typed characters
- Special keys (Enter, Space, Backspace, etc.)
- Timestamps for each keystroke

Make sure to:
- Secure the output files appropriately
- Only use on systems you own or have permission to monitor
- Comply with privacy laws and workplace policies

## Troubleshooting

### Permission Denied Errors

If you get permission errors when running KeyMeter:
1. Make sure you've added your user to the input group: `sudo usermod -a -G input $USER`
2. Log out and log back in
3. Verify group membership: `groups | grep input`

### Service Won't Start

Check the service logs:
```bash
sudo journalctl -u keymeter@$USER -f
```

Check the application log:
```bash
tail -f ~/keymeter_logs/keymeter.log
```

### KeyMeter Not Capturing Keys

1. Verify the service is running: `sudo systemctl status keymeter@$USER`
2. Check permissions on the output directory: `ls -la ~/keymeter_logs`
3. Check system logs: `sudo journalctl -xe`

## Development

### Project Structure

```
keyboardanalysis/
├── keymeter.py          # Main KeyMeter application
├── keymeter.service     # Systemd service file
├── install.sh           # Installation script
├── uninstall.sh         # Uninstallation script
├── requirements.txt     # Python dependencies
├── README.md            # This file
└── LICENSE              # License file
```

### Dependencies

- `pynput>=1.7.6`: Cross-platform keyboard event monitoring
- `python-daemon>=3.0.1`: Daemon process management

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## Acknowledgments

- Built with [pynput](https://github.com/moses-palmer/pynput) for keyboard event handling
- Uses [python-daemon](https://pagure.io/python-daemon/) for background process management
