# Advanced Usage Guide

## Custom Configurations

### Multiple Dashboards

Create `multi_dashboard_config.json`:
```json
{
  "dashboards": [
    {
      "name": "Sales Dashboard",
      "url": "http://company.com/sales",
      "group": "Sales Team"
    },
    {
      "name": "Analytics Dashboard",
      "url": "http://company.com/analytics",
      "group": "Analytics Team"
    }
  ],
  "interval_minutes": 30
}
```

Create `multi_dashboard_monitor.py`:
```python
import json
from dashboard_monitor import DashboardMonitor

with open('multi_dashboard_config.json') as f:
    config = json.load(f)

for dashboard in config['dashboards']:
    monitor = DashboardMonitor()
    monitor.config['dashboard_url'] = dashboard['url']
    monitor.config['whatsapp_group_name'] = dashboard['group']
    monitor.run_monitoring_cycle()
```

### Schedule-Based Monitoring

Only run during business hours (9 AM - 5 PM):

```python
from datetime import datetime
import time

def is_business_hours():
    now = datetime.now()
    return 9 <= now.hour < 17 and now.weekday() < 5  # Mon-Fri

monitor = DashboardMonitor()

while True:
    if is_business_hours():
        monitor.run_monitoring_cycle()
        time.sleep(30 * 60)  # 30 minutes
    else:
        print("Outside business hours, sleeping...")
        time.sleep(60 * 60)  # 1 hour
```

### Email Notifications

Add email alerts when monitoring fails:

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_alert(error_message):
    sender = "your_email@gmail.com"
    receiver = "admin@company.com"
    password = "your_app_password"
    
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = "Dashboard Monitoring Alert"
    
    body = f"Monitoring failed with error:\n\n{error_message}"
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
        print("Alert email sent")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Use in monitoring cycle:
try:
    monitor.run_monitoring_cycle()
except Exception as e:
    send_email_alert(str(e))
```

### Database Logging

Store monitoring history in SQLite:

```python
import sqlite3
from datetime import datetime

