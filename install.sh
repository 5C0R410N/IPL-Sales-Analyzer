#!/bin/bash

echo "IPL Sales Analyzer - Installation"
echo "=================================="

# Check if running in Termux
if [ -d "/data/data/com.termux/files/usr" ]; then
    echo "Termux environment detected"
    
    # Request storage permission
    echo "Requesting storage permissions..."
    termux-setup-storage
    
    # Update packages
    echo "Updating Termux packages..."
    pkg update -y
    pkg upgrade -y
    
    # Install required packages - ONLY what you actually use
    echo "Installing required packages..."
    pkg install -y python python-pip git
    
    # Check if pdftotext and pdftk are available
    if ! command -v pdftotext &> /dev/null; then
        echo "❌ pdftotext not found. Please install it manually:"
        echo "   pkg install poppler"
        exit 1
    fi
    
    if ! command -v pdftk &> /dev/null; then
        echo "❌ pdftk not found. Please install it manually:" 
        echo "   pkg install pdftk"
        exit 1
    fi

else
    echo "Standard Linux environment detected"
    # Install system dependencies for Linux
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv pdftk poppler-utils
fi

# Create necessary directories
echo "Creating directories..."
mkdir -p /storage/emulated/0/SalesSource
mkdir -p /storage/emulated/0/Analytics_Reports

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
