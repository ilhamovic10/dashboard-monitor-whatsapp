"""
Test script for Dashboard Monitor
Run this to verify everything is working correctly
"""

import sys
import time
import os
from pathlib import Path

def test_imports():
    """Test if all required modules are installed"""
    print("Testing imports...")
    
    try:
        import pyautogui
        print("✓ PyAutoGUI imported successfully")
    except ImportError:
        print("✗ PyAutoGUI not found. Run: pip install pyautogui")
        return False
    
    try:
        from PIL import Image
        print("✓ Pillow imported successfully")
    except ImportError:
        print("✗ Pillow not found. Run: pip install Pillow")
        return False
    
    try:
        import json
        print("✓ JSON module available")
    except ImportError:
        print("✗ JSON module not found")
        return False
    
    return True

def test_config_file():
    """Test if config file exists and is valid"""
    print("\nTesting configuration file...")
    
    if not os.path.exists('config.json'):
        print("✗ config.json not found")
        return False
    
    try:
        import json
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        required_keys = ['dashboard_url', 'whatsapp_group_name', 'interval_minutes']
        for key in required_keys:
            if key not in config:
                print(f"✗ Missing required key: {key}")
                return False
        
        print("✓ Configuration file is valid")
        print(f"  Dashboard URL: {config['dashboard_url']}")
        print(f"  WhatsApp Group: {config['whatsapp_group_name']}")
        print(f"  Interval: {config['interval_minutes']} minutes")
        return True
        
    except Exception as e:
        print(f"✗ Error reading config: {e}")
        return False

def test_pyautogui():
    """Test PyAutoGUI basic functionality"""
    print("\nTesting PyAutoGUI...")
    
    try:
        import pyautogui
        
        # Test screen size detection
        size = pyautogui.size()
        print(f"✓ Screen size detected: {size.width}x{size.height}")
        
        # Test mouse position
        pos = pyautogui.position()
        print(f"✓ Mouse position: {pos.x}, {pos.y}")
        
        print("✓ PyAutoGUI working correctly")
        return True
        
    except Exception as e:
        print(f"✗ PyAutoGUI error: {e}")
        return False

def test_directories():
    """Test if required directories exist"""
    print("\nTesting directories...")
    
    # Create screenshots directory if not exists
    Path('screenshots').mkdir(exist_ok=True)
    print("✓ Screenshots directory ready")
    
    # Check Downloads folder
    downloads = Path.home() / "Downloads"
    if downloads.exists():
        print(f"✓ Downloads folder found: {downloads}")
    else:
        print("✗ Downloads folder not found")
        return False
    
    return True

def test_chrome_extension():
    """Provide instructions to test Chrome extension"""
    print("\nChrome Extension Test (Manual):")
    print("─" * 50)
    print("1. Open Google Chrome")
    print("2. Navigate to any webpage")
    print("3. Press Alt+Shift+P")
    print("4. Verify screenshot is captured and downloaded")
    print("─" * 50)
    
    response = input("Did the GoFullPage extension work? (y/n): ").lower()
    return response == 'y'

def test_whatsapp_web():
    """Provide instructions to test WhatsApp Web"""
    print("\nWhatsApp Web Test (Manual):")
    print("─" * 50)
    print("1. Open Chrome")
    print("2. Navigate to web.whatsapp.com")
    print("3. Verify you are logged in")
    print("4. Search for your target group")
    print("5. Verify you can access the group")
    print("─" * 50)
    
    response = input("Is WhatsApp Web working? (y/n): ").lower()
    return response == 'y'

def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("Dashboard Monitor - System Test")
    print("=" * 50)
    
    tests = [
        ("Python Imports", test_imports),
        ("Configuration File", test_config_file),
        ("PyAutoGUI", test_pyautogui),
        ("Directories", test_directories),
        ("Chrome Extension", test_chrome_extension),
        ("WhatsApp Web", test_whatsapp_web),
    ]
    
    results = []
    
    for name, test_func in tests:
        print()
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"✗ Test failed with error: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {name}")
    
    print("─" * 50)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✅ All tests passed! You're ready to run the script.")
        print("\nNext step: Run 'python dashboard_monitor.py'")
    else:
        print("\n⚠️ Some tests failed. Please fix the issues above.")
        print("\nCheck README.md for troubleshooting help.")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
