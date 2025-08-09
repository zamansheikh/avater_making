#!/usr/bin/env python
"""
Setup script for Avatar Processing Backend

This script helps set up the development environment and dependencies.
"""

import os
import sys
import subprocess
import platform


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True


def setup_virtual_environment():
    """Set up virtual environment"""
    if not os.path.exists("venv"):
        if not run_command("python -m venv venv", "Creating virtual environment"):
            return False
    
    # Activation command depends on OS
    if platform.system() == "Windows":
        activate_cmd = "venv\\Scripts\\activate"
    else:
        activate_cmd = "source venv/bin/activate"
    
    print(f"💡 To activate the virtual environment, run: {activate_cmd}")
    return True


def install_dependencies():
    """Install Python dependencies"""
    pip_cmd = "venv\\Scripts\\pip" if platform.system() == "Windows" else "venv/bin/pip"
    
    commands = [
        (f"{pip_cmd} install --upgrade pip", "Upgrading pip"),
        (f"{pip_cmd} install -r requirements.txt", "Installing dependencies")
    ]
    
    for cmd, desc in commands:
        if not run_command(cmd, desc):
            return False
    
    return True


def setup_django():
    """Set up Django project"""
    python_cmd = "venv\\Scripts\\python" if platform.system() == "Windows" else "venv/bin/python"
    
    commands = [
        (f"{python_cmd} manage.py makemigrations", "Creating migrations"),
        (f"{python_cmd} manage.py migrate", "Running migrations"),
        (f"{python_cmd} manage.py collectstatic --noinput", "Collecting static files")
    ]
    
    for cmd, desc in commands:
        if not run_command(cmd, desc):
            return False
    
    return True


def create_superuser():
    """Prompt to create Django superuser"""
    python_cmd = "venv\\Scripts\\python" if platform.system() == "Windows" else "venv/bin/python"
    
    response = input("\n🤔 Would you like to create a Django admin superuser? (y/n): ")
    if response.lower() in ['y', 'yes']:
        print("📝 Creating superuser (you'll be prompted for credentials)...")
        os.system(f"{python_cmd} manage.py createsuperuser")


def setup_media_directories():
    """Create necessary media directories"""
    directories = [
        "media",
        "media/uploads",
        "media/uploads/original",
        "media/uploads/processed"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("✅ Media directories created")


def main():
    """Main setup function"""
    print("🚀 Avatar Processing Backend Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Set up virtual environment
    if not setup_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Set up Django
    if not setup_django():
        sys.exit(1)
    
    # Create media directories
    setup_media_directories()
    
    # Create superuser
    create_superuser()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Activate the virtual environment:")
    
    if platform.system() == "Windows":
        print("   venv\\Scripts\\activate")
        print("2. Start the development server:")
        print("   python manage.py runserver")
    else:
        print("   source venv/bin/activate")
        print("2. Start the development server:")
        print("   python manage.py runserver")
    
    print("\n🌐 API endpoints will be available at:")
    print("   http://localhost:8000/api/info/")
    print("   http://localhost:8000/api/process-avatar/")
    print("   http://localhost:8000/admin/ (Django admin)")


if __name__ == "__main__":
    main()
