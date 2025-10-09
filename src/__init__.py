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

# Import core modules with fallback - WITHOUT 'src.' prefix
try:
    core = import_with_fallback('core', 'core_pure_python')
    parser = import_with_fallback('parser', 'parser_pure_python') 
    calculator = import_with_fallback('calculator', 'calculator_pure_python')
    
    __all__ = ['core', 'parser', 'calculator']
    
except Exception as e:
    print(f"Module import failed: {e}")
    sys.exit(1)
