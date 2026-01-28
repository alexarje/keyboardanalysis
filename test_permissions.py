#!/usr/bin/env python3
"""
Test file permissions are set correctly.
"""

import sys
import os
import tempfile
from pathlib import Path
import stat

# Mock pynput
class MockKey:
    def __init__(self, char=None):
        self.char = char

class MockListener:
    def __init__(self, on_press=None, on_release=None):
        pass
    def start(self):
        return self
    def stop(self):
        pass
    def join(self):
        pass

class MockKeyboard:
    Listener = MockListener

mock_pynput = type('pynput', (), {'keyboard': MockKeyboard})()
sys.modules['pynput'] = mock_pynput
sys.modules['pynput.keyboard'] = MockKeyboard

from keymeter import KeyMeter

def test_file_permissions():
    """Test that capture files have restrictive permissions."""
    print("Testing file permissions...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "test_logs"
        
        keymeter = KeyMeter(output_dir=str(output_dir))
        
        # Get capture file
        capture_files = list(output_dir.glob("keystrokes_*.txt"))
        assert len(capture_files) == 1, "No capture file found"
        
        capture_file = capture_files[0]
        
        # Check file permissions
        file_stat = os.stat(capture_file)
        file_mode = stat.filemode(file_stat.st_mode)
        
        print(f"  File: {capture_file.name}")
        print(f"  Permissions: {file_mode}")
        print(f"  Octal mode: {oct(stat.S_IMODE(file_stat.st_mode))}")
        
        # Verify permissions are 0600 (owner read/write only)
        expected_mode = 0o600
        actual_mode = stat.S_IMODE(file_stat.st_mode)
        
        keymeter.stop()
        
        assert actual_mode == expected_mode, \
            f"Expected permissions {oct(expected_mode)}, got {oct(actual_mode)}"
        
        print("✓ File permissions test passed (0600)")

if __name__ == '__main__':
    try:
        test_file_permissions()
        print("\nAll permission tests passed!")
        sys.exit(0)
    except AssertionError as e:
        print(f"\nTest failed: {e}")
        sys.exit(1)
