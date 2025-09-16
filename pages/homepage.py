"""
Twitch homepage actions and interactions.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class Homepage(BasePage):
    """Page object for Twitch homepage."""
    
    # Locators - Updated for current Twitch UI (Search icon by XPath)
    SEARCH_ICON = (By.XPATH, "//*[@id='root']/div[2]/a[2]")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder*='Search'], input[placeholder*='search'], input[data-a-target='tw-input']")
    TWITCH_LOGO = (By.CSS_SELECTOR, "a[aria-label='Go to the Twitch home page']")
    
    # Alternative locators for different page layouts
    SEARCH_ICON_ALT = (By.XPATH, "//*[@id='root']/div[2]/a[2]")
    SEARCH_ICON_SPECIFIC = (By.XPATH, "//*[@id='root']/div[2]/a[2]")
    SEARCH_INPUT_ALT = (By.CSS_SELECTOR, "input[type='search'], input[name*='search']")
    
    def __init__(self, driver_manager):
        super().__init__(driver_manager)
    
    def click_search_icon(self):
        """Click the search icon (single click only)."""
        # Use only the most reliable selector to avoid double-clicking
        try:
            # Try the most reliable Browse button selector first
            if self.is_element_present(self.SEARCH_ICON_ALT):
                self.click_element(self.SEARCH_ICON_ALT)
                print(f"Successfully clicked search icon with selector: {self.SEARCH_ICON_ALT[1]}")
                return True
        except Exception as e:
            print(f"Failed to click with primary selector: {e}")
        
        # If primary selector fails, try one fallback only
        try:
            if self.is_element_present(self.SEARCH_ICON_SPECIFIC):
                self.click_element(self.SEARCH_ICON_SPECIFIC)
                print(f"Successfully clicked search icon with selector: {self.SEARCH_ICON_SPECIFIC[1]}")
                return True
        except Exception as e:
            print(f"Failed to click with fallback selector: {e}")
            
        raise Exception("Could not find or click search icon")
    
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
    
    def is_search_visible(self):
        """Check if search input is visible."""
        return (self.is_element_visible(self.SEARCH_INPUT) or 
                self.is_element_visible(self.SEARCH_INPUT_ALT))
    
    def is_twitch_logo_visible(self):
        """Check if Twitch logo is visible."""
        try:
            return self.is_element_visible(self.TWITCH_LOGO)
        except:
            return False
    
    def get_twitch_logo_aria_label(self):
        """Get the aria-label of the Twitch logo."""
        try:
            logo = self.find_element(self.TWITCH_LOGO)
            return logo.get_attribute("aria-label")
        except:
            return None