def init_database():
    conn = sqlite3.connect('monitoring_history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS screenshots
                 (id INTEGER PRIMARY KEY,
                  timestamp TEXT,
                  dashboard_url TEXT,
                  screenshot_path TEXT,
                  whatsapp_group TEXT,
                  status TEXT)''')
    conn.commit()
    conn.close()

def log_screenshot(url, path, group, status):
    conn = sqlite3.connect('monitoring_history.db')
    c = conn.cursor()
    c.execute('''INSERT INTO screenshots 
                 (timestamp, dashboard_url, screenshot_path, whatsapp_group, status)
                 VALUES (?, ?, ?, ?, ?)''',
              (datetime.now().isoformat(), url, path, group, status))
    conn.commit()
    conn.close()

# Initialize on startup
init_database()

# Log each screenshot
if monitor.run_monitoring_cycle():
    log_screenshot(url, screenshot_path, group, "success")
else:
    log_screenshot(url, screenshot_path, group, "failed")
```

## Performance Optimization

### Reduce CPU Usage

```python
# Add these to config.json
{
  "optimization": {
    "screenshot_quality": 85,  # 1-100
    "resize_screenshot": true,
    "max_width": 1920,
    "max_height": 1080
  }
}
```

Implement in script:
```python
from PIL import Image

def optimize_screenshot(path):
    img = Image.open(path)
    
    # Resize if too large
    max_width = monitor.config['optimization']['max_width']
    max_height = monitor.config['optimization']['max_height']
    
    if img.width > max_width or img.height > max_height:
        img.thumbnail((max_width, max_height), Image.LANCZOS)
    
    # Compress
    quality = monitor.config['optimization']['screenshot_quality']
    img.save(path, optimize=True, quality=quality)
```

### Faster Screenshot Detection

```python
import time
from pathlib import Path

def wait_for_new_screenshot(downloads_folder, timeout=10):
    """Wait for new screenshot file to appear"""
    start_time = time.time()
    initial_files = set(downloads_folder.glob('*.png'))
    
    while time.time() - start_time < timeout:
        current_files = set(downloads_folder.glob('*.png'))
        new_files = current_files - initial_files
        
        if new_files:
            return max(new_files, key=os.path.getctime)
        
        time.sleep(0.5)
    
    return None
```

## Error Recovery

### Auto-Restart on Failure

```python
import sys
import subprocess

def restart_script():
    """Restart the current script"""
    python = sys.executable
    subprocess.Popen([python] + sys.argv)
    sys.exit()

# Use in main loop
max_failures = 3
failure_count = 0

while failure_count < max_failures:
    try:
        monitor.run_monitoring_cycle()
        failure_count = 0  # Reset on success
    except Exception as e:
        failure_count += 1
        logging.error(f"Failure {failure_count}/{max_failures}: {e}")
        
        if failure_count >= max_failures:
            logging.critical("Max failures reached, restarting...")
            restart_script()
        else:
            time.sleep(60)  # Wait before retry
```

### Screenshot Backup

```python
import shutil
from datetime import datetime

def backup_screenshot(screenshot_path):
    """Backup screenshot to dated folder"""
    backup_dir = Path('backups') / datetime.now().strftime('%Y-%m-%d')
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    backup_path = backup_dir / screenshot_path.name
    shutil.copy2(screenshot_path, backup_path)
    
    logging.info(f"Screenshot backed up to {backup_path}")
    return backup_path
```

## Advanced WhatsApp Features

### Send to Multiple Groups

```python
def send_to_multiple_groups(screenshot_path, groups):
    """Send screenshot to multiple WhatsApp groups"""
    for group in groups:
        logging.info(f"Sending to {group}")
        monitor.search_whatsapp_group(group)
        monitor.send_screenshot_to_whatsapp(screenshot_path)
        time.sleep(5)  # Delay between groups

# Usage
groups = ["Sales Team", "Management", "Analytics"]
send_to_multiple_groups(screenshot_path, groups)
```

### Custom Caption with Metrics

```python
def create_dashboard_caption(metrics):
    """Create detailed caption with dashboard metrics"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    caption = f"""
📊 Dashboard Update - {timestamp}

📈 Metrics:
• Active Users: {metrics.get('active_users', 'N/A')}
• Revenue: ${metrics.get('revenue', 'N/A')}
• Conversion Rate: {metrics.get('conversion', 'N/A')}%

🔔 Alerts: {metrics.get('alerts', 'None')}
    """
    
    return caption.strip()

# Use when sending
pyautogui.write(create_dashboard_caption(current_metrics))
```

## Monitoring Dashboard Metrics

Extract metrics from dashboard before screenshot:

```python
from selenium import webdriver
from selenium.webdriver.common.by import By

def extract_dashboard_metrics(url):
    """Extract key metrics from dashboard"""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(url)
        time.sleep(3)
        
        metrics = {
            'active_users': driver.find_element(By.ID, 'active-users').text,
            'revenue': driver.find_element(By.ID, 'revenue').text,
            'conversion': driver.find_element(By.ID, 'conversion-rate').text
        }
        
        return metrics
    finally:
        driver.quit()

# Use before screenshot
metrics = extract_dashboard_metrics(monitor.config['dashboard_url'])
```

## Deployment Options

### Windows Service

Create `service.py`:
```python
import win32serviceutil
import win32service
import win32event
import servicemanager
from dashboard_monitor import DashboardMonitor

class DashboardMonitorService(win32serviceutil.ServiceFramework):
    _svc_name_ = "DashboardMonitor"
    _svc_display_name_ = "Dashboard Monitoring Service"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        
    def SvcDoRun(self):
        monitor = DashboardMonitor()
        monitor.run_continuous_monitoring(duration_hours=24)

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(DashboardMonitorService)
```

Install:
```bash
python service.py install
python service.py start
```

### Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3-tk \
    python3-dev \
    scrot

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "dashboard_monitor.py"]
```

Build and run:
```bash
docker build -t dashboard-monitor .
docker run -d --name monitor dashboard-monitor
```

### Cloud Deployment (AWS EC2)

```bash
# SSH into EC2 instance
ssh -i key.pem ubuntu@your-ec2-ip

# Install dependencies
sudo apt update
sudo apt install python3-pip xvfb

# Clone repository
git clone https://github.com/yourusername/dashboard-monitoring.git
cd dashboard-monitoring

# Install requirements
pip3 install -r requirements.txt

# Run with virtual display (for headless)
xvfb-run python3 dashboard_monitor.py
```

## Monitoring & Alerts

### Health Check Endpoint

```python
from flask import Flask, jsonify
import threading

app = Flask(__name__)
last_success = None
failure_count = 0

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy' if failure_count < 3 else 'unhealthy',
        'last_success': last_success.isoformat() if last_success else None,
        'failure_count': failure_count
    })

# Run Flask in background thread
threading.Thread(target=lambda: app.run(port=5000), daemon=True).start()
```

### Prometheus Metrics

```python
from prometheus_client import Counter, Gauge, start_http_server

screenshots_total = Counter('screenshots_total', 'Total screenshots taken')
screenshots_failed = Counter('screenshots_failed', 'Failed screenshots')
last_screenshot_time = Gauge('last_screenshot_timestamp', 'Last screenshot timestamp')

# Start metrics server
start_http_server(8000)

# Increment in code
screenshots_total.inc()
last_screenshot_time.set_to_current_time()
```

## Best Practices

1. **Always test locally first**
2. **Use version control (git)**
3. **Keep logs for debugging**
4. **Monitor resource usage**
5. **Set up alerts for failures**
6. **Regular backups of screenshots**
7. **Document configuration changes**
8. **Use environment variables for secrets**

## Security Considerations

```python
# Use environment variables for sensitive data
import os

config = {
    'dashboard_url': os.getenv('DASHBOARD_URL'),
    'whatsapp_group': os.getenv('WHATSAPP_GROUP'),
}

# Encrypt screenshots at rest
from cryptography.fernet import Fernet

def encrypt_screenshot(path):
    key = Fernet.generate_key()
    cipher = Fernet(key)
    
    with open(path, 'rb') as f:
        encrypted = cipher.encrypt(f.read())
    
    with open(path + '.encrypted', 'wb') as f:
        f.write(encrypted)
```

## Performance Benchmarks

Typical performance on standard hardware:
- Screenshot capture: 2-3 seconds
- WhatsApp send: 3-5 seconds
- Total cycle time: 10-15 seconds
- Memory usage: ~100MB
- CPU usage: <5% when idle

## Troubleshooting Advanced Issues

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed debugging guides.
