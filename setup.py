#!/usr/bin/env python3
"""
Setup script for Avatar Processing Backend

This script helps set up the development environment and dependencies.
Cross-platform compatible (Windows, Linux, macOS).
"""

import os
import sys
import subprocess
import platform
import shutil


def find_python_command():
    """Find the correct Python command for this system"""
    # Try different Python commands in order of preference
    python_commands = ['python3', 'python', 'py']
    
    for cmd in python_commands:
        try:
            # Check if command exists and is Python 3.8+
            result = subprocess.run([cmd, '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                version_str = result.stdout.strip()
                if 'Python 3.' in version_str:
                    version_parts = version_str.split()[1].split('.')
                    major, minor = int(version_parts[0]), int(version_parts[1])
                    if major >= 3 and minor >= 8:
                        print(f"✅ Found {version_str} at: {shutil.which(cmd)}")
                        return cmd
        except (subprocess.SubprocessError, FileNotFoundError, IndexError):
            continue
    
    print("❌ No suitable Python 3.8+ installation found!")
    print("Please install Python 3.8 or higher and try again.")
    return None


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout.strip():
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr.strip()}")
        return False


def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is too old")
        print("Python 3.8 or higher is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True


def get_platform_commands(python_cmd):
    """Get platform-specific commands"""
    is_windows = platform.system() == "Windows"
    
    if is_windows:
        venv_python = "venv\\Scripts\\python.exe"
        venv_pip = "venv\\Scripts\\pip.exe"
        activate_cmd = "venv\\Scripts\\activate"
    else:
        venv_python = "venv/bin/python"
        venv_pip = "venv/bin/pip"
        activate_cmd = "source venv/bin/activate"
    
    return {
        'python': python_cmd,
        'venv_python': venv_python,
        'venv_pip': venv_pip,
        'activate': activate_cmd,
        'is_windows': is_windows
    }


def setup_virtual_environment(python_cmd):
    """Set up virtual environment"""
    if not os.path.exists("venv"):
        if not run_command(f"{python_cmd} -m venv venv", "Creating virtual environment"):
            # Try alternative venv creation methods
            print("🔄 Trying alternative venv creation...")
            if not run_command(f"{python_cmd} -m virtualenv venv", "Creating virtual environment with virtualenv"):
                return False
    
    commands = get_platform_commands(python_cmd)
    print(f"💡 To activate the virtual environment, run: {commands['activate']}")
    return True


def install_dependencies(commands):
    """Install Python dependencies"""
    install_commands = [
        (f"{commands['venv_pip']} install --upgrade pip", "Upgrading pip"),
        (f"{commands['venv_pip']} install -r requirements.txt", "Installing dependencies")
    ]
    
    for cmd, desc in install_commands:
        if not run_command(cmd, desc):
            return False
    
    return True


def setup_django(commands):
    """Set up Django project"""
    django_commands = [
        (f"{commands['venv_python']} manage.py makemigrations", "Creating migrations"),
        (f"{commands['venv_python']} manage.py migrate", "Running migrations"),
        (f"{commands['venv_python']} manage.py collectstatic --noinput", "Collecting static files")
    ]
    
    for cmd, desc in django_commands:
        if not run_command(cmd, desc):
            # Continue with other commands even if one fails
            print(f"⚠️  {desc} failed, but continuing...")
    
    return True


def create_superuser(commands):
    """Prompt to create Django superuser"""
    response = input("\n🤔 Would you like to create a Django admin superuser? (y/n): ")
    if response.lower() in ['y', 'yes']:
        print("📝 Creating superuser (you'll be prompted for credentials)...")
        os.system(f"{commands['venv_python']} manage.py createsuperuser")


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


def create_run_scripts(commands):
    """Create convenient run scripts for different platforms"""
    if commands['is_windows']:
        # Windows batch file
        with open("run_server.bat", "w") as f:
            f.write(f"""@echo off
echo 🚀 Starting Avatar Processing Server...
{commands['venv_python']} manage.py runserver
pause
""")
        
        with open("run_demo.bat", "w") as f:
            f.write(f"""@echo off
echo 🎭 Starting Demo Server...
{commands['venv_python']} serve_demo.py
pause
""")
        print("✅ Created run_server.bat and run_demo.bat")
    
    else:
        # Unix shell script
        with open("run_server.sh", "w") as f:
            f.write(f"""#!/bin/bash
echo "🚀 Starting Avatar Processing Server..."
{commands['venv_python']} manage.py runserver
""")
        
        with open("run_demo.sh", "w") as f:
            f.write(f"""#!/bin/bash
echo "🎭 Starting Demo Server..."
{commands['venv_python']} serve_demo.py
""")
        
        # Make scripts executable
        os.chmod("run_server.sh", 0o755)
        os.chmod("run_demo.sh", 0o755)
        print("✅ Created run_server.sh and run_demo.sh")


def main():
    """Main setup function"""
    print("🚀 Avatar Processing Backend Setup")
    print("=" * 50)
    print(f"🖥️  Platform: {platform.system()} {platform.release()}")
    
    # Find correct Python command
    python_cmd = find_python_command()
    if not python_cmd:
        sys.exit(1)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Get platform-specific commands
    commands = get_platform_commands(python_cmd)
    
    # Set up virtual environment
    if not setup_virtual_environment(python_cmd):
        print("❌ Failed to create virtual environment")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies(commands):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Set up Django
    setup_django(commands)
    
    # Create media directories
    setup_media_directories()
    
    # Create run scripts
    create_run_scripts(commands)
    
    # Create superuser
    create_superuser(commands)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print(f"1. Activate the virtual environment:")
    print(f"   {commands['activate']}")
    print("2. Start the servers:")
    
    if commands['is_windows']:
        print("   run_server.bat    (for API server)")
        print("   run_demo.bat      (for demo page)")
        print("   OR manually:")
        print(f"   {commands['venv_python']} manage.py runserver")
    else:
        print("   ./run_server.sh   (for API server)")
        print("   ./run_demo.sh     (for demo page)")
        print("   OR manually:")
        print(f"   {commands['venv_python']} manage.py runserver")
    
    print("\n🌐 API endpoints will be available at:")
    print("   http://localhost:8000/api/info/")
    print("   http://localhost:8000/api/process-avatar/")
    print("   http://localhost:8000/admin/ (Django admin)")
    print("\n🎭 Demo page available at:")
    print("   http://localhost:3000/demo.html")


if __name__ == "__main__":
    main()
