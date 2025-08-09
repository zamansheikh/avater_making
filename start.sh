#!/bin/bash
# Cross-platform launcher for Avatar Processing Backend
# Works on Linux, macOS, and Windows (with Git Bash or WSL)

echo "🚀 Avatar Processing Backend Launcher"
echo "======================================"

# Function to find Python command
find_python() {
    for cmd in python3 python py; do
        if command -v "$cmd" &> /dev/null; then
            if "$cmd" --version 2>&1 | grep -q "Python 3\.[89]"; then
                echo "$cmd"
                return 0
            elif "$cmd" --version 2>&1 | grep -q "Python 3\.1[0-9]"; then
                echo "$cmd"
                return 0
            fi
        fi
    done
    return 1
}

# Find Python
PYTHON_CMD=$(find_python)
if [ $? -ne 0 ]; then
    echo "❌ No suitable Python 3.8+ found!"
    echo "Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Using Python: $PYTHON_CMD"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    "$PYTHON_CMD" -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment and install dependencies
if [ -f "venv/bin/activate" ]; then
    # Unix-like systems
    source venv/bin/activate
    PYTHON_CMD="venv/bin/python"
    PIP_CMD="venv/bin/pip"
elif [ -f "venv/Scripts/activate" ]; then
    # Windows with Git Bash
    source venv/Scripts/activate
    PYTHON_CMD="venv/Scripts/python.exe"
    PIP_CMD="venv/Scripts/pip.exe"
else
    echo "❌ Virtual environment activation failed"
    exit 1
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "📦 Installing dependencies..."
    "$PIP_CMD" install -r requirements.txt
fi

# Run Django migrations
echo "🔧 Setting up Django..."
"$PYTHON_CMD" manage.py makemigrations
"$PYTHON_CMD" manage.py migrate

# Create media directories
mkdir -p media/uploads/original media/uploads/processed

echo ""
echo "🎉 Setup complete!"
echo ""
echo "🚀 To start the servers:"
echo "   API Server:  $PYTHON_CMD manage.py runserver"
echo "   Demo Server: $PYTHON_CMD serve_demo.py"
echo ""
echo "🌐 Endpoints:"
echo "   API: http://127.0.0.1:8000/api/"
echo "   Demo: http://localhost:3000/demo.html"
