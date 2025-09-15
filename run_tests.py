#!/usr/bin/env python3
"""
Test runner script for Twitch UI automation framework.
"""
import os
import sys
import subprocess
import argparse
from pathlib import Path


def create_directories():
    """Create necessary directories for test execution."""
    directories = ["screenshots", "reports", "allure-results"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"Created directory: {directory}")


def run_tests(test_type="all", verbose=False, headless=False):
    """
    Run tests based on the specified type.
    
    Args:
        test_type (str): Type of tests to run (all, smoke, regression)
        verbose (bool): Run tests in verbose mode
        headless (bool): Run tests in headless mode
    """
    create_directories()
    
    # Base pytest command
    cmd = ["python3", "-m", "pytest"]
    
    # Add test selection
    if test_type == "smoke":
        cmd.extend(["-m", "smoke"])
    elif test_type == "regression":
        cmd.extend(["-m", "regression"])
    
    # Add verbosity
    if verbose:
        cmd.append("-v")
    
    # Add headless mode
    if headless:
        os.environ["HEADLESS"] = "true"
    
    # Add test path
    cmd.append("tests/")
    
    print(f"Running command: {' '.join(cmd)}")
    print(f"Test type: {test_type}")
    print(f"Headless mode: {headless}")
    print("-" * 50)
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n" + "=" * 50)
        print("✅ All tests completed successfully!")
        print("📊 Check the reports/ directory for detailed results")
        print("📸 Check the screenshots/ directory for test screenshots")
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Tests failed with exit code: {e.returncode}")
        return e.returncode


def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(description="Twitch UI Automation Test Runner")
    parser.add_argument(
        "--type", 
        choices=["all", "smoke", "regression"], 
        default="all",
        help="Type of tests to run (default: all)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Run tests in verbose mode"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run tests in headless mode"
    )
    
    args = parser.parse_args()
    
    print("🎮 Twitch UI Automation Test Runner")
    print("=" * 50)
    
    exit_code = run_tests(
        test_type=args.type,
        verbose=args.verbose,
        headless=args.headless
    )
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
