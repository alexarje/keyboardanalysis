#!/usr/bin/env python3
"""
Example script showing how to use KeyMeter programmatically.
This demonstrates the API without requiring X server.
"""

import tempfile
from pathlib import Path

# Mock pynput for demonstration
import sys

class MockKey:
    def __init__(self, char=None, name=None):
        self.char = char
        self.name = name
    
    def __str__(self):
        return f"Key.{self.name}" if self.name else str(self.char)

class MockListener:
    def __init__(self, on_press=None, on_release=None):
        self.on_press = on_press
        self.on_release = on_release
    
    def start(self):
        return self
    
    def stop(self):
        pass
    
    def join(self):
        pass

class MockKeyboard:
    Key = type('Key', (), {
        'enter': MockKey(name='enter'),
        'space': MockKey(name='space'),
    })
    Listener = MockListener

mock_pynput = type('pynput', (), {'keyboard': MockKeyboard})()
sys.modules['pynput'] = mock_pynput
sys.modules['pynput.keyboard'] = MockKeyboard

# Now import KeyMeter
from keymeter import KeyMeter


def example_basic_usage():
    """Example 1: Basic usage with default settings."""
    print("Example 1: Basic Usage")
    print("-" * 40)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "example_logs"
        
        # Create KeyMeter instance
        keymeter = KeyMeter(output_dir=str(output_dir))
        
        # Simulate some key presses
        print("Simulating key presses: 'hello'")
        for char in "hello":
            keymeter._on_press(MockKey(char=char))
        
        # Clean up
        keymeter.stop()
        
        # Show results
        capture_files = list(output_dir.glob("keystrokes_*.txt"))
        print(f"\nCreated file: {capture_files[0].name}")
        print(f"File location: {output_dir}")
        print("\nFile contents:")
        print(capture_files[0].read_text())
    
    print()


def example_custom_directory():
    """Example 2: Using custom output directory."""
    print("Example 2: Custom Output Directory")
    print("-" * 40)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        custom_dir = Path(tmpdir) / "my_custom_logs"
        
        # Create KeyMeter with custom directory
        keymeter = KeyMeter(output_dir=str(custom_dir))
        
        # Simulate typing
        print("Simulating key presses: 'test'")
        for char in "test":
            keymeter._on_press(MockKey(char=char))
        
        keymeter._on_press(MockKey(name='enter'))
        
        keymeter.stop()
        
        # Show results
        capture_files = list(custom_dir.glob("keystrokes_*.txt"))
        print(f"\nCustom directory: {custom_dir}")
        print(f"Files created: {len(capture_files)}")
        
        # Show last few lines
        content = capture_files[0].read_text()
        lines = [l for l in content.split('\n') if l and not l.startswith('#')]
        print(f"\nCaptured {len(lines)} keystrokes")
        print("\nLast 5 entries:")
        for line in lines[-5:]:
            print(f"  {line}")
    
    print()


def example_context_manager():
    """Example 3: Using context manager."""
    print("Example 3: Context Manager Usage")
    print("-" * 40)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "context_logs"
        
        print("Using KeyMeter as context manager...")
        # Context manager automatically handles cleanup
        with KeyMeter(output_dir=str(output_dir)) as km:
            print("Simulating key presses: 'context'")
            for char in "context":
                km._on_press(MockKey(char=char))
        
        print("Context exited - KeyMeter automatically stopped")
        
        # Verify files were created and closed properly
        capture_files = list(output_dir.glob("keystrokes_*.txt"))
        print(f"\nFile created and closed: {capture_files[0].name}")
    
    print()


def main():
    """Run all examples."""
    print("=" * 60)
    print("KeyMeter Usage Examples")
    print("=" * 60)
    print()
    
    example_basic_usage()
    example_custom_directory()
    example_context_manager()
    
    print("=" * 60)
    print("Examples completed!")
    print("=" * 60)
    print()
    print("To use KeyMeter on a real system:")
    print("  1. Install: ./install.sh")
    print("  2. Enable service: sudo systemctl enable keymeter@$USER")
    print("  3. Start service: sudo systemctl start keymeter@$USER")
    print("  4. Check logs: cat ~/keymeter_logs/keystrokes_*.txt")


if __name__ == '__main__':
    main()
