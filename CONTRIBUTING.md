# Contributing to KeyMeter

Thank you for considering contributing to KeyMeter! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful, inclusive, and constructive in all interactions.

## How to Contribute

### Reporting Bugs

Before creating a bug report:
1. Check existing issues to avoid duplicates
2. Gather system information (OS version, Python version, etc.)
3. Collect relevant logs from `~/keymeter_logs/keymeter.log`

Include in your bug report:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- System information
- Relevant log excerpts
- Screenshots if applicable

### Suggesting Enhancements

Enhancement suggestions are welcome! Please:
1. Check if the feature already exists or is planned
2. Clearly describe the use case
3. Explain why this would be useful
4. Provide examples if possible

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Commit with clear messages
7. Push to your fork
8. Open a pull request

## Development Setup

### Prerequisites

- Ubuntu 18.04+ (or similar Linux distribution)
- Python 3.6+
- Git

### Setting Up Development Environment

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/keyboardanalysis.git
cd keyboardanalysis

# Install dependencies
pip3 install -r requirements.txt

# Install development dependencies
pip3 install pytest pylint black
```

### Running Tests

```bash
# Run all tests
python3 test_keymeter.py

# Run example
python3 example.py
```

### Code Style

We follow PEP 8 with some modifications:
- Maximum line length: 100 characters
- Use 4 spaces for indentation
- Use descriptive variable names

Format your code:
```bash
black keymeter.py --line-length 100
```

Lint your code:
```bash
pylint keymeter.py
```

## Project Structure

```
keyboardanalysis/
├── keymeter.py          # Main application
├── keymeter.service     # Systemd service file
├── install.sh           # Installation script
├── uninstall.sh         # Uninstallation script
├── requirements.txt     # Python dependencies
├── test_keymeter.py     # Test suite
├── example.py           # Usage examples
├── README.md            # Main documentation
├── QUICKSTART.md        # Quick start guide
├── USAGE.md             # Detailed usage guide
├── CONTRIBUTING.md      # This file
└── LICENSE              # License file
```

## Testing Guidelines

### Writing Tests

- Add tests for new features
- Ensure tests pass before submitting PR
- Mock external dependencies (like pynput)
- Test edge cases and error conditions

Example test:
```python
def test_new_feature():
    """Test description."""
    km = KeyMeter(output_dir="/tmp/test")
    # Test code here
    km.stop()
    assert expected == actual
```

### Manual Testing

For features that require X server:
1. Test on actual Ubuntu system
2. Verify service installation
3. Check systemd integration
4. Verify file permissions
5. Test error handling

## Documentation

Update relevant documentation when making changes:
- README.md for major features
- USAGE.md for new usage patterns
- QUICKSTART.md if installation changes
- Code comments for complex logic
- Docstrings for functions/classes

## Commit Messages

Follow conventional commit format:

```
type(scope): subject

body (optional)

footer (optional)
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

Examples:
```
feat(capture): add support for mouse events
fix(service): correct systemd service file permissions
docs(readme): update installation instructions
```

## Release Process

1. Update version number in code
2. Update CHANGELOG.md
3. Create release branch
4. Test thoroughly
5. Tag release
6. Create GitHub release
7. Update documentation

## Areas for Contribution

Current priorities:
- [ ] Mouse event capture
- [ ] Configurable output formats (JSON, CSV)
- [ ] Real-time analysis dashboard
- [ ] Encryption support
- [ ] Windows/macOS support
- [ ] Performance optimizations
- [ ] Additional tests

## Questions?

- Open an issue for questions
- Check existing documentation
- Review closed issues/PRs

Thank you for contributing to KeyMeter!
