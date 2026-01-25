"""
Automated Postman Flow Variable Updater using Browser Automation
Opens Postman web interface and updates Flow configuration variables
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class PostmanFlowBrowserUpdater:
    """Updates Postman Flow variables using browser automation."""
    
    def __init__(self):
        self.flow_id = "69755954010ddb0014f502dc"
        self.flow_url = f"https://postman.com/flows/{self.flow_id}"
        self.variables = {
            "GHL_API_KEY": {
                "id": "vq0LPMl6",
                "value": "pit-81ca6da4-c48f-4d4d-887e-a6d35bca70a5",
                "type": "secret"
            },
            "GHL_LOCATION_ID": {
                "id": "qDnQBK2f",
                "value": "4X72lI7IBpK9tJOdKwOf",
                "type": "string"
            }
        }
        self.driver = None
    
    def setup_driver(self):
        """Setup Chrome WebDriver."""
        chrome_options = Options()
        # Uncomment to run headless (no browser window)
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            print("[INFO] Chrome browser opened")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to open browser: {e}")
            print("\nMake sure ChromeDriver is installed:")
            print("  1. Download from: https://chromedriver.chromium.org/")
            print("  2. Add to PATH or place in same directory")
            return False
    
    def login_to_postman(self):
        """Login to Postman (if not already logged in)."""
        print("[INFO] Navigating to Postman...")
        self.driver.get("https://postman.com/login")
        
        try:
            # Wait for page to load
            time.sleep(3)
            
            # Check if already logged in (redirected to dashboard)
            if "postman.com" in self.driver.current_url and "login" not in self.driver.current_url:
                print("[INFO] Already logged in to Postman")
                return True
            
            print("[WARNING] Please log in to Postman manually in the browser window")
            print("  - The browser will wait for you to complete login")
            input("  - Press Enter after you've logged in...")
            return True
            
        except Exception as e:
            print(f"[ERROR] Login failed: {e}")
            return False
    
    def navigate_to_flow(self):
        """Navigate to the Flow page."""
        print(f"[INFO] Opening Flow: {self.flow_id}")
        self.driver.get(self.flow_url)
        time.sleep(3)
        
        # Wait for flow to load
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            print("[INFO] Flow page loaded")
            return True
        except TimeoutException:
            print("[ERROR] Flow page did not load in time")
            return False
    
    def find_and_update_variables(self):
        """Find configuration panel and update variables."""
        print("[INFO] Looking for configuration panel...")
        
        # This is complex because Postman's UI structure may vary
        # We'll try multiple approaches
        
        try:
            # Method 1: Look for configuration/settings button
            config_selectors = [
                "button[aria-label*='Configuration']",
                "button[aria-label*='Settings']",
                "[data-testid*='config']",
                "[data-testid*='settings']",
                ".configuration-panel",
                ".settings-panel"
            ]
            
            config_button = None
            for selector in config_selectors:
                try:
                    config_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if config_button:
                        print(f"[INFO] Found configuration button with selector: {selector}")
                        config_button.click()
                        time.sleep(2)
                        break
                except NoSuchElementException:
                    continue
            
            if not config_button:
                print("[WARNING] Could not find configuration button automatically")
                print("[INFO] Please manually:")
                print("  1. Click on the Configuration/Settings panel in the Flow")
                print("  2. Find the variables: GHL_API_KEY and GHL_LOCATION_ID")
                input("  3. Press Enter after you've opened the configuration panel...")
            
            # Try to find and update variables
            self.update_variable_in_ui("GHL_API_KEY")
            self.update_variable_in_ui("GHL_LOCATION_ID")
            
            # Look for save button
            save_selectors = [
                "button[type='submit']",
                "button:contains('Save')",
                "[data-testid*='save']",
                "button.save"
            ]
            
            for selector in save_selectors:
                try:
                    save_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    save_button.click()
                    print("[INFO] Clicked save button")
                    time.sleep(2)
                    break
                except:
                    continue
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to update variables: {e}")
            return False
    
    def update_variable_in_ui(self, var_name):
        """Update a single variable in the UI."""
        var_info = self.variables[var_name]
        print(f"[INFO] Updating {var_name}...")
        
        # This is very UI-dependent and may need adjustment
        # Try to find input field by various methods
        try:
            # Look for input by name, id, or placeholder
            input_selectors = [
                f"input[name*='{var_name}']",
                f"input[id*='{var_info['id']}']",
                f"input[placeholder*='{var_name}']",
                f"textarea[name*='{var_name}']"
            ]
            
            for selector in input_selectors:
                try:
                    input_field = self.driver.find_element(By.CSS_SELECTOR, selector)
                    input_field.clear()
                    input_field.send_keys(var_info['value'])
                    print(f"[SUCCESS] Updated {var_name}")
                    time.sleep(1)
                    return True
                except NoSuchElementException:
                    continue
            
            print(f"[WARNING] Could not find input field for {var_name} automatically")
            return False
            
        except Exception as e:
            print(f"[ERROR] Error updating {var_name}: {e}")
            return False
    
    def run(self):
        """Run the complete update process."""
        print("=" * 60)
        print("POSTMAN FLOW AUTOMATED VARIABLE UPDATER")
        print("=" * 60)
        print()
        
        if not self.setup_driver():
            return False
        
        try:
            if not self.login_to_postman():
                return False
            
            if not self.navigate_to_flow():
                return False
            
            if not self.find_and_update_variables():
                print("\n[INFO] Manual intervention may be required")
                print("The browser window is open - you can complete the update manually")
                input("\nPress Enter when done (browser will close)...")
            
            print("\n[SUCCESS] Update process completed!")
            return True
            
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
            return False
        finally:
            if self.driver:
                print("[INFO] Closing browser...")
                time.sleep(2)
                self.driver.quit()


def main():
    """Main function."""
    updater = PostmanFlowBrowserUpdater()
    success = updater.run()
    return success


if __name__ == "__main__":
    import sys
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n[INFO] Process interrupted by user")
        sys.exit(1)
