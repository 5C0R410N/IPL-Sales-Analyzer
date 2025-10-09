#!/usr/bin/env python3
"""
IPL Sales Analyzer - Smart Cython Builder
Automatically builds Cython extensions or uses Python fallback
"""

import os
import sys
import subprocess
import importlib.util
from pathlib import Path

def check_cython_availability():
    """Check if Cython is available and working"""
    try:
        import Cython
        print("Cython is available")
        return True
    except ImportError:
        print("Cython not available")
        return False

def build_cython_extensions():
    """Attempt to build Cython extensions"""
    try:
        print("Building Cython extensions...")
        result = subprocess.run([
            sys.executable, "setup.py", "build_ext", "--inplace"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Cython extensions built successfully")
            return True
        else:
            print(f"Cython build failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"Cython build error: {e}")
        return False

def check_built_extensions():
    """Check if Cython extensions are available"""
    extensions = ['core', 'parser', 'calculator']
    available = True
    
    for ext in extensions:
        try:
            spec = importlib.util.find_spec(f"src.{ext}")
            if spec is None:
                available = False
                print(f"Extension {ext} not found")
        except:
            available = False
            print(f"Extension {ext} failed to load")
    
    return available

def setup_fallback_system():
    """Setup the fallback system to use pure Python if Cython fails"""
    print("Setting up fallback system...")
    
    # Create __init__.py if it doesn't exist
    init_file = Path("__init__.py")
    if not init_file.exists():
        init_file.write_text('''
"""
IPL Sales Analyzer - Smart Module Loader
"""
import sys
import importlib

def import_with_fallback(cython_name, python_name):
    """
    Import Cython module if available, otherwise use pure Python fallback
    """
    try:
        cython_module = importlib.import_module(cython_name)
        print(f"Using Cython optimized: {cython_name}")
        return cython_module
    except ImportError:
        python_module = importlib.import_module(python_name)
        print(f"Using Python fallback: {python_name}")
        return python_module

try:
    core = import_with_fallback('core', 'core_pure_python')
    parser = import_with_fallback('parser', 'parser_pure_python') 
    calculator = import_with_fallback('calculator', 'calculator_pure_python')
    
    __all__ = ['core', 'parser', 'calculator']
    
except Exception as e:
    print(f"Module import failed: {e}")
    sys.exit(1)
''')

def main():
    """Main build process"""
    print("IPL Sales Analyzer - Build System")
    print("=" * 40)
    
    # Step 1: Check Cython availability
    cython_available = check_cython_availability()
    
    # Step 2: Build Cython extensions if available
    cython_built = False
    if cython_available:
        cython_built = build_cython_extensions()
    
    # Step 3: Check if extensions are usable
    extensions_ready = check_built_extensions() if cython_built else False
    
    # Step 4: Setup fallback system
    setup_fallback_system()
    
    # Final status
    print("=" * 40)
    if extensions_ready:
        print("Cython optimization: ENABLED")
    else:
        print("Cython optimization: DISABLED")
    print("Build process completed")
    
    return extensions_ready

if __name__ == "__main__":
    main()
