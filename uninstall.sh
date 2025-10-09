#!/bin/bash

echo "IPL Sales Analyzer - Uninstallation"
echo "===================================="

# Remove all case variations of alias from bashrc files
echo "Removing command aliases..."
sed -i '/alias report=/d' /data/data/com.termux/files/usr/etc/bash.bashrc 2>/dev/null
sed -i '/alias Report=/d' /data/data/com.termux/files/usr/etc/bash.bashrc 2>/dev/null
sed -i '/alias REPORT=/d' /data/data/com.termux/files/usr/etc/bash.bashrc 2>/dev/null

sed -i '/alias report=/d' ~/.bashrc 2>/dev/null
sed -i '/alias Report=/d' ~/.bashrc 2>/dev/null  
sed -i '/alias REPORT=/d' ~/.bashrc 2>/dev/null

sed -i '/alias report=/d' ~/.bash_profile 2>/dev/null
sed -i '/alias Report=/d' ~/.bash_profile 2>/dev/null
sed -i '/alias REPORT=/d' ~/.bash_profile 2>/dev/null

# Remove compiled Cython files
echo "Removing compiled files..."
find src -name "*.so" -delete
find src -name "*.c" -delete
find src -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null

# Remove build directory
echo "Removing build directory..."
rm -rf src/build 2>/dev/null

echo ""
echo "Uninstallation completed!"
echo "All 'report' command variations have been removed"
echo "Note: User data and report directories were not removed"
echo "To completely remove, delete the IPL-Sales-Analyzer folder"
echo ""
echo "Repository: https://github.com/5C0R410N/IPL-Sales-Analyzer"
