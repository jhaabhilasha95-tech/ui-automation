"""
Twitch streamer page object model.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class TwitchStreamerPage(BasePage):
    """Page object for Twitch streamer page."""
    
    # Locators
    VIDEO_PLAYER = (By.CSS_SELECTOR, "video")
    VIDEO_CONTAINER = (By.CSS_SELECTOR, "[data-a-target='player-overlay-click-handler']")
    STREAMER_TITLE = (By.CSS_SELECTOR, "[data-a-target='stream-title']")
    STREAMER_NAME = (By.CSS_SELECTOR, "[data-a-target='stream-info-card-component__title']")
    FOLLOW_BUTTON = (By.CSS_SELECTOR, "[data-a-target='follow-button']")
    CHAT_CONTAINER = (By.CSS_SELECTOR, "[data-a-target='right-column__toggle-collapse-btn']")
    
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
                self.is_element_visible(self.VIDEO_CONTAINER))
