"""
Base page class for the Twitch UI automation framework.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.driver_factory import DriverFactory
from utils.waits import WaitHelpers
from utils.screenshot import ScreenshotHelper


class BasePage:
    """Base page class with common functionality."""
    
    def __init__(self, driver_manager):
        self.driver_manager = driver_manager
        self.driver = driver_manager.driver
        self.wait_helpers = WaitHelpers(self.driver)
        self.screenshot_helper = ScreenshotHelper(self.driver)
    
    def find_element(self, locator):
        """Find a single element."""
        return self.driver.find_element(*locator)
    
    def find_elements(self, locator):
        """Find multiple elements."""
        return self.driver.find_elements(*locator)
    
    def click_element(self, locator):
        """Click an element."""
        element = self.wait_for_clickable(locator)
        element.click()
    
    def send_keys_to_element(self, locator, text):
        """Send keys to an element."""
        element = self.wait_for_visible(locator)
        element.clear()
        element.send_keys(text)
    
    def get_element_text(self, locator):
        """Get text from an element."""
        element = self.wait_for_visible(locator)
        return element.text
    
    def is_element_present(self, locator):
        """Check if element is present."""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def is_element_visible(self, locator):
        """Check if element is visible."""
        try:
            element = self.driver.find_element(*locator)
            return element.is_displayed()
        except NoSuchElementException:
            return False
    
    def wait_for_clickable(self, locator, timeout=None):
        """Wait for element to be clickable."""
        return self.wait_helpers.wait_for_element_clickable(locator, timeout)
    
    def wait_for_visible(self, locator, timeout=None):
        """Wait for element to be visible."""
        return self.wait_helpers.wait_for_element_visible(locator, timeout)
    
    def wait_for_element(self, locator, timeout=None):
        """Wait for element to be present."""
        return self.wait_helpers.wait_for_element_present(locator, timeout)
    
    def scroll_to_element(self, locator):
        """Scroll to an element."""
        element = self.wait_for_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
    
    def take_screenshot(self, filename):
        """Take a screenshot."""
        return self.screenshot_helper.take_screenshot(filename)
