"""
Screenshot helper utilities with Allure integration.
"""
import os
import time
from datetime import datetime
import allure
from allure_commons.types import AttachmentType


class ScreenshotHelper:
    """Helper class for taking and managing screenshots."""
    
    def __init__(self, driver, base_dir="screenshots"):
        self.driver = driver
        self.base_dir = base_dir
        self._ensure_screenshots_dir()
    
    def _ensure_screenshots_dir(self):
        """Ensure the screenshots directory exists."""
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)
            print(f"✅ Created screenshots directory: {self.base_dir}")
    
    def take_screenshot(self, filename=None, add_timestamp=True, attach_to_allure=True, allure_name=None):
        """Take a screenshot and save it, optionally attach to Allure report."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        
        if add_timestamp and not filename.startswith("screenshot_"):
            timestamp = int(time.time())
            name, ext = os.path.splitext(filename)
            filename = f"{name}_{timestamp}{ext}"
        
        filepath = os.path.join(self.base_dir, filename)
        
        try:
            self.driver.save_screenshot(filepath)
            print(f"📸 Screenshot saved: {filepath}")
            
            # Attach to Allure report if requested
            if attach_to_allure:
                allure_name = allure_name or f"Screenshot: {filename}"
                with open(filepath, "rb") as f:
                    allure.attach(f.read(), name=allure_name, attachment_type=AttachmentType.PNG)
                print(f"📎 Screenshot attached to Allure: {allure_name}")
            
            return filepath
        except Exception as e:
            print(f"❌ Failed to take screenshot: {e}")
            return None
    
    def take_screenshot_with_metadata(self, filename, metadata=None, attach_to_allure=True):
        """Take a screenshot with additional metadata and Allure integration."""
        filepath = self.take_screenshot(filename, attach_to_allure=attach_to_allure)
        
        if filepath and metadata:
            # Create a metadata file alongside the screenshot
            metadata_file = filepath.replace('.png', '_metadata.txt')
            try:
                with open(metadata_file, 'w') as f:
                    f.write(f"Screenshot taken at: {datetime.now().isoformat()}\n")
                    f.write(f"URL: {self.driver.current_url}\n")
                    f.write(f"Title: {self.driver.title}\n")
                    if metadata:
                        for key, value in metadata.items():
                            f.write(f"{key}: {value}\n")
                print(f"📝 Metadata saved: {metadata_file}")
                
                # Attach metadata to Allure if requested
                if attach_to_allure:
                    with open(metadata_file, "r") as f:
                        allure.attach(f.read(), name=f"Metadata: {filename}", attachment_type=AttachmentType.TEXT)
                    print(f"📎 Metadata attached to Allure: {filename}")
                    
            except Exception as e:
                print(f"⚠️ Failed to save metadata: {e}")
        
        return filepath
    
    def take_full_page_screenshot(self, filename=None, attach_to_allure=True):
        """Take a full page screenshot (including parts not visible) with Allure integration."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"fullpage_screenshot_{timestamp}.png"
        
        # Get the full page dimensions
        total_width = self.driver.execute_script("return document.body.scrollWidth")
        total_height = self.driver.execute_script("return document.body.scrollHeight")
        
        # Set window size to full page
        self.driver.set_window_size(total_width, total_height)
        
        # Take screenshot with Allure integration
        filepath = self.take_screenshot(filename, add_timestamp=False, attach_to_allure=attach_to_allure, 
                                      allure_name=f"Full Page Screenshot: {filename}")
        
        # Reset window size (optional)
        # self.driver.set_window_size(1920, 1080)
        
        return filepath
    
    def take_element_screenshot(self, element, filename=None, attach_to_allure=True):
        """Take a screenshot of a specific element with Allure integration."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"element_screenshot_{timestamp}.png"
        
        try:
            filepath = os.path.join(self.base_dir, filename)
            element.screenshot(filepath)
            print(f"📸 Element screenshot saved: {filepath}")
            
            # Attach to Allure report if requested
            if attach_to_allure:
                allure_name = f"Element Screenshot: {filename}"
                with open(filepath, "rb") as f:
                    allure.attach(f.read(), name=allure_name, attachment_type=AttachmentType.PNG)
                print(f"📎 Element screenshot attached to Allure: {allure_name}")
            
            return filepath
        except Exception as e:
            print(f"❌ Failed to take element screenshot: {e}")
            return None
    
    def cleanup_old_screenshots(self, days_old=7):
        """Clean up screenshots older than specified days."""
        try:
            current_time = time.time()
            cutoff_time = current_time - (days_old * 24 * 60 * 60)
            
            deleted_count = 0
            for filename in os.listdir(self.base_dir):
                filepath = os.path.join(self.base_dir, filename)
                if os.path.isfile(filepath):
                    file_time = os.path.getmtime(filepath)
                    if file_time < cutoff_time:
                        os.remove(filepath)
                        deleted_count += 1
            
            if deleted_count > 0:
                print(f"🧹 Cleaned up {deleted_count} old screenshots")
            else:
                print("ℹ️ No old screenshots to clean up")
                
        except Exception as e:
            print(f"⚠️ Failed to cleanup old screenshots: {e}")
    
    def get_screenshot_list(self):
        """Get a list of all screenshots in the directory."""
        try:
            screenshots = []
            for filename in os.listdir(self.base_dir):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    filepath = os.path.join(self.base_dir, filename)
                    file_info = {
                        'filename': filename,
                        'filepath': filepath,
                        'size': os.path.getsize(filepath),
                        'modified': datetime.fromtimestamp(os.path.getmtime(filepath))
                    }
                    screenshots.append(file_info)
            
            return sorted(screenshots, key=lambda x: x['modified'], reverse=True)
        except Exception as e:
            print(f"⚠️ Failed to get screenshot list: {e}")
            return []
    
    def attach_screenshot_to_allure(self, filepath, name=None):
        """Attach an existing screenshot file to Allure report."""
        try:
            if not os.path.exists(filepath):
                print(f"❌ Screenshot file not found: {filepath}")
                return False
            
            allure_name = name or f"Screenshot: {os.path.basename(filepath)}"
            with open(filepath, "rb") as f:
                allure.attach(f.read(), name=allure_name, attachment_type=AttachmentType.PNG)
            print(f"📎 Screenshot attached to Allure: {allure_name}")
            return True
        except Exception as e:
            print(f"❌ Failed to attach screenshot to Allure: {e}")
            return False
    
    def take_screenshot_on_failure(self, test_name=None):
        """Take a screenshot specifically for test failure scenarios."""
        if test_name is None:
            test_name = "test_failure"
        
        filename = f"failure_{test_name}_{int(time.time())}.png"
        filepath = self.take_screenshot(filename, add_timestamp=False, 
                                      attach_to_allure=True, 
                                      allure_name=f"Test Failure Screenshot: {test_name}")
        return filepath
    
    def take_screenshot_on_success(self, test_name=None):
        """Take a screenshot specifically for test success scenarios."""
        if test_name is None:
            test_name = "test_success"
        
        filename = f"success_{test_name}_{int(time.time())}.png"
        filepath = self.take_screenshot(filename, add_timestamp=False, 
                                      attach_to_allure=True, 
                                      allure_name=f"Test Success Screenshot: {test_name}")
        return filepath
    
    def attach_page_source_to_allure(self, name="Page Source"):
        """Attach current page source to Allure report."""
        try:
            page_source = self.driver.page_source
            allure.attach(page_source, name=name, attachment_type=AttachmentType.HTML)
            print(f"📎 Page source attached to Allure: {name}")
            return True
        except Exception as e:
            print(f"❌ Failed to attach page source to Allure: {e}")
            return False
    
    def attach_browser_logs_to_allure(self, name="Browser Logs"):
        """Attach browser logs to Allure report."""
        try:
            logs = self.driver.get_log('browser')
            if logs:
                log_text = "\n".join([f"{log['timestamp']}: {log['level']} - {log['message']}" for log in logs])
                allure.attach(log_text, name=name, attachment_type=AttachmentType.TEXT)
                print(f"📎 Browser logs attached to Allure: {name}")
                return True
            else:
                print("ℹ️ No browser logs found")
                return False
        except Exception as e:
            print(f"❌ Failed to attach browser logs to Allure: {e}")
            return False
