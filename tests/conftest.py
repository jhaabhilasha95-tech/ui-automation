"""
Pytest configuration and fixtures for the Twitch UI automation framework.
"""
import pytest
import os
from utils.driver_manager import DriverManager
from pages.twitch_home_page import TwitchHomePage
from pages.twitch_streamer_page import TwitchStreamerPage


@pytest.fixture(scope="function")
def driver_manager():
    """Create and manage WebDriver instance."""
    driver_manager = DriverManager()
    driver_manager.setup_driver()
    yield driver_manager
    driver_manager.quit_driver()


@pytest.fixture(scope="function")
def twitch_home_page(driver_manager):
    """Create Twitch home page instance."""
    return TwitchHomePage(driver_manager)


@pytest.fixture(scope="function")
def twitch_streamer_page(driver_manager):
    """Create Twitch streamer page instance."""
    return TwitchStreamerPage(driver_manager)


@pytest.fixture(scope="function")
def setup_twitch_home(driver_manager, twitch_home_page):
    """Navigate to Twitch home page."""
    driver_manager.navigate_to_twitch()
    return twitch_home_page


def pytest_configure(config):
    """Configure pytest with custom settings."""
    # Create screenshots directory if it doesn't exist
    screenshot_dir = "screenshots"
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)


def pytest_html_report_title(report):
    """Set custom title for HTML report."""
    report.title = "Twitch UI Automation Test Report"


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Configure pytest options."""
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as regression test"
    )
