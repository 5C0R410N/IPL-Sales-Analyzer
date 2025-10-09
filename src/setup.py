from setuptools import setup, Extension
import sys

# Check if Cython is available
try:
    from Cython.Build import cythonize
    CYTHON_AVAILABLE = True
except ImportError:
    CYTHON_AVAILABLE = False
    print("Cython not available - Using Python fallback")

# Define Cython extensions if available
extensions = []
if CYTHON_AVAILABLE:
    extensions = cythonize([
        Extension("core", ["core.pyx"]),
        Extension("parser", ["parser.pyx"]), 
        Extension("calculator", ["calculator.pyx"])
    ], compiler_directives={
        'language_level': 3,
        'boundscheck': False,
        'wraparound': False,
        'initializedcheck': False,
        'cdivision': True
    })

setup(
    name="ipl-sales-analyzer",
    ext_modules=extensions,
    zip_safe=False,
)
