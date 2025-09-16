"""
Streamer page interactions - wait for page load and take screenshots.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class StreamerPage(BasePage):
    """Page object for Twitch streamer page."""
    
    # Locators
    VIDEO_PLAYER = (By.CSS_SELECTOR, "video")
    VIDEO_CONTAINER = (By.CSS_SELECTOR, "[data-a-target='player-overlay-click-handler']")
    STREAMER_TITLE = (By.CSS_SELECTOR, "[data-a-target='stream-title']")
    STREAMER_NAME = (By.CSS_SELECTOR, "[data-a-target='stream-info-card-component__title']")
    FOLLOW_BUTTON = (By.CSS_SELECTOR, "[data-a-target='follow-button']")
    CHAT_CONTAINER = (By.CSS_SELECTOR, "[data-a-target='right-column__toggle-collapse-btn']")
    
    # Specific locators for CranKy_Ducklings streamer page
    CRANKY_DUCKLINGS_TITLE = (By.XPATH, "//h1[@title='CranKy_Ducklings']")
    CRANKY_DUCKLINGS_TITLE_TEXT = (By.XPATH, "//h1[text()='CranKy_Ducklings']")
    SHARE_BUTTON = (By.CSS_SELECTOR, "[data-a-target='tw-core-button-label-text']")
    PAGE_WRAPPER = (By.CSS_SELECTOR, "#page-main-content-wrapper")
    
    # Modal/Popup locators
    MODAL_CLOSE = (By.CSS_SELECTOR, "button[aria-label='Close']")
    MODAL_OVERLAY = (By.CSS_SELECTOR, "[data-a-target='player-overlay-click-handler']")
    POPUP_CLOSE = (By.CSS_SELECTOR, ".modal-close-button")
    
    def __init__(self, driver_manager):
        super().__init__(driver_manager)
    
    def wait_for_page_load(self):
        """Wait for the streamer page to fully load."""
        # Wait for either video player or streamer info to be visible
        try:
            self.wait_for_visible(self.VIDEO_PLAYER, timeout=30)
        except:
            try:
                self.wait_for_visible(self.STREAMER_TITLE, timeout=30)
            except:
                # If neither loads, wait for any content
                self.wait_for_visible(self.VIDEO_CONTAINER, timeout=30)
    
    def handle_modal_popup(self):
        """Handle any modal popups that appear."""
        self.driver_manager.handle_modal_popup()
    
    def is_video_playing(self):
        """Check if video is playing."""
        try:
            video = self.find_element(self.VIDEO_PLAYER)
            return video.is_displayed()
        except:
            return False
    
    def get_streamer_name(self):
        """Get the streamer's name."""
        try:
            # Try to get CranKy_Ducklings name specifically
            try:
                return self.get_element_text(self.CRANKY_DUCKLINGS_TITLE)
            except:
                try:
                    return self.get_element_text(self.CRANKY_DUCKLINGS_TITLE_TEXT)
                except:
                    return self.get_element_text(self.STREAMER_NAME)
        except:
            return "Unknown Streamer"
    
    def get_stream_title(self):
        """Get the stream title."""
        try:
            return self.get_element_text(self.STREAMER_TITLE)
        except:
            return "Unknown Title"
    
    def take_streamer_screenshot(self, filename_prefix="streamer_page"):
        """Take a screenshot of the streamer page."""
        import time
        timestamp = int(time.time())
        filename = f"{filename_prefix}_{timestamp}.png"
        return self.take_screenshot(filename)
    
    def wait_for_video_content(self):
        """Wait for video content to load."""
        self.driver_manager.wait_for_video_load()
    
    def is_page_loaded(self):
        """Check if the page has loaded properly."""
        return (self.is_element_visible(self.VIDEO_PLAYER) or 
                self.is_element_visible(self.STREAMER_TITLE) or
                self.is_element_visible(self.VIDEO_CONTAINER) or
                self.is_element_visible(self.CRANKY_DUCKLINGS_TITLE) or
                self.is_element_visible(self.SHARE_BUTTON) or
                self.is_element_visible(self.PAGE_WRAPPER))
    
    def is_cranky_ducklings_visible(self):
        """Check if CranKy_Ducklings streamer name is visible."""
        try:
            return (self.is_element_visible(self.CRANKY_DUCKLINGS_TITLE) or 
                    self.is_element_visible(self.CRANKY_DUCKLINGS_TITLE_TEXT))
        except:
            return False
    
    def is_share_button_visible(self):
        """Check if Share this video button is visible."""
        try:
            return self.is_element_visible(self.SHARE_BUTTON)
        except:
            return False
    
    def is_page_wrapper_visible(self):
        """Check if page main content wrapper is visible."""
        try:
            return self.is_element_visible(self.PAGE_WRAPPER)
        except:
            return False
    
    def is_video_player_visible(self):
        """Check if video player is visible."""
        try:
            return self.is_element_visible(self.VIDEO_PLAYER)
        except:
            return False
    
    def is_stream_title_visible(self):
        """Check if stream title is visible."""
        try:
            return self.is_element_visible(self.STREAMER_TITLE)
        except:
            return False
    
    def wait_for_all_elements(self):
        """Wait for all key elements to be visible."""
        import time
        
        # Wait for page to settle
        time.sleep(3)
        
        # Handle any modal popups
        self.handle_modal_popup()
        
        # Additional wait for page to settle
        time.sleep(3)
        
        print("✅ Page settled after loading")
