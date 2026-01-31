"""
Dashboard Monitoring Automation Script
Automatically captures screenshots using GoFullPage and sends to WhatsApp
Author: Mujahid Latiff
Version: 1.0.0
"""

import pyautogui
import time
import os
import logging
from datetime import datetime
from pathlib import Path
import json
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dashboard_monitor.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

class DashboardMonitor:
    """Main class for dashboard monitoring and WhatsApp automation"""
    
    def __init__(self, config_file='config.json'):
        """Initialize the monitor with configuration"""
        self.config = self.load_config(config_file)
        self.screenshot_dir = Path(self.config.get('screenshot_dir', 'screenshots'))
        self.screenshot_dir.mkdir(exist_ok=True)
        
        # Safety settings for PyAutoGUI
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 1.0
        
        logging.info("Dashboard Monitor initialized")
    
    def load_config(self, config_file):
        """Load configuration from JSON file"""
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    return json.load(f)
            else:
                logging.warning(f"Config file {config_file} not found, using defaults")
                return self.get_default_config()
        except Exception as e:
            logging.error(f"Error loading config: {e}")
            return self.get_default_config()
    
    def get_default_config(self):
        """Return default configuration"""
        return {
            "dashboard_url": "http://localhost:3000/dashboard",
            "screenshot_dir": "screenshots",
            "interval_minutes": 30,
            "whatsapp_group_name": "Dashboard Monitoring",
            "chrome_shortcut_key": "ctrl+shift+s",  # GoFullPage shortcut
            "delays": {
                "browser_load": 5,
                "screenshot_capture": 3,
                "whatsapp_load": 3,
                "message_send": 2
            }
        }
    
    def switch_to_chrome(self):
        """Switch to Chrome browser using Alt+Tab"""
        logging.info("Switching to Chrome browser")
        pyautogui.hotkey('alt', 'tab')
        time.sleep(1)
    
    def open_dashboard(self):
        """Open dashboard URL in Chrome"""
        logging.info(f"Opening dashboard: {self.config['dashboard_url']}")
        
        # Focus Chrome address bar
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(0.5)
        
        # Type URL and press Enter
        pyautogui.write(self.config['dashboard_url'], interval=0.05)
        pyautogui.press('enter')
        
        # Wait for page to load
        time.sleep(self.config['delays']['browser_load'])
        logging.info("Dashboard loaded")
    
    def capture_screenshot_with_gofullpage(self):
        """Capture full page screenshot using GoFullPage extension"""
        logging.info("Capturing screenshot with GoFullPage")
        
        try:
            # Trigger GoFullPage extension (default: Alt+Shift+P)
            # You can customize this based on your GoFullPage shortcut
            pyautogui.hotkey('alt', 'shift', 'p')
            
            # Wait for GoFullPage to process
            time.sleep(self.config['delays']['screenshot_capture'])
            
            # GoFullPage automatically downloads the screenshot
            # Wait for download to complete
            time.sleep(2)
            
            logging.info("Screenshot captured successfully")
            return True
            
        except Exception as e:
            logging.error(f"Error capturing screenshot: {e}")
            return False
    
    def get_latest_screenshot(self):
        """Get the most recent screenshot from downloads folder"""
        downloads_folder = Path.home() / "Downloads"
        
        # Look for GoFullPage screenshots (they usually have timestamp)
        screenshots = list(downloads_folder.glob("*.png")) + list(downloads_folder.glob("*.jpg"))
        
        if not screenshots:
            logging.error("No screenshots found in Downloads folder")
            return None
        
        # Get the most recent file
        latest_screenshot = max(screenshots, key=os.path.getctime)
        logging.info(f"Found latest screenshot: {latest_screenshot}")
        
        return latest_screenshot
    
    def open_whatsapp_web(self):
        """Open WhatsApp Web in new tab"""
        logging.info("Opening WhatsApp Web")
        
        # Open new tab
        pyautogui.hotkey('ctrl', 't')
        time.sleep(1)
        
        # Navigate to WhatsApp Web
        pyautogui.write('web.whatsapp.com', interval=0.05)
        pyautogui.press('enter')
        
        # Wait for WhatsApp to load
        time.sleep(self.config['delays']['whatsapp_load'])
        logging.info("WhatsApp Web loaded")
    
    def search_whatsapp_group(self, group_name):
        """Search for WhatsApp group"""
        logging.info(f"Searching for group: {group_name}")
        
        # Click on search box (using Ctrl+F for WhatsApp search)
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(0.5)
        
        # Type group name
        pyautogui.write(group_name, interval=0.1)
        time.sleep(1)
        
        # Press Enter to select first result
        pyautogui.press('enter')
        time.sleep(1)
        
        logging.info(f"Group '{group_name}' selected")
    
    def send_screenshot_to_whatsapp(self, screenshot_path):
        """Send screenshot to WhatsApp group"""
        logging.info(f"Sending screenshot: {screenshot_path}")
        
        try:
            # Click on attachment button (paperclip icon)
            # Alternative: Use keyboard shortcut
            pyautogui.hotkey('ctrl', 'shift', 'a')
            time.sleep(1)
            
            # Type file path
            pyautogui.write(str(screenshot_path), interval=0.05)
            time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(2)
            
            # Add caption with timestamp
            caption = f"Dashboard Screenshot - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            pyautogui.write(caption, interval=0.05)
            time.sleep(0.5)
            
            # Send the image (Enter key)
            pyautogui.press('enter')
            time.sleep(self.config['delays']['message_send'])
            
            logging.info("Screenshot sent successfully")
            return True
            
        except Exception as e:
            logging.error(f"Error sending screenshot: {e}")
            return False
    
    def run_monitoring_cycle(self):
        """Run one complete monitoring cycle"""
        logging.info("=" * 50)
        logging.info("Starting monitoring cycle")
        logging.info("=" * 50)
        
        try:
            # Step 1: Switch to Chrome and open dashboard
            self.switch_to_chrome()
            self.open_dashboard()
            
            # Step 2: Capture screenshot with GoFullPage
            if not self.capture_screenshot_with_gofullpage():
                logging.error("Failed to capture screenshot")
                return False
            
            # Step 3: Get the latest screenshot
            screenshot_path = self.get_latest_screenshot()
            if not screenshot_path:
                logging.error("Could not find screenshot file")
                return False
            
            # Step 4: Open WhatsApp Web
            self.open_whatsapp_web()
            
            # Step 5: Search for group
            self.search_whatsapp_group(self.config['whatsapp_group_name'])
            
            # Step 6: Send screenshot
            if not self.send_screenshot_to_whatsapp(screenshot_path):
                logging.error("Failed to send screenshot")
                return False
            
            logging.info("Monitoring cycle completed successfully")
            return True
            
        except Exception as e:
            logging.error(f"Error in monitoring cycle: {e}")
            return False
    
    def run_continuous_monitoring(self, duration_hours=4):
        """Run continuous monitoring for specified duration"""
        logging.info(f"Starting continuous monitoring for {duration_hours} hours")
        logging.info(f"Interval: {self.config['interval_minutes']} minutes")
        
        interval_seconds = self.config['interval_minutes'] * 60
        end_time = time.time() + (duration_hours * 3600)
        cycle_count = 0
        
        while time.time() < end_time:
            cycle_count += 1
            logging.info(f"\n{'='*50}")
            logging.info(f"CYCLE {cycle_count}")
            logging.info(f"{'='*50}\n")
            
            # Run monitoring cycle
            self.run_monitoring_cycle()
            
            # Calculate time until next cycle
            remaining_time = end_time - time.time()
            if remaining_time > interval_seconds:
                logging.info(f"Waiting {self.config['interval_minutes']} minutes until next cycle...")
                time.sleep(interval_seconds)
            else:
                logging.info("Monitoring duration completed")
                break
        
        logging.info(f"\nMonitoring completed. Total cycles: {cycle_count}")


