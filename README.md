# 🎮 Twitch UI Automation Framework

A comprehensive Selenium-based UI automation framework for testing Twitch web application using mobile emulation in Google Chrome.

## 📋 Overview

This framework implements the required test case for Twitch UI automation:

1. **Go to Twitch** - Navigate to the Twitch homepage
2. **Click in the search icon** - Access the search functionality
3. **Input StarCraft II** - Search for the specified game
4. **Scroll down 2 times** - Navigate through search results
5. **Select one streamer** - Choose a streamer from the results
6. **Wait until all is load and take a screenshot** - Capture the streamer page

## 🚀 Features

- **Mobile Emulation**: Uses Chrome's mobile emulation for iPhone X viewport
- **Page Object Model**: Clean, maintainable code structure
- **Robust Error Handling**: Handles modal popups and dynamic content
- **Screenshot Capture**: Automatic screenshot generation for verification
- **Pytest Integration**: Professional test runner with detailed reporting
- **CI/CD Ready**: GitHub Actions workflow included

## 🏗️ Project Structure

```
twitch-ui-automation/
├── config/                 # Configuration files
│   ├── __init__.py
│   └── config.py          # Test configuration and settings
├── pages/                  # Page Object Model
│   ├── __init__.py
│   ├── base_page.py       # Base page class with common functionality
│   ├── twitch_home_page.py # Twitch homepage object
│   └── twitch_streamer_page.py # Streamer page object
├── tests/                  # Test cases
│   ├── __init__.py
│   ├── conftest.py        # Pytest fixtures and configuration
│   └── test_twitch_automation.py # Main test cases
├── utils/                  # Utility classes
│   ├── __init__.py
│   └── driver_manager.py  # WebDriver management and utilities
├── screenshots/            # Test screenshots (generated)
├── reports/               # Test reports (generated)
├── requirements.txt       # Python dependencies
├── pytest.ini           # Pytest configuration
├── run_tests.py         # Test runner script
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- Google Chrome browser
- Git

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd twitch-ui-automation
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Copy environment configuration:**
   ```bash
   cp env.example .env
   ```

## 🧪 Running Tests

### Quick Start

Run all tests:
```bash
python run_tests.py
```

### Advanced Usage

Run specific test types:
```bash
# Run only smoke tests
python run_tests.py --type smoke

# Run only regression tests
python run_tests.py --type regression

# Run with verbose output
python run_tests.py --verbose

# Run in headless mode
python run_tests.py --headless
```

### Using Pytest Directly

```bash
# Run all tests
pytest

# Run with HTML report
pytest --html=reports/report.html --self-contained-html

# Run specific test
pytest tests/test_twitch_automation.py::TestTwitchAutomation::test_twitch_search_and_streamer_selection

# Run with markers
pytest -m smoke
pytest -m regression
```

## 📊 Test Results

After running tests, you'll find:

- **HTML Report**: `reports/report.html` - Detailed test results with screenshots
- **JUnit XML**: `reports/junit.xml` - For CI/CD integration
- **Screenshots**: `screenshots/` - Test execution screenshots
- **Console Output**: Detailed logging of test execution

## 🎯 Test Cases

### Main Test Case
- **`test_twitch_search_and_streamer_selection`**: Implements the complete 6-step workflow
- **`test_twitch_homepage_elements`**: Verifies homepage functionality
- **`test_mobile_emulation_verification`**: Confirms mobile emulation is working

### Test Markers
- **`@pytest.mark.smoke`**: Quick validation tests
- **`@pytest.mark.regression`**: Comprehensive test suite

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following settings:

```env
# Browser settings
BROWSER=chrome
HEADLESS=false
WINDOW_SIZE=375,812

# Timeout settings (in seconds)
IMPLICIT_WAIT=10
EXPLICIT_WAIT=20
PAGE_LOAD_TIMEOUT=30

# Screenshot settings
SCREENSHOT_DIR=screenshots

# Test settings
SEARCH_TERM=StarCraft II
SCROLL_COUNT=2
```

### Mobile Emulation

The framework automatically configures Chrome for mobile emulation:
- **Device**: iPhone X
- **Viewport**: 375x812 pixels
- **User Agent**: Mobile Safari

## 🔧 Framework Features

### Page Object Model
- **BasePage**: Common functionality for all pages
- **TwitchHomePage**: Homepage interactions and elements
- **TwitchStreamerPage**: Streamer page handling and modal management

### Driver Management
- **Automatic ChromeDriver setup** using webdriver-manager
- **Mobile emulation configuration**
- **Robust wait strategies** for dynamic content
- **Modal popup handling** for streamer pages

### Error Handling
- **Timeout management** for slow-loading content
- **Modal popup detection and dismissal**
- **Fallback locators** for different page layouts
- **Comprehensive logging** for debugging

## 🚀 CI/CD Integration

### GitHub Actions

The framework includes a GitHub Actions workflow (`.github/workflows/test.yml`) that:
- Runs tests on multiple Python versions
- Generates HTML reports
- Uploads test artifacts
- Supports both headless and headed modes

### Local CI Simulation

```bash
# Run tests as they would run in CI
python run_tests.py --headless --type regression
```

## 📸 Screenshots

The framework automatically captures screenshots at key points:
- Homepage verification
- Search results
- Streamer page final state
- Error conditions (if any)

Screenshots are saved in the `screenshots/` directory with timestamps.

## 🐛 Troubleshooting

### Common Issues

1. **ChromeDriver Issues**:
   - The framework automatically downloads the correct ChromeDriver version
   - Ensure Chrome browser is installed and up-to-date

2. **Mobile Emulation Not Working**:
   - Check that Chrome supports mobile emulation
   - Verify viewport size in browser developer tools

3. **Element Not Found**:
   - Twitch may have updated their UI
   - Check locators in page object files
   - Framework includes fallback locators

4. **Modal Popups**:
   - Framework automatically handles common modal patterns
   - Check console output for modal handling logs

### Debug Mode

Run tests with verbose output for detailed debugging:
```bash
python run_tests.py --verbose
```

## 📈 Performance

- **Test Execution Time**: ~30-60 seconds per test
- **Screenshot Generation**: Automatic with minimal overhead
- **Memory Usage**: Optimized for CI/CD environments
- **Parallel Execution**: Supported via pytest-xdist

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For issues and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review test logs and screenshots

---

**Note**: This framework is designed for educational and testing purposes. Please respect Twitch's terms of service and rate limits when running tests.
