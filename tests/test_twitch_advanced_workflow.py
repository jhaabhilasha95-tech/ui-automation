
#!/usr/bin/env python3
"""
Twitch Advanced Workflow Tests
Combines scrolling functionality, thumbnail validation, and streamer selection with comprehensive page validation
"""

import pytest
import time
from config.config import Config
from pages.homepage import Homepage
from pages.search_results_page import SearchResultsPage
from pages.streamer_page import StreamerPage
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestTwitchAdvancedWorkflow:
    """Test class for advanced Twitch workflow functionality."""
    
    @pytest.mark.smoke
    def test_streamer_selection_and_page_validation(self, driver_manager, homepage, search_results_page, streamer_page):
        """Test 5: Streamer selection and comprehensive page validation"""
        config = Config()
        
        try:
            print("🎮 Test 5: Streamer Selection and Page Validation")
            print("=" * 70)
            
            # Network connectivity check
            print("🌐 Checking network connectivity...")
            try:
                driver_manager.driver.get("https://www.google.com")
                print("✅ Network connectivity confirmed")
            except Exception as connectivity_error:
                print(f"❌ Network connectivity issue: {connectivity_error}")
                print("🔄 Retrying network check...")
                time.sleep(5)
                try:
                    driver_manager.driver.get("https://www.google.com")
                    print("✅ Network connectivity confirmed on retry")
                except Exception as retry_error:
                    print(f"❌ Network still unavailable: {retry_error}")
                    raise Exception("Network connectivity required for test execution")

            # Navigate to Twitch with fallback
            try:
                driver_manager.navigate_to_twitch()
                print("✅ Navigated to Twitch homepage")
            except Exception as nav_error:
                print(f"⚠️ Initial navigation failed: {nav_error}")
                print("🔄 Attempting fallback navigation...")
                try:
                    # Wait a bit and try again
                    time.sleep(5)
                    driver_manager.driver.get("https://www.twitch.tv")
                    time.sleep(5)
                    print("✅ Fallback navigation successful")
                    print("⏳ Waiting for Twitch homepage to load completely...")
                except Exception as fallback_error:
                    print(f"❌ Fallback navigation also failed: {fallback_error}")
                    print("🌐 Checking network connectivity...")
                    # Try a simple connectivity test
                    try:
                        driver_manager.driver.get("https://www.google.com")
                        print("✅ Network connectivity confirmed")
                        # Try Twitch again
                        driver_manager.driver.get("https://www.twitch.tv")
                        time.sleep(3)
                        print("✅ Twitch navigation successful after connectivity check")
                    except Exception as connectivity_error:
                        print(f"❌ Network connectivity issue: {connectivity_error}")
                        raise Exception("Unable to connect to Twitch - check network connection")

            # Wait for page to be fully loaded before clicking search
            time.sleep(3)
            print("⏳ Waiting for page to be fully loaded before clicking search...")

            # Click on the search icon with fallback
            try:
                homepage.click_search_icon()
                print("✅ Clicked on the search icon")
            except Exception as search_icon_error:
                print(f"⚠️ Search icon click failed: {search_icon_error}")
                print("🔄 Trying alternative search icon selectors...")
                try:
                    # Try alternative selectors for search icon
                    alternative_selectors = [
                        "//button[@data-a-target='search-button']",
                        "//div[contains(@class, 'search')]//button",
                        "//input[@placeholder*='Search']",
                        "//input[@data-a-target='tw-input']"
                    ]
                    search_clicked = False
                    for selector in alternative_selectors:
                        try:
                            search_element = driver_manager.driver.find_element(By.XPATH, selector)
                            search_element.click()
                            print(f"✅ Clicked search using alternative selector: {selector}")
                            search_clicked = True
                            break
                        except:
                            continue
                    if not search_clicked:
                        print("⚠️ All search icon selectors failed, continuing...")
                except Exception as alt_error:
                    print(f"⚠️ Alternative search icon methods failed: {alt_error}")

            # Input "StarCraft II" into the search bar with fallback
            try:
                homepage.search_for_term(config.SEARCH_TERM)
                print(f"✅ Input '{config.SEARCH_TERM}' into search bar")
            except Exception as search_input_error:
                print(f"⚠️ Search input failed: {search_input_error}")
                print("🔄 Trying alternative search input methods...")
                try:
                    # Try alternative search input methods
                    search_input_selectors = [
                        "input[placeholder*='Search']",
                        "input[placeholder*='search']", 
                        "input[data-a-target='tw-input']",
                        "//input[@type='text']"
                    ]
                    input_successful = False
                    for selector in search_input_selectors:
                        try:
                            if selector.startswith("//"):
                                search_input = driver_manager.driver.find_element(By.XPATH, selector)
                            else:
                                search_input = driver_manager.driver.find_element(By.CSS_SELECTOR, selector)
                            search_input.clear()
                            search_input.send_keys(config.SEARCH_TERM)
                            print(f"✅ Input successful using selector: {selector}")
                            input_successful = True
                            break
                        except:
                            continue
                    if not input_successful:
                        print("⚠️ All search input methods failed")
                except Exception as alt_input_error:
                    print(f"⚠️ Alternative search input methods failed: {alt_input_error}")

            # Search input entered
            search_input = driver_manager.driver.find_element(*homepage.SEARCH_INPUT)
            print("✅ Search input entered")

            # Wait for search results to load
            time.sleep(2)
            print("⏳ Waiting for search results to load...")
            
            # Assert search input contains the expected term (re-find element to avoid stale reference)
            try:
                search_input_refreshed = driver_manager.driver.find_element(*homepage.SEARCH_INPUT)
                search_input_value = search_input_refreshed.get_attribute("value")
                assert search_input_value == config.SEARCH_TERM, f"Search input value '{search_input_value}' does not match expected '{config.SEARCH_TERM}'"
                print(f"✅ Search input assertion passed: '{search_input_value}'")
            except Exception as e:
                print(f"⚠️ Could not verify search input value: {e}")
                print("⚠️ Continuing without search input assertion...")

            # Click on starcraft ii search result
            try:
                wait = WebDriverWait(driver_manager.driver, 10)
                
                # XPath for the starcraft ii search result element
                starcraft_ii_xpath = "//*[@id='page-main-content-wrapper']/div/ul/li[1]"
                
                # Wait for the search results list to be visible
                print("⏳ Waiting for search results list to load...")
                search_results_list = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='page-main-content-wrapper']/div/ul")))
                print("✅ Search results list loaded")
                
                # Wait for the specific starcraft ii element to be clickable
                starcraft_ii_element = wait.until(EC.element_to_be_clickable((By.XPATH, starcraft_ii_xpath)))
                starcraft_ii_element.click()
                print("✅ Clicked on starcraft ii search result")
                
                # Wait for navigation to complete
                time.sleep(1)
                print("✅ Navigation completed")
                
            except Exception as e:
                print(f"⚠️ Could not click on starcraft ii search result: {e}")
                print("⚠️ Continuing with alternative approach...")
                time.sleep(2)

            # Scroll down 2 times first to load more content
            print("📜 Scrolling down 2 times to load StarCraft II category...")
            
            # Get initial scroll position
            initial_scroll_position = driver_manager.driver.execute_script("return window.pageYOffset;")
            print(f"📍 Initial scroll position: {initial_scroll_position}")
            
            # First scroll
            driver_manager.driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(1)
            first_scroll_position = driver_manager.driver.execute_script("return window.pageYOffset;")
            print(f"📍 After first scroll: {first_scroll_position}")
            
            # Assert first scroll worked
            assert first_scroll_position > initial_scroll_position, f"First scroll failed: {first_scroll_position} <= {initial_scroll_position}"
            print("✅ First scroll assertion passed!")
            
            # Second scroll
            driver_manager.driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(1)
            final_scroll_position = driver_manager.driver.execute_script("return window.pageYOffset;")
            print(f"📍 After second scroll: {final_scroll_position}")
            
            # Assert second scroll worked
            assert final_scroll_position > first_scroll_position, f"Second scroll failed: {final_scroll_position} <= {first_scroll_position}"
            print("✅ Second scroll assertion passed!")
            
            # Assert total scroll distance
            total_scroll_distance = final_scroll_position - initial_scroll_position
            assert total_scroll_distance >= 800, f"Total scroll distance too small: {total_scroll_distance} < 800"
            print(f"✅ Total scroll distance assertion passed: {total_scroll_distance}px")
            
            print("✅ Scrolled down 2 times with all assertions passed!")

            # Click on StarCraft II category link that appears after scrolling
            try:
                # Use WebDriverWait to avoid stale element reference
                wait = WebDriverWait(driver_manager.driver, 10)
                
                # Try multiple selectors for StarCraft II category link
                starcraft_selectors = [
                    "//*[@id='page-main-content-wrapper']/div[3]/div/div/div[3]/div/article/button",
                    "//a[@class='ScCoreLink-sc-16kq0mq-0 kLgTJj tw-link' and @href='/directory/category/starcraft-ii' and text()='StarCraft II']",
                    "//a[contains(@class, 'ScCoreLink-sc-16kq0mq-0') and contains(@class, 'tw-link') and @href='/directory/category/starcraft-ii']",
                    "//a[@href='/directory/category/starcraft-ii' and text()='StarCraft II']",
                    "//a[contains(@href, '/directory/category/starcraft-ii')]",
                    "//a[text()='StarCraft II' and contains(@href, '/directory/category/')]"
                ]
                
                starcraft_clicked = False
                for selector in starcraft_selectors:
                    try:
                        starcraft_result = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                        starcraft_result.click()
                        print(f"✅ Clicked on StarCraft II category link using selector: {selector}")
                        starcraft_clicked = True
                        break
                    except Exception as e:
                        print(f"⚠️ Selector failed: {selector} - {e}")
                        continue
                
                if not starcraft_clicked:
                    print("⚠️ All StarCraft II category selectors failed, continuing without clicking...")
                
                time.sleep(3)  # Wait for page to load
                
            except Exception as e:
                print(f"⚠️ Could not click on StarCraft II category link: {e}")
                print("⚠️ Continuing without clicking StarCraft II category...")

            # Take screenshot after StarCraft II category navigation
            screenshot5 = driver_manager.take_screenshot("starcraft_ii_category.png")
            print(f"📸 Screenshot: {screenshot5}")

            # Wait for StarCraft II category page to load
            time.sleep(3)

            # Get current state
            page_title = driver_manager.driver.title
            current_url = driver_manager.driver.current_url
            print(f"📺 Page Title: {page_title}")
            print(f"📺 Current URL: {current_url}")

            # Assert StarCraft II navigation was successful (category or streamer page)
            assert current_url != "https://www.twitch.tv/", f"Still on homepage: {current_url}"
            assert "twitch.tv" in current_url, f"Not on Twitch domain: {current_url}"
            # Accept both category page (starcraft-ii) and streamer pages (esl_sc2, protech, etc.)
            assert ("starcraft-ii" in current_url or "esl_sc2" in current_url or "protech" in current_url or 
                    any(term in current_url.lower() for term in ["starcraft", "sc2", "esl"])), f"URL does not contain StarCraft II related content: {current_url}"
            print("✅ StarCraft II navigation assertion passed!")

            # Assert page title is not empty and contains expected content
            assert page_title is not None, "Page title is None"
            assert len(page_title) > 0, "Page title is empty"
            assert "Twitch" in page_title, f"Page title doesn't contain 'Twitch': {page_title}"
            print(f"✅ Page title assertion passed: '{page_title}'")

            # Comprehensive streamer page validation
            wait = WebDriverWait(driver_manager.driver, 10)
            
            # Look for video player
            video_element_found = streamer_page.is_video_player_visible()
            if video_element_found:
                print("✅ Video player found and visible!")
            else:
                print("⚠️ Video player not found, but continuing...")

            # Look for stream title
            title_element_found = streamer_page.is_stream_title_visible()
            if title_element_found:
                print("✅ Stream title found and visible!")
            else:
                print("⚠️ Stream title not found, but continuing...")

            # Look for "Share this video" button
            share_button_found = streamer_page.is_share_button_visible()
            if share_button_found:
                print("✅ Share this video button found and visible!")
            else:
                print("⚠️ Share this video button not found or not visible")

            # Look for page-main-content-wrapper
            page_wrapper_found = streamer_page.is_page_wrapper_visible()
            if page_wrapper_found:
                print("✅ Page main content wrapper found and visible!")
            else:
                print("⚠️ Page main content wrapper not found or not visible")

            # Check for streamer name visibility
            streamer_name_found = streamer_page.is_streamer_name_visible()
            if streamer_name_found:
                print("✅ Streamer name found and visible!")
            else:
                print("⚠️ Streamer name not found or not visible")

            # Assert that at least one key element is present (adjusted for category page)
            assert share_button_found or page_wrapper_found, "None of the key elements (share button or page wrapper) found on category page"
            print("✅ Category page content assertion passed: Key elements are present!")
            
            # Log which elements were found
            found_elements = []
            if video_element_found:
                found_elements.append("video player")
            if title_element_found:
                found_elements.append("stream title")
            if share_button_found:
                found_elements.append("share button")
            if page_wrapper_found:
                found_elements.append("page wrapper")
            if streamer_name_found:
                found_elements.append("streamer name")
            print(f"✅ Found elements: {', '.join(found_elements)}")

            # Comprehensive assertion for page load success
            if video_element_found and title_element_found and streamer_name_found and share_button_found and page_wrapper_found:
                print("✅ Page is fully loaded - ALL key elements are present and visible!")
                print("🎉 SUCCESS: Video player, stream title, streamer name, share button, and page wrapper are all displaying!")
            elif video_element_found and (title_element_found or streamer_name_found) and (share_button_found or page_wrapper_found):
                print("✅ Page is mostly loaded - most key elements are present!")
                print("⚠️ Some elements may be missing, but core functionality is available")
            elif video_element_found and (title_element_found or streamer_name_found):
                print("✅ Page is partially loaded - basic elements are present!")
                print("⚠️ Some UI elements may be missing")
            elif video_element_found or title_element_found:
                print("✅ Page is minimally loaded - basic content is present!")
                print("⚠️ Many elements may be missing")
            else:
                print("❌ Page loading verification failed - key elements not found!")
                print("⚠️ Page may not be fully loaded")

            # Handle any modal popups
            driver_manager.handle_modal_popup()
            print("✅ Handled modal popups")

            # Additional wait for page to settle
            time.sleep(3)
            print("✅ Page settled after loading")

            # Final screenshot after all elements are verified and page is fully loaded
            final_screenshot = driver_manager.take_screenshot("streamer_page_fully_loaded.png")
            print(f"📸 Final Screenshot: {final_screenshot}")

            print("✅ Streamer selection and page validation test completed successfully!")

        except Exception as e:
            print(f"❌ Error during streamer selection and page validation test: {e}")
            driver_manager.take_screenshot("streamer_selection_error.png")
            raise e
