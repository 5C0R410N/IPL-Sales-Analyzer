#!/bin/bash

echo "IPL Sales Analyzer - Installation"
echo "=================================="

# Check if running in Termux
if [ -d "/data/data/com.termux/files/usr" ]; then
    echo "Termux environment detected"
    
    # Request storage permission
    echo "Requesting storage permissions..."
    termux-setup-storage
    sleep 2
    
    # Update packages
    echo "Updating Termux packages..."
    pkg update -y && pkg upgrade -y
    
    # Install required packages - ALL IN ONE COMMAND
    echo "Installing required packages..."
    pkg install -y python python-pip git poppler pdftk

else
    echo "Standard Linux environment detected"
    # Install system dependencies for Linux
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv pdftk poppler-utils
fi

# Verify critical commands
echo "Verifying installation..."
for cmd in python pip pdftotext pdftk; do
    if command -v $cmd &> /dev/null; then
        echo "✅ $cmd is available"
    else
        echo "❌ $cmd is NOT available"
    fi
done

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Build Cython extensions
echo "Building Cython extensions..."
cd src
python build_cython.py
cd ..

# Setup directories and bashrc alias
echo "Setting up directories and command alias..."
python setup_directories.py

# Make scripts executable
chmod +x install.sh
chmod +x uninstall.sh

# Verify bashrc setup
echo "Verifying command alias setup..."
if grep -q "alias report=" ~/.bashrc 2>/dev/null || grep -q "alias report=" /data/data/com.termux/files/usr/etc/bash.bashrc 2>/dev/null; then
    echo "Command 'report' alias installed successfully"
    echo "You can now type 'report' from anywhere to start the analyzer"
else
    echo "Could not set up command alias automatically"
    echo "You can manually run: python src/ipl_analyzer.py"
fi

echo ""
echo "Installation completed successfully!"
echo ""
echo "Usage:"
echo "1. Place PDF files in /storage/emulated/0/SalesSource/"
echo "2. Run: report (from anywhere in Termux)"
echo "3. Or run: python src/ipl_analyzer.py"
echo ""
echo "The 'report' command works in any case: report/Report/REPORT"
echo ""
echo "Repository: https://github.com/5C0R410N/IPL-Sales-Analyzer"
