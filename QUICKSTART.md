# KeyMeter Quick Start Guide

This guide will help you get KeyMeter up and running quickly on your Ubuntu system.

## Prerequisites

- Ubuntu 18.04 or later
- Python 3.6+
- sudo access

## Installation (5 minutes)

### 1. Clone the repository

```bash
git clone https://github.com/alexarje/keyboardanalysis.git
cd keyboardanalysis
```

### 2. Run installation script

```bash
chmod +x install.sh
./install.sh
```

This will:
- Install required Python packages (pynput, python-daemon)
- Copy KeyMeter to `/opt/keymeter/`
- Install systemd service
- Create output directory at `~/keymeter_logs`

### 3. Grant permissions

Add your user to the input group (required for keyboard capture):

```bash
sudo usermod -a -G input $USER
```

**Important:** Log out and log back in for this to take effect!

### 4. Enable and start the service

```bash
sudo systemctl enable keymeter@$USER
sudo systemctl start keymeter@$USER
```

### 5. Verify it's running

```bash
sudo systemctl status keymeter@$USER
```

You should see `active (running)` in green.

## Quick Test

Type something on your keyboard, then check the logs:

```bash
ls -lh ~/keymeter_logs/
cat ~/keymeter_logs/keystrokes_*.txt
```

You should see your keystrokes with timestamps!

## Common Commands

### Check service status
```bash
sudo systemctl status keymeter@$USER
```

### Stop KeyMeter
```bash
sudo systemctl stop keymeter@$USER
```

### Start KeyMeter
```bash
sudo systemctl start keymeter@$USER
```

### Restart KeyMeter
```bash
sudo systemctl restart keymeter@$USER
```

### View live logs
```bash
tail -f ~/keymeter_logs/keymeter.log
```

### View captured keystrokes
```bash
tail -f ~/keymeter_logs/keystrokes_*.txt
```

## Manual Usage (Without Service)

If you want to run KeyMeter manually without the systemd service:

```bash
# Run in foreground (Ctrl+C to stop)
python3 keymeter.py

# Run with custom output directory
python3 keymeter.py --output-dir /path/to/logs

# Run as daemon (background)
python3 keymeter.py --daemon
```

## Troubleshooting

### "Permission denied" errors

Make sure you added your user to the input group and logged out/in:
```bash
groups | grep input
```

If you don't see "input" in the output, run:
```bash
sudo usermod -a -G input $USER
```
Then log out and log back in.

### Service won't start

Check the logs:
```bash
sudo journalctl -u keymeter@$USER -n 50
```

### No keystrokes being captured

1. Check if service is running: `sudo systemctl status keymeter@$USER`
2. Check application logs: `cat ~/keymeter_logs/keymeter.log`
3. Verify permissions: `ls -ld ~/keymeter_logs`

## Uninstallation

To completely remove KeyMeter:

```bash
chmod +x uninstall.sh
./uninstall.sh
```

This removes the service and application, but keeps your log files.
To remove logs too:
```bash
rm -rf ~/keymeter_logs
```

## Security & Privacy

⚠️ **Important**: KeyMeter captures ALL keyboard input. 

- Keep log files secure
- Only use on systems you own/control
- Comply with all applicable laws and policies
- Consider encrypting the output directory
- Regularly clean old log files

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Review the [example.py](example.py) for programmatic usage
- Customize output location in the systemd service file
- Set up log rotation for long-term use

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review logs in `~/keymeter_logs/keymeter.log`
3. Check system logs: `sudo journalctl -u keymeter@$USER`
4. Open an issue on GitHub with logs and error messages

## Quick Reference

| Task | Command |
|------|---------|
| Start service | `sudo systemctl start keymeter@$USER` |
| Stop service | `sudo systemctl stop keymeter@$USER` |
| Status | `sudo systemctl status keymeter@$USER` |
| Enable auto-start | `sudo systemctl enable keymeter@$USER` |
| Disable auto-start | `sudo systemctl disable keymeter@$USER` |
| View logs | `cat ~/keymeter_logs/keymeter.log` |
| View captures | `cat ~/keymeter_logs/keystrokes_*.txt` |
| Live monitoring | `tail -f ~/keymeter_logs/keystrokes_*.txt` |

Happy keystroke analyzing! 🎹