def main():
    """Main entry point"""
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║   Dashboard Monitoring Automation Script             ║
    ║   Version 1.0.0                                       ║
    ║   Author: Mujahid Latiff                             ║
    ╚═══════════════════════════════════════════════════════╝
    """)
    
    # Create monitor instance
    monitor = DashboardMonitor()
    
    # Display configuration
    print("\nConfiguration:")
    print(f"  Dashboard URL: {monitor.config['dashboard_url']}")
    print(f"  Interval: {monitor.config['interval_minutes']} minutes")
    print(f"  WhatsApp Group: {monitor.config['whatsapp_group_name']}")
    print(f"  Screenshot Directory: {monitor.screenshot_dir}")
    
    print("\n⚠️  Important:")
    print("  1. Make sure Chrome is open with GoFullPage extension installed")
    print("  2. Make sure WhatsApp Web is already logged in")
    print("  3. Do not move the mouse during automation")
    print("  4. Press Ctrl+C to stop at any time (failsafe)")
    
    input("\nPress Enter to start monitoring...")
    
    try:
        # Run for 4 hours as specified
        monitor.run_continuous_monitoring(duration_hours=4)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Monitoring stopped by user")
        logging.info("Monitoring stopped by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        logging.error(f"Fatal error: {e}")
    finally:
        print("\n✅ Script terminated")


if __name__ == "__main__":
    main()
