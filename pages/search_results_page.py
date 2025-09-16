"""
Searching and scrolling logic for Twitch search results.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class SearchResultsPage(BasePage):
    """Page object for Twitch search results page."""
    
    # Locators
    SEARCH_RESULTS = (By.CSS_SELECTOR, "[data-a-target='search-results'], .search-results, [class*='search-results']")
    STREAMER_CARDS = (By.CSS_SELECTOR, "[data-a-target='search-result-card'], .search-result-card, [class*='search-result']")
    STREAMER_LINK = (By.CSS_SELECTOR, "a[data-a-target='search-result-card'], a[class*='search-result']")
    
    # Generic locators for streamer elements
    STREAMER_THUMBNAIL = (By.XPATH, "//img[@alt='' and @class='tw-image']")
    STREAMER_LINK = (By.XPATH, "//a[contains(@href, '/videos/')]")
    STREAMER_NAME = (By.XPATH, "//p[contains(@class, 'CoreText')]")
    
    # StarCraft II specific locators
    STARCRAFT_II_RESULT = (By.XPATH, "//p[@title='StarCraft II' and @class='CoreText-sc-1txzju1-0 gQCPzm']")
    STARCRAFT_II_TITLE = (By.XPATH, "//h1[contains(@class, 'CoreText-sc-1txzju1-0') and contains(@class, 'kuIRux')]")
    FOLLOW_BUTTON = (By.CSS_SELECTOR, "[data-a-target='game-directory-follow-button']")
    
    def __init__(self, driver_manager):
        super().__init__(driver_manager)
    
    def get_search_results(self):
        """Get search results elements."""
        # Look for StarCraft II specifically first
        starcraft_results = self.find_elements(self.STARCRAFT_II_RESULT)
        if starcraft_results:
            return starcraft_results
        
        # Fallback to general search results
        return self.find_elements(self.STREAMER_CARDS)
    
    def wait_for_search_results(self):
        """Wait for search results to load."""
        self.wait_for_visible(self.SEARCH_RESULTS)
    
    def scroll_down(self, times=1):
        """Scroll down the page a specified number of times."""
        for i in range(times):
            self.driver.execute_script("window.scrollBy(0, 500);")
            print(f"Scrolled down {i+1}/{times} times")
    
    def get_scroll_position(self):
        """Get current scroll position."""
        return self.driver.execute_script("return window.pageYOffset;")
    
    def is_streamer_thumbnail_visible(self):
        """Check if streamer thumbnail is visible."""
        try:
            return self.is_element_visible(self.STREAMER_THUMBNAIL)
        except:
            return False
    
    def get_streamer_thumbnail_src(self):
        """Get the src attribute of streamer thumbnail."""
        try:
            thumbnail = self.find_element(self.STREAMER_THUMBNAIL)
            return thumbnail.get_attribute("src")
        except:
            return None
    
    def get_streamer_thumbnail_class(self):
        """Get the class attribute of streamer thumbnail."""
        try:
            thumbnail = self.find_element(self.STREAMER_THUMBNAIL)
            return thumbnail.get_attribute("class")
        except:
            return None
    
    def select_streamer(self):
        """Select a streamer from search results."""
        try:
            # Try to find and click on a streamer
            streamer_selectors = [
                self.STREAMER_LINK,
                self.STREAMER_NAME,
                (By.XPATH, "//a[contains(@href, '/videos/')]"),
                (By.XPATH, "/html/body/div[1]/main/div/div/section[4]/div[2]/a"),
                (By.CSS_SELECTOR, "a[href*='/videos/']"),
            ]
            
            for selector in streamer_selectors:
                try:
                    if self.is_element_present(selector):
                        element = self.find_element(selector)
                        if element.tag_name == "p":
                            # Find the parent link element
                            parent_link = element.find_element(By.XPATH, "./ancestor::a")
                            # Try multiple click methods to handle interception
                            try:
                                parent_link.click()
                                print(f"Selected streamer using parent link")
                                return True
                            except Exception as click_e:
                                # Try JavaScript click if regular click fails
                                self.driver.execute_script("arguments[0].click();", parent_link)
                                print(f"Selected streamer using JavaScript click")
                                return True
                        else:
                            # Try multiple click methods to handle interception
                            try:
                                element.click()
                                print(f"Selected streamer using selector: {selector[1]}")
                                return True
                            except Exception as click_e:
                                # Try JavaScript click if regular click fails
                                self.driver.execute_script("arguments[0].click();", element)
                                print(f"Selected streamer using JavaScript click with selector: {selector[1]}")
                                return True
                except Exception as e:
                    print(f"Failed to select streamer with selector {selector[1]}: {e}")
                    continue
            
            return False
        except Exception as e:
            print(f"Error selecting streamer: {e}")
            return False
    
    def select_first_streamer(self):
        """Select the first available streamer from search results."""
        try:
            # First try to select a streamer
            if self.select_streamer():
                return True
            
            # Fallback: try to find any streamer
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
    
    def is_starcraft_ii_title_visible(self):
        """Check if StarCraft II title is visible on the game page."""
        try:
            return self.is_element_visible(self.STARCRAFT_II_TITLE)
        except:
            return False
    
    def is_follow_button_visible(self):
        """Check if Follow button is visible on the game page."""
        try:
            return self.is_element_visible(self.FOLLOW_BUTTON)
        except:
            return False

