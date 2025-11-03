#!/bin/bash

echo "🔧 IPL Sales Analyzer - Complete Installation"
echo "============================================="

# Check if running in Termux
if [ -d "/data/data/com.termux/files/usr" ]; then
    echo "📱 Termux environment detected"

    # Request storage permission
    echo "📁 Requesting storage permissions..."
    termux-setup-storage
    sleep 2

    # Update packages
    echo "🔄 Updating Termux packages..."
    pkg update -y && pkg upgrade -y

    # Install required packages - OPTIMIZED FOR YOUR ENVIRONMENT
    echo "📦 Installing required packages..."
    pkg install -y python python-pip git poppler pdftk openjdk-17

else
    echo "🐧 Standard Linux environment detected"
    # Install system dependencies for Linux
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv pdftk poppler-utils default-jdk
fi

# Verify critical commands - ENHANCED VERIFICATION
echo "🔍 Verifying installation..."
for cmd in python pip java; do
    if command -v $cmd &> /dev/null; then
        echo "✅ $cmd is available"
    else
        echo "❌ $cmd is NOT available"
    fi
done

# Verify Java version specifically
echo "☕ Checking Java version..."
java -version
if [ $? -eq 0 ]; then
    echo "✅ Java is working correctly"
else
    echo "❌ Java installation failed"
    exit 1
fi

# Install Python dependencies - OPTIMIZED BASED ON YOUR NUMPY CONFIG
echo "🐍 Installing Python dependencies..."
pip install --upgrade pip

# Get Python version dynamically
PYTHON_VERSION=$(python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "🐍 Detected Python version: $PYTHON_VERSION"

# Install with optimized flags for Termux - BASED ON YOUR ACTUAL CONFIG
if [ -d "/data/data/com.termux/files/usr" ]; then
    echo "🚀 Using Termux-optimized installation..."
    
    # Install EXACT build dependencies from your numpy config
    echo "📦 Installing build dependencies..."
    pkg install -y python build-essential libopenblas cmake patchelf binutils-is-llvm
    
    # Install Python build tools that your numpy actually uses
    echo "📦 Installing Python build tools..."
    pip install meson-python pyproject-metadata cython
    
    # SET OPTIMIZED ENVIRONMENT VARIABLES BASED ON YOUR CONFIG
    export NPY_NUM_BUILD_JOBS=4
    export CFLAGS="-fstack-protector-strong -Oz -march=armv8-a"
    export LDFLAGS="-L/data/data/com.termux/files/usr/lib -Wl,-rpath=/data/data/com.termux/files/usr/lib"
    
    # INSTALL NUMPY WITH EXACT OPTIONS FROM YOUR CONFIG
    echo "📦 Installing numpy (optimized for ARM64)..."
    MATHLIB="m" LDFLAGS="-lpython$PYTHON_VERSION -L/data/data/com.termux/files/usr/lib" \
    pip install --no-build-isolation --no-cache-dir --compile "numpy==1.24.3"
    
    # INSTALL PANDAS WITH OPTIMIZED SETTINGS
    echo "📦 Installing pandas (optimized version)..."
    LDFLAGS="-lpython$PYTHON_VERSION -L/data/data/com.termux/files/usr/lib" \
    pip install --no-build-isolation --no-cache-dir --compile "pandas==1.5.3"
    
    # Install remaining requirements
    echo "📦 Installing other dependencies..."
    pip install Cython>=0.29.0 pytz>=2021.3 colorama>=0.4.4 tabula-py>=2.8.0 jpype1>=1.4.0 python-dateutil>=2.8.2
    
else
    # Standard installation for Linux
    echo "📦 Installing latest package versions..."
    pip install -r requirements.txt
fi

# Test Tabula installation
echo "🧪 Testing Tabula installation..."
python -c "import tabula; import jpype; import pandas; print('✅ All dependencies working!')"
if [ $? -eq 0 ]; then
    echo "✅ Tabula and pandas installation successful"
else
    echo "❌ Installation failed - checking dependencies..."
    pip list | grep -E "(tabula|jpype|pandas|numpy)"
    exit 1
fi

# Setup directories and bashrc alias
echo "📁 Setting up directories and command alias..."
python setup_directories.py

# Make scripts executable
chmod +x install.sh
chmod +x uninstall.sh
chmod +x src/ipl_analyzer.py

# Verify bashrc setup
echo "🔗 Verifying command alias setup..."
if grep -q "alias report=" ~/.bashrc 2>/dev/null || grep -q "alias report=" /data/data/com.termux/files/usr/etc/bash.bashrc 2>/dev/null; then
    echo "✅ Command 'report' alias installed successfully"
    echo "💡 You can now type 'report' from anywhere to start the analyzer"
else
    echo "⚠️ Could not set up command alias automatically"
    echo "💡 You can manually run: python src/ipl_analyzer.py"
fi

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "🚀 Features:"
echo "   • 100% Accurate Tabula PDF Parser"
echo "   • Automatic PDF import from Downloads"
echo "   • Territory detection and analysis"
echo "   • National average calculations"
echo ""
echo "📁 Usage:"
echo "1. Place PDF files in /storage/emulated/0/SalesSource/"
echo "2. Run: report (from anywhere in Termux)"
echo "3. Or run: python src/ipl_analyzer.py"
echo ""
echo "🔗 Repository: https://github.com/5C0R410N/IPL-Sales-Analyzer"
echo ""
echo "💡 The 'report' command works in any case: report/Report/REPORT"
