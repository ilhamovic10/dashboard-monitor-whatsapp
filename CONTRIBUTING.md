# Contributing to Dashboard Monitoring Automation

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and encourage diverse perspectives
- Focus on what is best for the community
- Show empathy towards other community members

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:

1. **Clear title**: Brief description of the issue
2. **Environment details**:
   - OS version
   - Python version
   - Chrome version
   - Extension versions
3. **Steps to reproduce**: Detailed steps to recreate the bug
4. **Expected behavior**: What should happen
5. **Actual behavior**: What actually happens
6. **Logs**: Relevant log files or error messages
7. **Screenshots**: If applicable

### Suggesting Features

For feature requests, please include:

1. **Use case**: Why this feature is needed
2. **Proposed solution**: How it should work
3. **Alternatives**: Other approaches you've considered
4. **Additional context**: Any other relevant information

### Pull Requests

#### Before Submitting

1. **Check existing issues/PRs**: Avoid duplicates
2. **Create an issue**: Discuss major changes first
3. **Fork the repository**: Create your own fork
4. **Create a branch**: Use descriptive branch names
   ```bash
   git checkout -b feature/amazing-feature
   ```

#### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/dashboard-monitoring.git
cd dashboard-monitoring

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest flake8 black
```

#### Coding Standards

**Python Style:**
- Follow PEP 8
- Use 4 spaces for indentation
- Maximum line length: 88 characters (Black default)
- Use meaningful variable names
- Add docstrings to functions and classes

**Code Formatting:**
```bash
# Format code with Black
black dashboard_monitor.py

# Check with flake8
flake8 dashboard_monitor.py --max-line-length=88
```

**Example:**
```python
def capture_screenshot(self, delay: int = 3) -> bool:
    """
    Capture full page screenshot using GoFullPage extension.
    
    Args:
        delay: Seconds to wait for capture (default: 3)
        
    Returns:
        bool: True if successful, False otherwise
        
    Raises:
        Exception: If screenshot capture fails
    """
    logging.info("Capturing screenshot with GoFullPage")
    
    try:
        pyautogui.hotkey('alt', 'shift', 'p')
        time.sleep(delay)
        return True
    except Exception as e:
        logging.error(f"Screenshot failed: {e}")
        return False
```

#### Testing

**Write Tests:**
```python
# tests/test_monitor.py
import unittest
from dashboard_monitor import DashboardMonitor

class TestDashboardMonitor(unittest.TestCase):
    def setUp(self):
        self.monitor = DashboardMonitor()
    
    def test_config_loading(self):
        self.assertIsNotNone(self.monitor.config)
        self.assertIn('dashboard_url', self.monitor.config)
    
    def test_screenshot_directory_creation(self):
        self.assertTrue(self.monitor.screenshot_dir.exists())
```

**Run Tests:**
```bash
pytest tests/
```

#### Documentation

- Update README.md if adding features
- Add docstrings to new functions
- Update ADVANCED_USAGE.md for advanced features
- Include code examples where helpful

#### Commit Messages

Follow conventional commits:

```
feat: add email notification feature
fix: resolve WhatsApp group search issue
docs: update installation instructions
style: format code with black
refactor: simplify screenshot capture logic
test: add unit tests for config loading
chore: update dependencies
```

**Good commit message example:**
```
feat: add multiple dashboard support

- Add multi_dashboard_config.json support
- Implement loop for multiple dashboards
- Update documentation with examples
- Add tests for multi-dashboard feature

Closes #42
```

#### Pull Request Process

1. **Update documentation**: README, docstrings, etc.
2. **Add tests**: For new features
3. **Update changelog**: Add entry to CHANGELOG.md
4. **Run tests**: Ensure all tests pass
5. **Format code**: Run Black and flake8
6. **Push to your fork**:
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Create PR**: Use the PR template
8. **Wait for review**: Be patient and responsive

#### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Manual testing completed
- [ ] All tests pass

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
- [ ] Commit messages follow convention

## Screenshots (if applicable)
Add screenshots here

## Related Issues
Closes #XX
```

### Project Structure

```
dashboard-monitoring/
├── dashboard_monitor.py      # Main script
├── config.json              # Configuration
├── requirements.txt         # Dependencies
├── test_setup.py           # Setup test script
├── README.md               # Main documentation
├── SETUP_GUIDE.md         # Setup instructions
├── ADVANCED_USAGE.md      # Advanced features
├── CONTRIBUTING.md        # This file
├── LICENSE                # MIT License
├── .gitignore            # Git ignore rules
├── .github/
│   └── workflows/
│       └── test.yml      # CI/CD pipeline
└── tests/
    ├── __init__.py
    ├── test_monitor.py
    └── test_config.py
```

### Areas for Contribution

We welcome contributions in these areas:

1. **Bug Fixes**: Fix reported issues
2. **Features**: 
   - Multiple dashboard support
   - Email notifications
   - Slack integration
   - Database logging
   - Web dashboard
3. **Documentation**:
   - Improve README
   - Add video tutorials
   - Translate documentation
4. **Testing**:
   - Add unit tests
   - Integration tests
   - End-to-end tests
5. **Performance**:
   - Optimize screenshot capture
   - Reduce memory usage
   - Faster WhatsApp sending

### Getting Help

- **Questions**: Open a discussion on GitHub
- **Bugs**: Open an issue with details
- **Chat**: Join our community (if available)

### Review Process

1. **Automated checks**: CI/CD must pass
2. **Code review**: Maintainer reviews code
3. **Testing**: Manual testing if needed
4. **Approval**: At least one maintainer approval
5. **Merge**: Maintainer merges PR

### Release Process

1. Update version in `dashboard_monitor.py`
2. Update CHANGELOG.md
3. Create git tag: `git tag v1.1.0`
4. Push tag: `git push --tags`
5. Create GitHub release

### Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Acknowledged in README

### License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing! 🎉**
