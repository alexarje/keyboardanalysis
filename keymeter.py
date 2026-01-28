#!/usr/bin/env python3
"""
KeyMeter - Keyboard stroke capture tool for Ubuntu
Captures keyboard events and logs them to text files.
"""

import os
import sys
import signal
import argparse
import logging
from datetime import datetime
from pathlib import Path
from pynput import keyboard


class KeyMeter:
    """Keyboard event capture and logging."""
    
    def __init__(self, output_dir=None, log_file=None):
        """
        Initialize KeyMeter.
        
        Args:
            output_dir: Directory to store capture files (default: ~/keymeter_logs)
            log_file: Path to log file for application logs (default: ~/keymeter_logs/keymeter.log)
        """
        # Set default output directory
        if output_dir is None:
            output_dir = os.path.expanduser("~/keymeter_logs")
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up logging
        if log_file is None:
            log_file = self.output_dir / "keymeter.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('KeyMeter')
        
        # Create current capture file
        self.current_file = None
        self.capture_file = None
        self._create_new_capture_file()
        
        # Keyboard listener
        self.listener = None
        self.running = False
        
        self.logger.info(f"KeyMeter initialized. Output directory: {self.output_dir}")
    
    def _create_new_capture_file(self):
        """Create a new capture file with timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"keystrokes_{timestamp}.txt"
        self.current_file = self.output_dir / filename
        
        # Open file in append mode with restrictive permissions (0600)
        # Create file with secure permissions if it doesn't exist
        fd = os.open(
            self.current_file, 
            os.O_WRONLY | os.O_CREAT | os.O_APPEND,
            0o600
        )
        self.capture_file = os.fdopen(fd, 'a')
        self.capture_file.write(f"# KeyMeter capture started at {datetime.now().isoformat()}\n")
        self.capture_file.flush()
        
        self.logger.info(f"Created new capture file: {self.current_file}")
    
    def _on_press(self, key):
        """Handle key press events."""
        try:
            timestamp = datetime.now().isoformat()
            
            # Handle different key types
            if hasattr(key, 'char') and key.char is not None:
                # Regular character key
                key_str = key.char
            else:
                # Special key (e.g., shift, ctrl, enter)
                key_str = str(key).replace('Key.', '')
            
            # Write to file
            self.capture_file.write(f"{timestamp}\t{key_str}\n")
            self.capture_file.flush()
            
        except Exception as e:
            self.logger.error(f"Error capturing key press: {e}")
    
    def _on_release(self, key):
        """Handle key release events (optional, for future use)."""
        # Currently not logging releases to keep files smaller
        # Can be enabled if needed
        pass
    
    def start(self):
        """Start capturing keyboard events."""
        self.logger.info("Starting keyboard capture...")
        self.running = True
        
        # Create and start listener
        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )
        self.listener.start()
        
        self.logger.info("Keyboard capture started successfully")
        
        # Keep the program running
        try:
            self.listener.join()
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop capturing keyboard events."""
        self.logger.info("Stopping keyboard capture...")
        self.running = False
        
        if self.listener:
            self.listener.stop()
        
        if self.capture_file and not self.capture_file.closed:
            self.capture_file.write(f"# KeyMeter capture stopped at {datetime.now().isoformat()}\n")
            self.capture_file.close()
        
        self.logger.info("Keyboard capture stopped")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()


def main():
    """Main entry point for KeyMeter."""
    parser = argparse.ArgumentParser(
        description='KeyMeter - Keyboard stroke capture tool for Ubuntu'
    )
    parser.add_argument(
        '-o', '--output-dir',
        help='Directory to store capture files (default: ~/keymeter_logs)',
        default=None
    )
    parser.add_argument(
        '-l', '--log-file',
        help='Path to application log file',
        default=None
    )
    parser.add_argument(
        '-d', '--daemon',
        action='store_true',
        help='Run as daemon (background process)'
    )
    
    args = parser.parse_args()
    
    # Create KeyMeter instance
    keymeter = KeyMeter(output_dir=args.output_dir, log_file=args.log_file)
    
    # Set up signal handlers for graceful shutdown
    def signal_handler(signum, frame):
        keymeter.logger.info(f"Received signal {signum}, shutting down...")
        keymeter.stop()
        if not args.daemon:
            sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Run as daemon if requested
    if args.daemon:
        try:
            import daemon
            import daemon.pidfile
            
            pidfile_path = keymeter.output_dir / "keymeter.pid"
            
            with daemon.DaemonContext(
                pidfile=daemon.pidfile.PIDLockFile(str(pidfile_path)),
                signal_map={
                    signal.SIGTERM: signal_handler,
                    signal.SIGINT: signal_handler,
                }
            ):
                keymeter.start()
        except ImportError:
            keymeter.logger.error("python-daemon not installed. Install with: pip install python-daemon")
            sys.exit(1)
    else:
        # Run in foreground
        keymeter.start()


if __name__ == '__main__':
    main()
