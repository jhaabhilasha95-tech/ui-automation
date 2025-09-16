"""
WebDriver setup and teardown utilities.
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from config.config import Config


class DriverFactory:
    """Factory class for creating and managing WebDriver instances."""
    
    def __init__(self):
        self.config = Config()
        self.driver = None
    
    def setup_driver(self):
        """Set up Chrome WebDriver with mobile emulation."""
        chrome_options = Options()
        
        # Mobile emulation settings
        if self.config.MOBILE_EMULATION:
            chrome_options.add_experimental_option("mobileEmulation", self.config.MOBILE_EMULATION)
            print("✅ Mobile emulation enabled")
        else:
            # Only apply window-size if mobile emulation is not active
            chrome_options.add_argument("--window-size=1920,1080")
        
        # Additional Chrome options
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--ignore-ssl-errors")
        chrome_options.add_argument("--ignore-certificate-errors-spki-list")
        
        # Set up ChromeDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Set timeouts
        self.driver.implicitly_wait(self.config.IMPLICIT_WAIT)
        self.driver.set_page_load_timeout(self.config.PAGE_LOAD_TIMEOUT)
        
        print("✅ WebDriver setup completed")
        return self.driver
    
    def quit_driver(self):
        """Quit the WebDriver instance."""
        if self.driver:
            self.driver.quit()
            self.driver = None
            print("✅ WebDriver closed")
    
    def navigate_to_twitch(self):
        """Navigate to Twitch homepage."""
        if not self.driver:
            self.setup_driver()
        
        self.driver.get(self.config.TWITCH_URL)
        print(f"✅ Navigated to {self.config.TWITCH_URL}")
    
    def take_screenshot(self, filename):
        """Take a screenshot and save it."""
        import os
        
        # Create screenshots directory if it doesn't exist
        screenshots_dir = "screenshots"
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)
        
        # Take screenshot
        filepath = os.path.join(screenshots_dir, filename)
        self.driver.save_screenshot(filepath)
        print(f"Screenshot saved: {filepath}")
        return filepath
    
    def handle_modal_popup(self):
        """Handle any modal popups that appear."""
        try:
            # Common modal close selectors
            modal_selectors = [
                "button[aria-label='Close']",
                ".modal-close-button",
                "[data-a-target='player-overlay-click-handler']",
                "button[class*='close']",
                "button[class*='dismiss']"
            ]
            
            for selector in modal_selectors:
                try:
                    modal_element = self.driver.find_element("css selector", selector)
                    if modal_element.is_displayed():
                        modal_element.click()
                        print(f"✅ Closed modal popup with selector: {selector}")
                        return True
                except:
                    continue
            
            print("ℹ️ No modal popups found to close")
            return False
            
        except Exception as e:
            print(f"⚠️ Error handling modal popup: {e}")
            return False
    
    def scroll_page(self, times=1):
        """Scroll the page down a specified number of times."""
        for i in range(times):
            self.driver.execute_script("window.scrollBy(0, 500);")
            print(f"Scrolled down {i+1}/{times} times")
    
    def wait_for_page_load(self):
        """Wait for page to load completely."""
        import time
        time.sleep(2)  # Basic wait for page load
    
    def wait_for_video_load(self):
        """Wait for video content to load."""
        import time
        time.sleep(3)  # Wait for video content
