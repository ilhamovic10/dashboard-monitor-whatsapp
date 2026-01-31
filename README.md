# Dashboard Monitoring Automation

Automated dashboard screenshot monitoring system that captures full-page screenshots every 30 minutes and sends them to WhatsApp groups using Python automation.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-production-success.svg)

## 🎯 Features

- ✅ **Automated Screenshot Capture**: Uses GoFullPage Chrome extension for full-page screenshots
- ✅ **WhatsApp Integration**: Automatically sends screenshots to specified WhatsApp groups
- ✅ **Scheduled Monitoring**: Runs every 30 minutes for 4 hours (configurable)
- ✅ **Logging System**: Comprehensive logging for debugging and monitoring
- ✅ **Configurable**: Easy JSON-based configuration
- ✅ **Error Handling**: Robust error handling and failsafe mechanisms

## 📋 Prerequisites

### System Requirements
- Windows OS (tested on Windows 10/11)
- Python 3.8 or higher
- Google Chrome browser
- Active internet connection

### Required Chrome Extensions
1. **GoFullPage - Full Page Screen Capture**
   - Install from: [Chrome Web Store](https://chrome.google.com/webstore/detail/gofullpage-full-page-scre/fdpohaocaechififmbbbbbknoalclacl)
   - Set keyboard shortcut to `Alt+Shift+P`

### WhatsApp Setup
1. Open [WhatsApp Web](https://web.whatsapp.com)
2. Scan QR code to log in
3. Keep the session active (enable "Keep me signed in")

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/ilhamovic10/dashboard-monitor-whatsapp.git
cd dashboard-monitor-whatsapp
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On Linux/Mac:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### 1. Edit `config.json`

```json
{
  "dashboard_url": "http://your-dashboard-url.com",
  "screenshot_dir": "screenshots",
  "interval_minutes": 30,
  "whatsapp_group_name": "Your Group Name",
  "chrome_shortcut_key": "alt+shift+p",
  "delays": {
    "browser_load": 5,
    "screenshot_capture": 3,
    "whatsapp_load": 3,
    "message_send": 2
  }
}
```

### 2. Configure GoFullPage Extension

1. Open Chrome Extensions (`chrome://extensions/`)
2. Click on GoFullPage extension
3. Set keyboard shortcut:
   - Click "Keyboard shortcuts" at bottom
   - Set "Capture Entire Page" to `Alt+Shift+P`
   - Save changes

### 3. Test WhatsApp Web Access

1. Open Chrome
2. Navigate to `web.whatsapp.com`
3. Log in and verify you can access your groups
4. Find your target group name (must match `config.json`)

## 📖 Usage

### Quick Start

```bash
python dashboard_monitor.py
```

### What Happens:
1. Script starts and loads configuration
2. Opens Chrome browser
3. Navigates to dashboard URL
4. Captures full-page screenshot using GoFullPage
5. Opens WhatsApp Web
6. Searches for specified group
7. Sends screenshot with timestamp
8. Waits 30 minutes
9. Repeats for 4 hours total

### Command Line Options

```bash
# Run with default settings (4 hours, 30-minute intervals)
python dashboard_monitor.py

# Stop at any time
Press Ctrl+C
```

## 📁 Project Structure

```
dashboard-monitoring/
│
├── dashboard_monitor.py    # Main script
├── config.json             # Configuration file
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── LICENSE                # MIT License
├── .gitignore            # Git ignore file
│
├── screenshots/          # Screenshot storage (created automatically)
└── dashboard_monitor.log # Execution logs (created automatically)
```

## 🔧 Troubleshooting

### Common Issues

#### 1. PyAutoGUI Not Working
**Problem**: Mouse/keyboard automation not working

**Solution**:
```bash
# Reinstall PyAutoGUI
pip uninstall pyautogui
pip install pyautogui==0.9.54
```

#### 2. GoFullPage Not Capturing
**Problem**: Screenshots not being taken

**Solutions**:
- Verify GoFullPage extension is installed
- Check keyboard shortcut is set to `Alt+Shift+P`
- Ensure Chrome has focus when script runs
- Try manually pressing `Alt+Shift+P` to test

#### 3. WhatsApp Group Not Found
**Problem**: Cannot find WhatsApp group

**Solutions**:
- Verify exact group name in `config.json`
- Group name is case-sensitive
- Make sure you're a member of the group
- Try searching manually on WhatsApp Web first

#### 4. Screenshots Not Sending
**Problem**: Screenshots captured but not sent

**Solutions**:
- Check internet connection
- Verify WhatsApp Web is logged in
- Increase delays in `config.json`:
```json
"delays": {
  "browser_load": 8,
  "screenshot_capture": 5,
  "whatsapp_load": 5,
  "message_send": 3
}
```

#### 5. Script Stops Unexpectedly
**Problem**: Script crashes or stops

**Solutions**:
- Check `dashboard_monitor.log` for errors
- Ensure you don't move mouse during execution
- Verify all URLs are accessible
- Check Chrome is set as default browser

## 📊 Logs

Logs are automatically created in `dashboard_monitor.log`:

```
2025-01-31 10:00:00 - INFO - Dashboard Monitor initialized
2025-01-31 10:00:05 - INFO - Opening dashboard: http://localhost:3000
2025-01-31 10:00:10 - INFO - Screenshot captured successfully
2025-01-31 10:00:15 - INFO - Screenshot sent successfully
```

## 🔐 Security Best Practices

1. **Never commit sensitive data**:
   - Don't include actual dashboard URLs in public repos
   - Don't commit logs with sensitive information
   - Use environment variables for sensitive config

2. **WhatsApp Session**:
   - Log out from WhatsApp Web when not monitoring
   - Don't share screenshots publicly

3. **Access Control**:
   - Restrict access to the script
   - Use strong passwords for dashboard access

## 🎨 Customization

### Change Screenshot Interval

Edit `config.json`:
```json
{
  "interval_minutes": 15  // Change to 15 minutes
}
```

### Change Monitoring Duration

Edit `dashboard_monitor.py`:
```python
# Line in main():
monitor.run_continuous_monitoring(duration_hours=8)  # Change to 8 hours
```

### Add Multiple Groups

Modify the script to loop through groups:
```python
groups = ["Group 1", "Group 2", "Group 3"]
for group in groups:
    monitor.search_whatsapp_group(group)
    monitor.send_screenshot_to_whatsapp(screenshot_path)
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Changelog

### Version 1.0.0 (2025-01-31)
- Initial release
- Automated screenshot capture with GoFullPage
- WhatsApp integration
- Configurable monitoring intervals
- Comprehensive logging system

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Elham1x0**

## 🙏 Acknowledgments

- [PyAutoGUI](https://github.com/asweigart/pyautogui) for automation capabilities
- [GoFullPage](https://gofullpage.com/) for screenshot functionality
- WhatsApp Web for messaging API

## 📞 Support

If you encounter any issues:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review `dashboard_monitor.log` for errors
3. Open an issue on GitHub
4. Contact: [ilhami.hanafiah@gmail.com]

## ⚠️ Disclaimer

This tool is for automation purposes only. Ensure you have permission to:
- Access and screenshot the dashboard
- Send automated messages to WhatsApp groups
- Use automation on the systems involved

Use responsibly and in accordance with all applicable terms of service.

---

**Made with ❤️ by Elham1x0**

**⭐ Star this repo if you find it useful!**
