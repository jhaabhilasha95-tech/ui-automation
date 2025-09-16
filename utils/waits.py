"""
Explicit wait helpers for WebDriver interactions.
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class WaitHelpers:
    """Helper class for explicit waits."""
    
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    
    def wait_for_element_visible(self, locator, timeout=None):
        """Wait for an element to be visible."""
        wait_timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_timeout)
        return wait.until(EC.visibility_of_element_located(locator))
    
    def wait_for_element_present(self, locator, timeout=None):
        """Wait for an element to be present in DOM."""
        wait_timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_timeout)
        return wait.until(EC.presence_of_element_located(locator))
    
    def wait_for_element_clickable(self, locator, timeout=None):
        """Wait for an element to be clickable."""
        wait_timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_timeout)
        return wait.until(EC.element_to_be_clickable(locator))
    
    def wait_for_text_to_be_present_in_element(self, locator, text, timeout=None):
        """Wait for text to be present in an element."""
        wait_timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_timeout)
        return wait.until(EC.text_to_be_present_in_element(locator, text))
    
    def wait_for_url_contains(self, url_fragment, timeout=None):
        """Wait for URL to contain a specific fragment."""
        wait_timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_timeout)
        return wait.until(EC.url_contains(url_fragment))
    
    def wait_for_title_contains(self, title_fragment, timeout=None):
        """Wait for page title to contain a specific fragment."""
        wait_timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_timeout)
        return wait.until(EC.title_contains(title_fragment))
    
    def is_element_visible(self, locator, timeout=5):
        """Check if an element is visible within a short timeout."""
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.visibility_of_element_located(locator))
            return element.is_displayed()
        except TimeoutException:
            return False
    
    def is_element_present(self, locator, timeout=5):
        """Check if an element is present in DOM within a short timeout."""
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def wait_for_page_load(self, timeout=30):
        """Wait for page to load completely."""
        wait = WebDriverWait(self.driver, timeout)
        wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
    
    def wait_for_ajax_complete(self, timeout=30):
        """Wait for AJAX requests to complete."""
        wait = WebDriverWait(self.driver, timeout)
        wait.until(lambda driver: driver.execute_script("return jQuery.active == 0"))
    
    def wait_for_scroll_position(self, expected_position, timeout=10):
        """Wait for page to scroll to a specific position."""
        wait = WebDriverWait(self.driver, timeout)
        wait.until(lambda driver: abs(driver.execute_script("return window.pageYOffset;") - expected_position) < 10)

