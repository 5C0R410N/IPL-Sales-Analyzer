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

    # Install required packages - USING TUR-REPO METHOD
    echo "📦 Installing required packages..."
    pkg install -y python git poppler pdftk openjdk-17
    
    # Install numpy first (available in main repo)
    echo "📦 Installing numpy..."
    pkg install -y python-numpy
    
    # Install tur-repo for pandas
    echo "📦 Installing tur-repo..."
    pkg install -y tur-repo
    
    # Install pandas from tur-repo
    echo "📦 Installing pandas from tur-repo..."
    pkg install -y python-pandas
    
    # Install remaining Python packages via pip
    echo "📦 Installing remaining Python dependencies..."
    pip install --upgrade pip
    pip install Cython>=0.29.0 pytz>=2021.3 colorama>=0.4.4 tabula-py>=2.8.0 jpype1>=1.4.0 python-dateutil>=2.8.2 tzdata

else
    echo "🐧 Standard Linux environment detected"
    # Install system dependencies for Linux
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv pdftk poppler-utils default-jdk
    pip install -r requirements.txt
fi

# Verify critical commands
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

# Test Python installation
echo "🧪 Testing Python installation..."
python -c "import pandas; print(f'✅ Pandas {pandas.__version__} working')"
python -c "import numpy; print(f'✅ NumPy {numpy.__version__} working')"
python -c "import tabula; import jpype; print('✅ Tabula and JPype1 working!')"

if [ $? -eq 0 ]; then
    echo "✅ All dependencies installed successfully"
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
