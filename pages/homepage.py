"""
Twitch homepage actions and interactions.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class Homepage(BasePage):
    """Page object for Twitch homepage."""
    
    # Locators - Updated for current Twitch UI (Browse button)
    SEARCH_ICON = (By.XPATH, "//div[@class='Layout-sc-1xcs6mc-0 iwaIid']//div[@class='ScSvgWrapper-sc-wkgzod-0 dKXial tw-svg']//svg[@width='20' and @height='20']")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder*='Search'], input[placeholder*='search'], input[data-a-target='tw-input']")
    TWITCH_LOGO = (By.CSS_SELECTOR, "a[aria-label='Go to the Twitch home page']")
    
    # Alternative locators for different page layouts
    SEARCH_ICON_ALT = (By.XPATH, "//div[contains(@class, 'CoreText-sc-1txzju1-0') and text()='Browse']")
    SEARCH_INPUT_ALT = (By.CSS_SELECTOR, "input[type='search'], input[name*='search']")
    
    def __init__(self, driver_manager):
        super().__init__(driver_manager)
    
    def click_search_icon(self):
        """Click the search icon."""
        # Try multiple approaches to find and click search
        search_selectors = [
            self.SEARCH_ICON_ALT,  # Browse button with XPath (most reliable)
            self.SEARCH_ICON,  # SVG search icon
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
