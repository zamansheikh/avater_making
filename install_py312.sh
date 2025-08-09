#!/bin/bash
# Quick fix for Python 3.12 on your Linux server

echo "🔧 Python 3.12 Compatible Installation"
echo "======================================"

# Remove old virtual environment if it exists
if [ -d "venv" ]; then
    echo "🗑️  Removing old virtual environment..."
    rm -rf venv
fi

# Create new virtual environment
echo "🔧 Creating fresh virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "⚡ Activating virtual environment..."
source venv/bin/activate

# Upgrade pip first
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install packages one by one to handle conflicts
echo "📦 Installing Django packages..."
pip install "Django>=4.2.7,<5.1"
pip install "djangorestframework>=3.14.0"
pip install "django-cors-headers>=4.3.1"
pip install "python-dotenv>=1.0.0"

echo "📦 Installing image processing packages..."
pip install "Pillow>=10.1.0"
pip install "opencv-python>=4.8.0"
pip install "numpy>=1.24.0,<2.1.0"

echo "📦 Installing AI packages for background removal..."
pip install "onnxruntime>=1.15.0"
pip install "rembg>=2.0.55"  # Latest version supporting Python 3.12

echo "📦 Installing additional dependencies..."
pip install "python-decouple>=3.8"
pip install "scikit-image>=0.21.0"

# Run Django setup
echo "🔧 Setting up Django database..."
python manage.py makemigrations
python manage.py migrate

# Create media directories
echo "📁 Creating media directories..."
mkdir -p media/uploads/original media/uploads/processed

echo ""
echo "🎉 Python 3.12 setup complete!"
echo ""
echo "🚀 To start the servers:"
echo "   source venv/bin/activate"
echo "   python manage.py runserver 0.0.0.0:8000"
echo ""
echo "🌐 Your server will be accessible at:"
echo "   http://YOUR_SERVER_IP:8000/api/"
echo ""
echo "💡 To run in background:"
echo "   nohup python manage.py runserver 0.0.0.0:8000 &"
