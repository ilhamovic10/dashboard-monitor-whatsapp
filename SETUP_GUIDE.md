# Quick Setup Guide

## First Time Setup (5 minutes)

### Step 1: Install Python
1. Download Python 3.8+ from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Verify installation:
   ```bash
   python --version
   ```

### Step 2: Install Chrome Extension
1. Open Chrome
2. Go to: https://chrome.google.com/webstore/detail/gofullpage-full-page-scre/fdpohaocaechififmbbbbbknoalclacl
3. Click "Add to Chrome"
4. Click "Add extension"

### Step 3: Configure Extension Shortcut
1. Open Chrome and type: `chrome://extensions/shortcuts`
2. Find "GoFullPage - Full Page Screen Capture"
3. Click the pencil icon next to "Capture Entire Page"
4. Press: `Alt + Shift + P`
5. Click "OK"

### Step 4: Setup WhatsApp Web
1. Open Chrome
2. Go to: https://web.whatsapp.com
3. Scan QR code with your phone
4. Check "Keep me signed in"
5. Verify you can see your chats

### Step 5: Install Script Dependencies
1. Download/clone this repository
2. Open Command Prompt in the folder
3. Run:
   ```bash
   pip install -r requirements.txt
   ```

### Step 6: Configure the Script
1. Open `config.json` in a text editor
2. Update these fields:
   ```json
   {
     "dashboard_url": "YOUR_DASHBOARD_URL_HERE",
     "whatsapp_group_name": "YOUR_GROUP_NAME_HERE"
   }
   ```
3. Save the file

### Step 7: Test Run
1. Open Command Prompt in the folder
2. Run:
   ```bash
   python dashboard_monitor.py
   ```
3. Press Enter when prompted
4. Watch it work! (Don't touch mouse/keyboard)

## Pre-Flight Checklist

Before running the script, verify:

- [ ] Python is installed and in PATH
- [ ] Chrome is installed
- [ ] GoFullPage extension is installed
- [ ] GoFullPage shortcut is set to `Alt+Shift+P`
- [ ] WhatsApp Web is logged in
- [ ] You know your WhatsApp group name (exact spelling)
- [ ] Dashboard URL is accessible
- [ ] `config.json` is properly configured
- [ ] Dependencies are installed (`pip install -r requirements.txt`)

## Quick Test

Test each component individually:

### Test 1: GoFullPage
1. Open any webpage in Chrome
2. Press `Alt+Shift+P`
3. Screenshot should be captured and downloaded

### Test 2: WhatsApp Web
1. Open https://web.whatsapp.com
2. Search for your group
3. Verify you can send messages

### Test 3: Python Script
```bash
python dashboard_monitor.py
```
Press Enter and let it run one cycle.

## Common First-Time Issues

### "Python not recognized"
**Solution**: Add Python to PATH:
1. Search "Environment Variables" in Windows
2. Edit "Path" variable
3. Add Python installation folder
4. Restart Command Prompt

### "No module named 'pyautogui'"
**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

### "GoFullPage not working"
**Solution**: 
1. Verify extension is enabled
2. Check shortcut is correctly set
3. Test manually with `Alt+Shift+P`

### "WhatsApp group not found"
**Solution**:
1. Check exact group name (case-sensitive)
2. Verify you're a member
3. Test manual search on WhatsApp Web

## Running in Background

### Option 1: Keep Terminal Open
Just run the script and minimize the window.

### Option 2: Task Scheduler (Windows)
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., Daily at 9 AM)
4. Action: Start a program
5. Program: `python.exe`
6. Arguments: `C:\path\to\dashboard_monitor.py`
7. Start in: `C:\path\to\script\folder`

### Option 3: Python Background Process
Create `run_background.py`:
```python
import subprocess
import os

# Run in background
subprocess.Popen(
    ['python', 'dashboard_monitor.py'],
    cwd=os.path.dirname(os.path.abspath(__file__)),
    creationflags=subprocess.CREATE_NO_WINDOW
)
```

## Need Help?

1. Check `dashboard_monitor.log` for errors
2. Read the [Troubleshooting section](README.md#-troubleshooting) in README
3. Open an issue on GitHub

## Success!

If everything works, you should see:
1. Chrome opens automatically
2. Dashboard loads
3. Screenshot is taken
4. WhatsApp Web opens
5. Screenshot is sent to group
6. Script waits 30 minutes
7. Process repeats

**You're all set! 🎉**
