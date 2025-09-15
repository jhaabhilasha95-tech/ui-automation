"""
Twitch home page object model.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class TwitchHomePage(BasePage):
    """Page object for Twitch home page."""
    
    # Locators - Updated for current Twitch UI (Browse button)
    SEARCH_ICON = (By.XPATH, "//div[contains(@class, 'CoreText-sc-1txzju1-0') and text()='Browse']")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder*='Search'], input[placeholder*='search'], input[data-a-target='tw-input']")
    SEARCH_RESULTS = (By.CSS_SELECTOR, "[data-a-target='search-results'], .search-results, [class*='search-results']")
    STREAMER_CARDS = (By.CSS_SELECTOR, "[data-a-target='search-result-card'], .search-result-card, [class*='search-result']")
    STREAMER_LINK = (By.CSS_SELECTOR, "a[data-a-target='search-result-card'], a[class*='search-result']")
    
    # Alternative locators for different page layouts
    SEARCH_ICON_ALT = (By.CSS_SELECTOR, "div.CoreText-sc-1txzju1-0.irZUBM")
    SEARCH_INPUT_ALT = (By.CSS_SELECTOR, "input[type='search'], input[name*='search']")
    
    def __init__(self, driver_manager):
        super().__init__(driver_manager)
    
    def click_search_icon(self):
        """Click the search icon."""
        # Try multiple approaches to find and click search
        search_selectors = [
            self.SEARCH_ICON,  # Browse button with XPath
            self.SEARCH_ICON_ALT,  # Browse button with CSS
            (By.XPATH, "//div[text()='Browse']"),  # Simple Browse text
            (By.CSS_SELECTOR, "div.CoreText-sc-1txzju1-0"),  # Browse text class
            (By.CSS_SELECTOR, "button[aria-label*='Search']"),
            (By.CSS_SELECTOR, "button[title*='Search']"),
            (By.CSS_SELECTOR, "[data-testid*='search']"),
        ]
        
        for selector in search_selectors:
            try:
                if self.is_element_present(selector):
                    self.click_element(selector)
                    print(f"Successfully clicked search icon with selector: {selector[1]}")
                    return True
            except Exception as e:
                print(f"Failed to click with selector {selector[1]}: {e}")
                continue
        
        # If no search icon found, try to find search input directly
        try:
            if self.is_element_present(self.SEARCH_INPUT):
                self.click_element(self.SEARCH_INPUT)
                print("Clicked search input directly")
                return True
        except:
            pass
            
        raise Exception("Could not find or click search icon or input")
    
    def search_for_term(self, search_term):
        """Search for a specific term."""
        # Try multiple approaches to find search input
        input_selectors = [
            self.SEARCH_INPUT,
            self.SEARCH_INPUT_ALT,
            (By.CSS_SELECTOR, "input[type='search']"),
            (By.CSS_SELECTOR, "input[placeholder*='Search']"),
            (By.CSS_SELECTOR, "input[data-a-target='tw-input']"),
            (By.CSS_SELECTOR, "input[name*='search']"),
        ]
        
        for selector in input_selectors:
            try:
                if self.is_element_present(selector):
                    self.send_keys_to_element(selector, search_term)
                    print(f"Successfully entered search term with selector: {selector[1]}")
                    return True
            except Exception as e:
                print(f"Failed to enter search term with selector {selector[1]}: {e}")
                continue
                
        raise Exception("Could not find search input field")
    
    def get_search_results(self):
        """Get search results elements."""
        # Look for StarCraft II specifically first
        starcraft_results = self.find_elements((By.XPATH, "//p[text()='StarCraft II']"))
        if starcraft_results:
            return starcraft_results
        
        # Fallback to general search results
        return self.find_elements(self.STREAMER_CARDS)
    
    def select_first_streamer(self):
        """Select the first available streamer from search results."""
        try:
            # Re-find elements to avoid stale element reference
            streamer_cards = self.get_search_results()
            if streamer_cards:
                # Click on the first streamer card
                streamer_cards[0].click()
                print(f"Selected search result: {streamer_cards[0].text}")
                return True
        except Exception as e:
            print(f"Error selecting streamer: {e}")
            # Try to find and click StarCraft II directly
            try:
                starcraft_element = self.driver.find_element(By.XPATH, "//p[text()='StarCraft II']")
                starcraft_element.click()
                print("Selected StarCraft II directly")
                return True
            except:
                pass
        return False
    
    def is_search_visible(self):
        """Check if search input is visible."""
        return (self.is_element_visible(self.SEARCH_INPUT) or 
                self.is_element_visible(self.SEARCH_INPUT_ALT))
    
    def wait_for_search_results(self):
        """Wait for search results to load."""
        self.wait_for_visible(self.SEARCH_RESULTS)
