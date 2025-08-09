#!/usr/bin/env python3
"""
Unified server that runs both Django API and demo page on port 8989
"""

import subprocess
import threading
import time
import webbrowser
import os
import sys
from pathlib import Path

def run_django_server():
    """Run Django development server"""
    print("🚀 Starting Django API server on port 8989...")
    os.system("python manage.py runserver 8989")

def run_demo_server():
    """Wait for Django server, then open demo"""
    time.sleep(3)  # Wait for Django to start
    print("🎭 Opening demo page...")
    try:
        webbrowser.open('http://127.0.0.1:8989/demo.html')
    except:
        pass

if __name__ == "__main__":
    print("🌟 Starting Avatar Processing Server + Demo")
    print("=" * 50)
    print("📡 API Server: http://127.0.0.1:8989/api/")
    print("🎭 Demo Page: http://127.0.0.1:8989/demo.html")
    print("📋 API Info: http://127.0.0.1:8989/api/info/")
    print("❤️ Health Check: http://127.0.0.1:8989/api/health/")
    print("=" * 50)
    print("Press Ctrl+C to stop all servers")
    print()
    
    # Start demo opener in background
    demo_thread = threading.Thread(target=run_demo_server, daemon=True)
    demo_thread.start()
    
    # Run Django server (blocking)
    try:
        run_django_server()
    except KeyboardInterrupt:
        print("\n👋 Servers stopped")
