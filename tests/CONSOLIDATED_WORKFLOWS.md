# Consolidated Workflows Documentation

This document provides an overview of the consolidated workflow test files in the `tests/` directory.

## Workflow Files

### 1. Basic Functionality Tests
**File:** `tests/test_twitch_basic_functionality.py`
**Class:** `TestTwitchBasicFunctionality`
**Description:** Combines homepage navigation, search icon functionality, and StarCraft II search

#### Test Methods:

**`test_homepage_navigation()`**
- Navigate to Twitch homepage
- Assert Twitch logo is visible
- Verify logo has correct aria-label
- Take screenshot
- Verify homepage navigation success

**`test_search_icon_functionality()`**
- Navigate to Twitch homepage
- Assert search icon is visible before clicking (SVG with 20x20 dimensions and "Browse" text)
- Click on the search icon
- Assert search input is visible and functional
- Verify search functionality works
- Take screenshots at each step

**`test_starcraft_ii_search()`**
- Navigate to Twitch homepage
- Assert search icon is visible before clicking
- Click on the search icon
- Input "StarCraft II" into search bar
- Press Enter/Return to execute search
- Assert "StarCraft II" is displaying in the search input after typing
- Assert "StarCraft II" is displaying in the search results list
- Click on StarCraft II result
- Assert StarCraft II title is displaying on results page
- Assert Follow button is displaying on results page
- Final assertion: Both title and Follow button are visible
- Take screenshots at each step

### 2. Advanced Workflow Tests
**File:** `tests/test_twitch_advanced_workflow.py`
**Class:** `TestTwitchAdvancedWorkflow`
**Description:** Combines scrolling functionality, thumbnail validation, and streamer selection with comprehensive page validation

#### Test Methods:

**`test_scroll_and_thumbnail_validation()`**
- Navigate to Twitch homepage
- Click on the search icon
- Input "StarCraft II" into search bar
- Press Enter/Return to execute search
- Click on StarCraft II result
- Scroll down 2 times to load more streamers
- Assert CranKy_Ducklings streamer thumbnail is visible after scrolling
- Verify thumbnail has correct src attribute (contains 'cranky_ducklings')
- Verify thumbnail has correct class ('tw-image')
- Take screenshots at each step
- Verify scroll functionality and thumbnail visibility

**`test_streamer_selection_and_page_validation()`**
- Navigate to Twitch homepage
- Click on the search icon
- Input "StarCraft II" into search bar
- Press Enter/Return to execute search
- Click on StarCraft II result
- Scroll down 2 times to load more streamers
- Select CranKy_Ducklings streamer from the results
- Assert streamer selection was successful
- Assert we're on a valid streamer/video page (not homepage)
- Assert page title is not empty and contains "Twitch"
- Assert video player is visible on streamer page
- Assert stream title is visible on streamer page
- Assert "Share this video" button is visible
- Assert page-main-content-wrapper is visible
- Assert CranKy_Ducklings streamer name is visible
- Assert at least one key element (video player OR stream title) is present
- Handle modal popups
- Wait until page fully loads
- Take final screenshot after all elements are verified
- Comprehensive page load validation with detailed logging

## Benefits of Consolidated Structure

### Advantages:
1. **Reduced Maintenance:** Only 2 files to maintain instead of 5
2. **Logical Grouping:** Related functionality grouped together
3. **Better Organization:** Clear separation between basic and advanced workflows
4. **Efficient Testing:** Can run individual test methods or entire test classes
5. **Shared Setup:** Common setup code can be reused within test classes
6. **Cleaner Structure:** More professional and maintainable test suite

### Test Execution:
- **Run all basic functionality tests:** `pytest tests/test_twitch_basic_functionality.py -v`
- **Run all advanced workflow tests:** `pytest tests/test_twitch_advanced_workflow.py -v`
- **Run specific test method:** `pytest tests/test_twitch_basic_functionality.py::TestTwitchBasicFunctionality::test_homepage_navigation -v`
- **Run all tests:** `pytest tests/ -v`

### Page Objects Used:
- `Homepage` - Homepage interactions and logo validation
- `SearchResultsPage` - Search functionality, scrolling, and streamer selection
- `StreamerPage` - Streamer page validation and element assertions

### Utilities Used:
- `DriverFactory` - WebDriver setup and management
- `WaitHelpers` - Explicit wait utilities
- `ScreenshotHelper` - Screenshot capture and management