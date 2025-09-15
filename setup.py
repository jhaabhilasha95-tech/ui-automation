#!/usr/bin/env python3
"""
Setup script for Twitch UI automation framework.
"""
import os
import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True


def check_chrome():
    """Check if Chrome browser is installed."""
    try:
        # Try to get Chrome version
        result = subprocess.run(
            ["google-chrome", "--version"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        if result.returncode == 0:
            print(f"✅ Chrome found: {result.stdout.strip()}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    try:
        # Try alternative command
        result = subprocess.run(
            ["chromium-browser", "--version"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        if result.returncode == 0:
            print(f"✅ Chromium found: {result.stdout.strip()}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("⚠️  Chrome browser not found. Please install Google Chrome.")
    return False


def create_directories():
    """Create necessary directories."""
    directories = ["screenshots", "reports", "allure-results"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")


def install_dependencies():
    """Install Python dependencies."""
    try:
        print("📦 Installing Python dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def create_env_file():
    """Create .env file from template if it doesn't exist."""
    if not os.path.exists(".env"):
        if os.path.exists("env.example"):
            import shutil
            shutil.copy("env.example", ".env")
            print("✅ Created .env file from template")
        else:
            print("⚠️  No env.example file found")
    else:
        print("✅ .env file already exists")


def run_demo():
    """Run the demo script."""
    try:
        print("\n🎮 Running framework demo...")
        subprocess.run([sys.executable, "demo.py"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Demo failed: {e}")
        return False


def main():
    """Main setup function."""
    print("🎮 Twitch UI Automation Framework Setup")
    print("=" * 50)
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    if not check_chrome():
        print("Please install Google Chrome and run setup again.")
        sys.exit(1)
    
    # Setup framework
    create_directories()
    create_env_file()
    
    if not install_dependencies():
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("\n🚀 Next steps:")
    print("1. Run demo: python demo.py")
    print("2. Run tests: python run_tests.py")
    print("3. Run specific test: python run_tests.py --type smoke")
    print("\n📚 Check README.md for detailed usage instructions")
    
    # Ask if user wants to run demo
    try:
        response = input("\nWould you like to run the demo now? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            run_demo()
    except KeyboardInterrupt:
        print("\nSetup completed. You can run the demo later with: python demo.py")


if __name__ == "__main__":
    main()
