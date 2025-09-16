"""
Configuration settings for the Twitch UI automation framework.
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for test settings."""
    
    # Base URL
    TWITCH_URL = "https://www.twitch.tv"
    
    # Browser settings
    BROWSER = os.getenv("BROWSER", "chrome")
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    WINDOW_SIZE = os.getenv("WINDOW_SIZE", "375,812")  # iPhone X dimensions
    
    # Mobile emulation settings
    MOBILE_EMULATION = {
        "deviceMetrics": {
            "width": 375,
            "height": 812,
            "pixelRatio": 3.0
        },
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1"
    }
    
    # Timeouts
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "10"))
    EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "20"))
    PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))
    
    # Screenshot settings
    SCREENSHOT_DIR = os.getenv("SCREENSHOT_DIR", "screenshots")
    
    # Test data
    SEARCH_TERM = "StarCraft II"
    SCROLL_COUNT = 2
    
    # Wait conditions
    MODAL_WAIT_TIMEOUT = 10
    VIDEO_LOAD_TIMEOUT = 30

