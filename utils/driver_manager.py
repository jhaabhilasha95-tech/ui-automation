"""
WebDriver management utilities for the Twitch UI automation framework.
"""
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from config.config import Config


class DriverManager:
    """Manages WebDriver instance and provides utility methods."""
    
    def __init__(self):
        self.driver = None
        self.wait = None
        self.config = Config()
    
    def setup_driver(self):
        """Set up Chrome WebDriver with mobile emulation."""
        chrome_options = Options()
        
        # Mobile emulation settings
        mobile_emulation = self.config.MOBILE_EMULATION
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        
        # Additional Chrome options
        if self.config.HEADLESS:
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        
        # Set window size
        chrome_options.add_argument(f"--window-size={self.config.WINDOW_SIZE}")
        
        # Initialize driver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Set timeouts
        self.driver.implicitly_wait(self.config.IMPLICIT_WAIT)
        self.driver.set_page_load_timeout(self.config.PAGE_LOAD_TIMEOUT)
        
        # Initialize WebDriverWait
        self.wait = WebDriverWait(self.driver, self.config.EXPLICIT_WAIT)
        
        return self.driver
    
    def navigate_to_twitch(self):
        """Navigate to Twitch homepage."""
        self.driver.get(self.config.TWITCH_URL)
        self.wait_for_page_load()
    
    def wait_for_page_load(self):
        """Wait for page to fully load."""
        try:
            self.wait.until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
        except TimeoutException:
            print("Page load timeout - continuing anyway")
    
    def wait_for_element(self, locator, timeout=None):
        """Wait for element to be present and visible."""
        if timeout is None:
            timeout = self.config.EXPLICIT_WAIT
        
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))
    
    def wait_for_clickable(self, locator, timeout=None):
        """Wait for element to be clickable."""
        if timeout is None:
            timeout = self.config.EXPLICIT_WAIT
        
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))
    
    def wait_for_visible(self, locator, timeout=None):
        """Wait for element to be visible."""
        if timeout is None:
            timeout = self.config.EXPLICIT_WAIT
        
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))
    
    def handle_modal_popup(self):
        """Handle modal popups that may appear on streamer pages."""
        try:
            # Common modal selectors
            modal_selectors = [
                "button[data-a-target='player-overlay-click-handler']",
                "button[aria-label='Close']",
                ".modal-close-button",
                "[data-testid='modal-close']",
                "button[class*='close']"
            ]
            
            for selector in modal_selectors:
                try:
                    modal = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if modal.is_displayed():
                        modal.click()
                        time.sleep(1)
                        print(f"Closed modal with selector: {selector}")
                        break
                except NoSuchElementException:
                    continue
                    
        except Exception as e:
            print(f"No modal found or error handling modal: {e}")
    
    def scroll_page(self, count=1):
        """Scroll the page down by specified count."""
        for i in range(count):
            self.driver.execute_script("window.scrollBy(0, window.innerHeight);")
            time.sleep(1)
            print(f"Scrolled down {i+1} time(s)")
    
    def take_screenshot(self, filename):
        """Take a screenshot and save it."""
        if not os.path.exists(self.config.SCREENSHOT_DIR):
            os.makedirs(self.config.SCREENSHOT_DIR)
        
        filepath = os.path.join(self.config.SCREENSHOT_DIR, filename)
        self.driver.save_screenshot(filepath)
        print(f"Screenshot saved: {filepath}")
        return filepath
    
    def wait_for_video_load(self):
        """Wait for video to load on streamer page."""
        try:
            # Wait for video element to be present
            video_selectors = [
                "video",
                "[data-a-target='player-overlay-click-handler']",
                ".video-player",
                "[class*='video']"
            ]
            
            for selector in video_selectors:
                try:
                    self.wait_for_element((By.CSS_SELECTOR, selector), self.config.VIDEO_LOAD_TIMEOUT)
                    print(f"Video element found with selector: {selector}")
                    break
                except TimeoutException:
                    continue
            
            # Additional wait for video to be ready
            time.sleep(3)
            
        except Exception as e:
            print(f"Error waiting for video load: {e}")
    
    def quit_driver(self):
        """Quit the WebDriver instance."""
        if self.driver:
            self.driver.quit()
            print("WebDriver closed")
