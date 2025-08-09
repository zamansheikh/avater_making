@echo off
echo 🚀 Starting Avatar Processing Server on port 8989...
echo.
echo 📡 Server will be available at:
echo    http://127.0.0.1:8989/api/
echo    http://localhost:8989/api/
echo.
echo 🎭 Demo page will be available at:
echo    http://127.0.0.1:8989/demo.html
echo    http://localhost:8989/demo.html
echo.
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver 8989
pause
