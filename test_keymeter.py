#!/usr/bin/env python3
"""
Test script for KeyMeter - validates the module structure without X server
"""

import sys
import os
import tempfile
from pathlib import Path
from datetime import datetime

# Mock pynput keyboard module for testing
class MockKey:
    """Mock keyboard key."""
    def __init__(self, char=None, name=None):
        self.char = char
        self.name = name
    
    def __str__(self):
        return f"Key.{self.name}" if self.name else str(self.char)

class MockListener:
    """Mock keyboard listener."""
    def __init__(self, on_press=None, on_release=None):
        self.on_press = on_press
        self.on_release = on_release
        self.running = False
    
    def start(self):
        self.running = True
        return self
    
    def stop(self):
        self.running = False
    
    def join(self):
        pass

# Mock the pynput module
class MockKeyboard:
    Key = type('Key', (), {
        'enter': MockKey(name='enter'),
        'space': MockKey(name='space'),
        'backspace': MockKey(name='backspace'),
    })
    Listener = MockListener

# Create mock module object
mock_pynput = type('pynput', (), {'keyboard': MockKeyboard})()
sys.modules['pynput'] = mock_pynput
sys.modules['pynput.keyboard'] = MockKeyboard

# Now we can import keymeter
from keymeter import KeyMeter

def test_keymeter_initialization():
    """Test KeyMeter initialization."""
    print("Testing KeyMeter initialization...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "test_logs"
        log_file = output_dir / "test.log"
        
        keymeter = KeyMeter(output_dir=str(output_dir), log_file=str(log_file))
        
        # Verify output directory was created
        assert output_dir.exists(), "Output directory not created"
        
        # Verify log file exists
        assert log_file.exists(), "Log file not created"
        
        # Verify capture file was created
        capture_files = list(output_dir.glob("keystrokes_*.txt"))
        assert len(capture_files) == 1, f"Expected 1 capture file, found {len(capture_files)}"
        
        keymeter.stop()
        
    print("✓ Initialization test passed")

def test_keymeter_key_capture():
    """Test key capture simulation."""
    print("Testing key capture...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "test_logs"
        
        keymeter = KeyMeter(output_dir=str(output_dir))
        
        # Simulate some key presses
        test_keys = [
            MockKey(char='h'),
            MockKey(char='e'),
            MockKey(char='l'),
            MockKey(char='l'),
            MockKey(char='o'),
            MockKey(name='space'),
        ]
        
        for key in test_keys:
            keymeter._on_press(key)
        
        # Verify capture file has content
        capture_files = list(output_dir.glob("keystrokes_*.txt"))
        assert len(capture_files) == 1, "No capture file found"
        
        capture_file = capture_files[0]
        content = capture_file.read_text()
        
        # Check that we have the header and key entries
        lines = content.strip().split('\n')
        assert len(lines) >= 7, f"Expected at least 7 lines (header + 6 keys), got {len(lines)}"
        assert lines[0].startswith('#'), "First line should be a comment"
        
        # Check that keys were recorded
        assert 'h' in content, "Character 'h' not found in capture"
        assert 'space' in content, "Special key 'space' not found in capture"
        
        keymeter.stop()
        
    print("✓ Key capture test passed")

def test_keymeter_file_format():
    """Test output file format."""
    print("Testing output file format...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "test_logs"
        
        keymeter = KeyMeter(output_dir=str(output_dir))
        
        # Simulate key press
        keymeter._on_press(MockKey(char='a'))
        
        keymeter.stop()
        
        # Read and verify format
        capture_files = list(output_dir.glob("keystrokes_*.txt"))
        content = capture_files[0].read_text()
        lines = [l for l in content.split('\n') if l and not l.startswith('#')]
        
        # Check format: timestamp\tkey
        if lines:
            parts = lines[0].split('\t')
            assert len(parts) == 2, f"Expected 2 parts (timestamp, key), got {len(parts)}"
            
            # Verify timestamp format (ISO 8601)
            timestamp = parts[0]
            try:
                datetime.fromisoformat(timestamp)
            except ValueError:
                raise AssertionError(f"Invalid timestamp format: {timestamp}")
            
            # Verify key
            assert parts[1] == 'a', f"Expected key 'a', got '{parts[1]}'"
        
    print("✓ File format test passed")

def test_context_manager():
    """Test KeyMeter as context manager."""
    print("Testing context manager...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "test_logs"
        
        with KeyMeter(output_dir=str(output_dir)) as keymeter:
            keymeter._on_press(MockKey(char='x'))
            assert keymeter.capture_file is not None, "Capture file not opened"
        
        # After context exit, file should be closed
        # (we can't easily test this without accessing private attributes)
        
    print("✓ Context manager test passed")

def main():
    """Run all tests."""
    print("=" * 60)
    print("KeyMeter Test Suite")
    print("=" * 60)
    print()
    
    try:
        test_keymeter_initialization()
        test_keymeter_key_capture()
        test_keymeter_file_format()
        test_context_manager()
        
        print()
        print("=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print()
        print("=" * 60)
        print(f"Test failed: {e}")
        print("=" * 60)
        return 1
    except Exception as e:
        print()
        print("=" * 60)
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        print("=" * 60)
        return 1

if __name__ == '__main__':
    sys.exit(main())
