"""
Twitch home page object model.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class TwitchHomePage(BasePage):
    """Page object for Twitch home page."""
    
    # Locators
    SEARCH_ICON = (By.CSS_SELECTOR, "[data-a-target='top-nav-search-button']")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[data-a-target='tw-input']")
    SEARCH_RESULTS = (By.CSS_SELECTOR, "[data-a-target='search-results']")
    STREAMER_CARDS = (By.CSS_SELECTOR, "[data-a-target='search-result-card']")
    STREAMER_LINK = (By.CSS_SELECTOR, "a[data-a-target='search-result-card']")
    
    # Alternative locators for different page layouts
    SEARCH_ICON_ALT = (By.CSS_SELECTOR, "button[aria-label='Search']")
    SEARCH_INPUT_ALT = (By.CSS_SELECTOR, "input[placeholder*='Search']")
    
    def __init__(self, driver_manager):
        super().__init__(driver_manager)
    
    def click_search_icon(self):
        """Click the search icon."""
        try:
            self.click_element(self.SEARCH_ICON)
        except:
            # Try alternative locator
            self.click_element(self.SEARCH_ICON_ALT)
    
    def search_for_term(self, search_term):
        """Search for a specific term."""
        try:
            self.send_keys_to_element(self.SEARCH_INPUT, search_term)
        except:
            # Try alternative locator
            self.send_keys_to_element(self.SEARCH_INPUT_ALT, search_term)
    
    def get_search_results(self):
        """Get search results elements."""
        return self.find_elements(self.STREAMER_CARDS)
    
    def select_first_streamer(self):
        """Select the first available streamer from search results."""
        streamer_cards = self.get_search_results()
        if streamer_cards:
            # Click on the first streamer card
            streamer_cards[0].click()
            return True
        return False
    
    def is_search_visible(self):
        """Check if search input is visible."""
        return (self.is_element_visible(self.SEARCH_INPUT) or 
                self.is_element_visible(self.SEARCH_INPUT_ALT))
    
    def wait_for_search_results(self):
        """Wait for search results to load."""
        self.wait_for_visible(self.SEARCH_RESULTS)
