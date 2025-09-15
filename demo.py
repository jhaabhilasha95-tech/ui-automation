#!/usr/bin/env python3
"""
Demo script to showcase the Twitch UI automation framework.
This script demonstrates the framework capabilities without running full tests.
"""
import time
from utils.driver_manager import DriverManager
from pages.twitch_home_page import TwitchHomePage
from pages.twitch_streamer_page import TwitchStreamerPage
from config.config import Config


def demo_twitch_automation():
    """Demonstrate the Twitch automation framework."""
    print("🎮 Twitch UI Automation Framework Demo")
    print("=" * 50)
    
    # Initialize components
    driver_manager = DriverManager()
    config = Config()
    
    try:
        # Setup driver
        print("1. Setting up Chrome WebDriver with mobile emulation...")
        driver_manager.setup_driver()
        
        # Navigate to Twitch
        print("2. Navigating to Twitch homepage...")
        driver_manager.navigate_to_twitch()
        
        # Initialize page objects
        home_page = TwitchHomePage(driver_manager)
        streamer_page = TwitchStreamerPage(driver_manager)
        
        # Take homepage screenshot
        print("3. Taking homepage screenshot...")
        home_page.take_screenshot("demo_homepage.png")
        
        # Demonstrate search functionality
        print("4. Demonstrating search functionality...")
        if home_page.is_search_visible():
            print("   ✅ Search functionality is available")
            home_page.click_search_icon()
            time.sleep(1)
            home_page.take_screenshot("demo_search_clicked.png")
        else:
            print("   ⚠️  Search functionality not immediately visible")
        
        # Check mobile emulation
        print("5. Verifying mobile emulation...")
        user_agent = driver_manager.driver.execute_script("return navigator.userAgent;")
        viewport = driver_manager.driver.execute_script(
            "return {width: window.innerWidth, height: window.innerHeight};"
        )
        
        print(f"   User Agent: {user_agent[:50]}...")
        print(f"   Viewport: {viewport['width']}x{viewport['height']}")
        
        if "iPhone" in user_agent or "Mobile" in user_agent:
            print("   ✅ Mobile emulation is active")
        else:
            print("   ⚠️  Mobile emulation may not be working correctly")
        
        # Demonstrate modal handling
        print("6. Demonstrating modal handling capabilities...")
        driver_manager.handle_modal_popup()
        print("   ✅ Modal handling completed")
        
        # Take final screenshot
        print("7. Taking final demonstration screenshot...")
        home_page.take_screenshot("demo_final.png")
        
        print("\n" + "=" * 50)
        print("✅ Demo completed successfully!")
        print("📸 Check the screenshots/ directory for demo images")
        print("🚀 Ready to run full test suite with: python run_tests.py")
        
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Cleanup
        print("\n8. Cleaning up...")
        driver_manager.quit_driver()
        print("✅ Demo cleanup completed")


if __name__ == "__main__":
    demo_twitch_automation()
