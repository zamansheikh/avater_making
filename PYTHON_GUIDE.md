# 🐍 Python Command Guide - Solving python vs python3 Conflicts

## 🚨 **Why the python/python3 Conflict Happens**

Different operating systems handle Python differently:

### **Windows** 🪟
- Usually uses `python` command
- Python 3 installed via Microsoft Store: `python`
- Python 3 from python.org: `python` or `py`

### **Linux** 🐧
- Often uses `python3` command
- `python` might point to Python 2.7 (legacy)
- Modern distributions: `python3` for Python 3.x

### **macOS** 🍎
- Default `python` = Python 2.7 (legacy)
- Python 3: `python3` command
- With Homebrew: usually `python3`

## ✅ **Solutions Implemented**

### **1. Smart Auto-Detection Setup Script**
The new `setup.py` automatically detects the right Python command:

```bash
# Works on any platform
python3 setup.py    # Linux/macOS
python setup.py     # Windows
```

It tries commands in this order:
1. `python3` (preferred for Linux/macOS)
2. `python` (Windows default)
3. `py` (Windows Python Launcher)

### **2. Cross-Platform Launcher**
Use the `start.sh` script (works on Linux, macOS, Windows with Git Bash):

```bash
chmod +x start.sh
./start.sh
```

### **3. Platform-Specific Run Scripts**
The setup now creates convenient scripts:

**Windows:**
- `run_server.bat` - Start API server
- `run_demo.bat` - Start demo server

**Linux/macOS:**
- `run_server.sh` - Start API server  
- `run_demo.sh` - Start demo server

## 🔧 **Manual Commands for Each Platform**

### **Linux/Ubuntu/Debian:**
```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate

# Run
python manage.py runserver
```

### **macOS:**
```bash
# Setup (with Homebrew Python)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate

# Run
python manage.py runserver
```

### **Windows:**
```batch
# Setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate

# Run
python manage.py runserver
```

## 🎯 **Quick Fix for Your Current Issue**

If you're on Linux and getting `python` command not found:

### **Option 1: Use python3**
```bash
python3 setup.py
```

### **Option 2: Create python alias (temporary)**
```bash
alias python=python3
python setup.py
```

### **Option 3: Install python-is-python3 (Ubuntu/Debian)**
```bash
sudo apt install python-is-python3
python setup.py
```

### **Option 4: Use our cross-platform launcher**
```bash
chmod +x start.sh
./start.sh
```

## 🚀 **Recommended Approach**

1. **Use the improved setup.py** - it auto-detects the right Python
2. **Use generated run scripts** - platform-specific and reliable
3. **Check Python version first**: `python3 --version` or `python --version`

The new setup script will handle all these conflicts automatically! 🎉
