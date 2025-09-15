"""
Test cases for Twitch UI automation.
"""
import pytest
import time
from config.config import Config


class TestTwitchAutomation:
    """Test class for Twitch UI automation scenarios."""
    
    @pytest.mark.smoke
    def test_twitch_search_and_streamer_selection(self, setup_twitch_home, twitch_streamer_page, driver_manager):
        """
        Test case: Search for StarCraft II, scroll down, and select a streamer.
        
        Steps:
        1. Go to Twitch
        2. Click in the search icon
        3. Input StarCraft II
        4. Scroll down 2 times
        5. Select one streamer
        6. On the streamer page wait until all is load and take a screenshot
        """
        config = Config()
        home_page = setup_twitch_home
        
        # Step 1: Go to Twitch (already done in setup_twitch_home fixture)
        print("Step 1: Navigated to Twitch homepage")
        
        # Step 2: Click in the search icon
        home_page.click_search_icon()
        print("Step 2: Clicked search icon")
        
        # Wait for search input to be visible
        home_page.wait_for_visible(home_page.SEARCH_INPUT, timeout=10)
        print("Search input is now visible")
        
        # Step 3: Input StarCraft II
        home_page.search_for_term(config.SEARCH_TERM)
        print(f"Step 3: Searched for '{config.SEARCH_TERM}'")
        
        # Wait for search results
        time.sleep(2)  # Allow time for search results to load
        home_page.wait_for_search_results()
        print("Search results loaded")
        
        # Step 4: Scroll down 2 times
        driver_manager.scroll_page(config.SCROLL_COUNT)
        print(f"Step 4: Scrolled down {config.SCROLL_COUNT} times")
        
        # Step 5: Select one streamer
        streamer_selected = home_page.select_first_streamer()
        assert streamer_selected, "Failed to select a streamer from search results"
        print("Step 5: Selected first available streamer")
        
        # Step 6: On the streamer page wait until all is load and take a screenshot
        # Wait for page to load
        twitch_streamer_page.wait_for_page_load()
        print("Streamer page loaded")
        
        # Handle any modal popups
        twitch_streamer_page.handle_modal_popup()
        print("Handled modal popups if any")
        
        # Wait for video content to load
        twitch_streamer_page.wait_for_video_content()
        print("Video content loaded")
        
        # Take screenshot
        screenshot_path = twitch_streamer_page.take_streamer_screenshot("twitch_streamer_test")
        print(f"Step 6: Screenshot taken and saved at: {screenshot_path}")
        
        # Verify page loaded successfully
        assert twitch_streamer_page.is_page_loaded(), "Streamer page did not load properly"
        
        # Get streamer information
        streamer_name = twitch_streamer_page.get_streamer_name()
        stream_title = twitch_streamer_page.get_stream_title()
        
        print(f"Streamer: {streamer_name}")
        print(f"Stream Title: {stream_title}")
        
        # Verify we're on a streamer page
        assert streamer_name != "Unknown Streamer", "Could not identify streamer name"
        assert stream_title != "Unknown Title", "Could not identify stream title"
        
        print("✅ All test steps completed successfully!")
    
    @pytest.mark.regression
    def test_twitch_homepage_elements(self, setup_twitch_home):
        """Test that Twitch homepage loads correctly with mobile emulation."""
        home_page = setup_twitch_home
        
        # Verify search functionality is available
        assert home_page.is_search_visible(), "Search functionality not visible on homepage"
        
        # Take screenshot of homepage
        screenshot_path = home_page.take_screenshot("twitch_homepage_mobile")
        print(f"Homepage screenshot saved: {screenshot_path}")
        
        print("✅ Homepage test completed successfully!")
    
    @pytest.mark.regression
    def test_mobile_emulation_verification(self, driver_manager):
        """Test that mobile emulation is working correctly."""
        driver_manager.navigate_to_twitch()
        
        # Check user agent
        user_agent = driver_manager.driver.execute_script("return navigator.userAgent;")
        print(f"User Agent: {user_agent}")
        
        # Check viewport size
        viewport_size = driver_manager.driver.execute_script(
            "return {width: window.innerWidth, height: window.innerHeight};"
        )
        print(f"Viewport Size: {viewport_size}")
        
        # Verify mobile emulation is active
        assert "iPhone" in user_agent or "Mobile" in user_agent, "Mobile emulation not active"
        assert viewport_size["width"] <= 400, "Viewport width too large for mobile emulation"
        
        print("✅ Mobile emulation verification completed successfully!")
