#!/usr/bin/env python3
"""
DEBUG: Check what's actually in the PDF header
"""

import os
import subprocess
import tempfile
import re

def debug_pdf_header(pdf_path):
    """Debug function to see raw PDF header content"""
    print("🔍 DEBUG: Checking PDF header content...")
    
    try:
        # Create temp text file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            temp_text_file = f.name
        
        # Extract text from first 3 pages
        cmd = f'pdftotext -l 3 "{pdf_path}" "{temp_text_file}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(temp_text_file):
            with open(temp_text_file, 'r', encoding='utf-8', errors='ignore') as f:
                raw_text = f.read()
            
            print("📄 RAW HEADER TEXT (first 1000 characters):")
            print("=" * 50)
            print(raw_text[:1000])
            print("=" * 50)
            
            # Look for territory patterns
            print("\n🔍 Looking for territory patterns...")
            territory_patterns = [
                r'Terr\s*Id\s*:\s*([A-Z0-9\-]+)',
                r'Territory\s*Id\s*:\s*([A-Z0-9\-]+)',
                r'([A-Z]{2,3}-\d{2,3})',
            ]
            
            for i, pattern in enumerate(territory_patterns):
                matches = re.findall(pattern, raw_text, re.IGNORECASE)
                if matches:
                    print(f"✅ Pattern {i+1} found: {matches}")
                else:
                    print(f"❌ Pattern {i+1} not found")
            
            # Cleanup
            os.remove(temp_text_file)
        else:
            print("❌ Failed to extract text")
            
    except Exception as e:
        print(f"❌ Error: {e}")

# Test with your PDF
pdf_path = "/storage/emulated/0/SalesSource/original_full_report.pdf"
if os.path.exists(pdf_path):
    debug_pdf_header(pdf_path)
else:
    print("❌ PDF not found")
