"""
Pytest configuration and fixtures for the Twitch UI automation framework.
"""
import pytest
import os
from utils.driver_factory import DriverFactory
from pages.homepage import Homepage
from pages.search_results_page import SearchResultsPage
from pages.streamer_page import StreamerPage


@pytest.fixture(scope="function")
def driver_manager():
    """Create and manage WebDriver instance."""
    driver_manager = DriverFactory()
    driver_manager.setup_driver()
    yield driver_manager
    driver_manager.quit_driver()


@pytest.fixture(scope="function")
def homepage(driver_manager):
    """Create Homepage instance."""
    return Homepage(driver_manager)


@pytest.fixture(scope="function")
def search_results_page(driver_manager):
    """Create SearchResultsPage instance."""
    return SearchResultsPage(driver_manager)


@pytest.fixture(scope="function")
def streamer_page(driver_manager):
    """Create StreamerPage instance."""
    return StreamerPage(driver_manager)


@pytest.fixture(scope="function")
def setup_twitch_home(driver_manager, homepage):
    """Navigate to Twitch home page."""
    driver_manager.navigate_to_twitch()
    return homepage


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
