#!/usr/bin/env python3
"""
Simple HTTP server to serve the demo.html file
This avoids CORS issues with file:// protocol
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

# Get the directory where this script is located
PORT = 8989
Handler = http.server.SimpleHTTPRequestHandler

# Change to the project directory
project_dir = Path(__file__).parent
os.chdir(project_dir)

print(f"🌐 Starting HTTP server on port {PORT}...")
print(f"📁 Serving files from: {project_dir}")
print(f"🎭 Demo available at: http://localhost:{PORT}/demo.html")
print(f"🔧 API server should be running at: http://127.0.0.1:8989/")
print("\n🚀 Open http://localhost:8989/demo.html in your browser")
print("Press Ctrl+C to stop the server")

try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        # Try to open the browser automatically
        try:
            webbrowser.open(f'http://localhost:{PORT}/demo.html')
        except:
            pass
        
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\n👋 Server stopped")
except OSError as e:
    if "Address already in use" in str(e):
        print(f"❌ Port {PORT} is already in use. Try a different port or stop the existing server.")
    else:
        print(f"❌ Error starting server: {e}")
