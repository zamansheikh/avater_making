@echo off
echo 🚀 Starting Avatar Processing Server on port 8989...
echo.
echo 📡 API Server: http://127.0.0.1:8989/api/
echo 🎭 Demo Page: http://127.0.0.1:8989/demo.html
echo 📋 API Info: http://127.0.0.1:8989/api/info/
echo ❤️ Health Check: http://127.0.0.1:8989/api/health/
echo.
echo Press Ctrl+C to stop the server
echo.

C:\Users\zaman\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\python.exe manage.py runserver 8989
pause
