#!/usr/bin/env python3
"""
Script to create a demo GIF showing the Twitch automation framework in action.
This script runs the automation and captures screenshots to create a GIF.
"""
import time
import os
from PIL import Image
from utils.driver_manager import DriverManager
from pages.twitch_home_page import TwitchHomePage
from pages.twitch_streamer_page import TwitchStreamerPage
from config.config import Config


def capture_screenshots_for_gif():
    """Capture screenshots at key points for GIF creation."""
    print("🎬 Creating demo GIF - capturing screenshots...")
    
    driver_manager = DriverManager()
    config = Config()
    screenshots = []
    
    try:
        # Setup driver
        driver_manager.setup_driver()
        driver_manager.navigate_to_twitch()
        
        home_page = TwitchHomePage(driver_manager)
        streamer_page = TwitchStreamerPage(driver_manager)
        
        # Step 1: Homepage
        print("📸 Capturing homepage...")
        screenshot_path = home_page.take_screenshot("gif_step1_homepage.png")
        screenshots.append(screenshot_path)
        time.sleep(2)
        
        # Step 2: Click search
        print("📸 Capturing search click...")
        home_page.click_search_icon()
        time.sleep(1)
        screenshot_path = home_page.take_screenshot("gif_step2_search_clicked.png")
        screenshots.append(screenshot_path)
        time.sleep(2)
        
        # Step 3: Search input
        print("📸 Capturing search input...")
        home_page.search_for_term(config.SEARCH_TERM)
        time.sleep(2)
        screenshot_path = home_page.take_screenshot("gif_step3_search_input.png")
        screenshots.append(screenshot_path)
        time.sleep(2)
        
        # Step 4: Search results
        print("📸 Capturing search results...")
        home_page.wait_for_search_results()
        screenshot_path = home_page.take_screenshot("gif_step4_search_results.png")
        screenshots.append(screenshot_path)
        time.sleep(2)
        
        # Step 5: After scrolling
        print("📸 Capturing after scroll...")
        driver_manager.scroll_page(config.SCROLL_COUNT)
        time.sleep(2)
        screenshot_path = home_page.take_screenshot("gif_step5_after_scroll.png")
        screenshots.append(screenshot_path)
        time.sleep(2)
        
        # Step 6: Streamer selection
        print("📸 Capturing streamer selection...")
        if home_page.select_first_streamer():
            time.sleep(3)
            streamer_page.wait_for_page_load()
            streamer_page.handle_modal_popup()
            time.sleep(2)
            screenshot_path = streamer_page.take_streamer_screenshot("gif_step6_streamer_page")
            screenshots.append(screenshot_path)
        
        print(f"✅ Captured {len(screenshots)} screenshots for GIF creation")
        return screenshots
        
    except Exception as e:
        print(f"❌ Error capturing screenshots: {e}")
        return screenshots
        
    finally:
        driver_manager.quit_driver()


def create_gif_from_screenshots(screenshots, output_path="demo_automation.gif", duration=2000):
    """Create a GIF from the captured screenshots."""
    if not screenshots:
        print("❌ No screenshots to create GIF")
        return None
    
    print(f"🎬 Creating GIF from {len(screenshots)} screenshots...")
    
    try:
        # Load images
        images = []
        for screenshot_path in screenshots:
            if os.path.exists(screenshot_path):
                img = Image.open(screenshot_path)
                # Resize to standard size for GIF
                img = img.resize((400, 600), Image.Resampling.LANCZOS)
                images.append(img)
        
        if not images:
            print("❌ No valid images found")
            return None
        
        # Create GIF
        images[0].save(
            output_path,
            save_all=True,
            append_images=images[1:],
            duration=duration,
            loop=0
        )
        
        print(f"✅ GIF created successfully: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"❌ Error creating GIF: {e}")
        return None


def main():
    """Main function to create demo GIF."""
    print("🎮 Twitch UI Automation - Demo GIF Creator")
    print("=" * 50)
    
    # Capture screenshots
    screenshots = capture_screenshots_for_gif()
    
    if screenshots:
        # Create GIF
        gif_path = create_gif_from_screenshots(screenshots)
        
        if gif_path:
            print(f"\n🎉 Demo GIF created successfully!")
            print(f"📁 Location: {gif_path}")
            print(f"📏 Size: {os.path.getsize(gif_path)} bytes")
            print("\n💡 You can now use this GIF in your README.md file")
        else:
            print("❌ Failed to create GIF")
    else:
        print("❌ No screenshots captured")


if __name__ == "__main__":
    main()
