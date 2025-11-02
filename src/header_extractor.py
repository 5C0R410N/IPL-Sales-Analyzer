#!/usr/bin/env python3
"""
IPL Sales Analyzer - Header Extractor for Cut PDFs
Works on the extracted small PDF (pages 339-345)
"""

import os
import sys
import subprocess
import tempfile
import re
import json
from datetime import datetime
from pathlib import Path

def extract_header_from_cut_pdf(cut_pdf_path):
    """
    Extract header information from CUT PDF (small extracted file)
    This is called AFTER pdftk creates the cut PDF
    """
    header_data = {
        "pdf_file": os.path.basename(cut_pdf_path),
        "extraction_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "report_type": "Territory Wise Sale",
        "period_from": "Unknown",
        "period_to": "Unknown", 
        "printed_on": "Unknown",
        "group": "Unknown",
        "territory_id": "Unknown_Territory",
    }
    
    print(f"🔍 Extracting header from cut PDF: {os.path.basename(cut_pdf_path)}")
    
    try:
        # Create temp text file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            temp_text_file = f.name
        
        # Extract text from FIRST PAGE of cut PDF only (fast)
        cmd = f'pdftotext -l 1 "{cut_pdf_path}" "{temp_text_file}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(temp_text_file):
            with open(temp_text_file, 'r', encoding='utf-8', errors='ignore') as f:
                raw_text = f.read()
            
            print(f"📄 Extracted {len(raw_text)} characters from cut PDF header")
            
            # Split into lines for better parsing
            lines = raw_text.split('\n')
            
            # DEBUG: Show first 10 lines to see structure
            print("📋 First 10 lines of cut PDF:")
            for i, line in enumerate(lines[:10]):
                print(f"   {i+1}: {line}")
            
            # EXTRACT TERRITORY - Handle line breaks
            territory_found = False
            for i, line in enumerate(lines):
                line_clean = line.strip()
                
                # Look for "Terr Id:" pattern
                if 'Terr Id:' in line_clean:
                    # Try to extract from current line
                    terr_match = re.search(r'Terr Id:\s*([A-Z]{2,3}-\d{2})', line_clean)
                    if terr_match:
                        header_data["territory_id"] = terr_match.group(1)
                        territory_found = True
                        print(f"✅ Found territory in same line: {terr_match.group(1)}")
                        break
                    else:
                        # Check next line for territory (like "XO-24")
                        if i + 1 < len(lines):
                            next_line = lines[i + 1].strip()
                            if re.match(r'^[A-Z]{2,3}-\d{2}$', next_line):
                                header_data["territory_id"] = next_line
                                territory_found = True
                                print(f"✅ Found territory on next line: {next_line}")
                                break
            
            # EXTRACT DATE RANGE
            for i, line in enumerate(lines):
                if 'From :' in line:
                    # Extract "From" date
                    from_match = re.search(r'From :\s*(\d{2}-[A-Z]{3}-\d{2})', line)
                    if from_match:
                        header_data["period_from"] = from_match.group(1)
                    
                    # Extract "To" date - check current line and next line
                    to_match = re.search(r'To\s+(\d{2}-[A-Z]{3}-\d{2})', line)
                    if to_match:
                        header_data["period_to"] = to_match.group(1)
                    elif i + 1 < len(lines):
                        next_line = lines[i + 1]
                        to_match = re.search(r'To\s+(\d{2}-[A-Z]{3}-\d{2})', next_line)
                        if to_match:
                            header_data["period_to"] = to_match.group(1)
                    break
            
            # EXTRACT GROUP
            for i, line in enumerate(lines):
                if 'Group:' in line:
                    group_match = re.search(r'Group:\s*([A-Z\-]+)', line)
                    if group_match:
                        header_data["group"] = group_match.group(1)
                    # Check if group name is on next line
                    if i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        if next_line and not re.match(r'^[A-Z]{2,3}-\d{2}$', next_line):
                            header_data["group"] = next_line
                    break
            
            # EXTRACT PRINTED DATE
            for line in lines:
                if 'Printed On:' in line:
                    printed_match = re.search(r'Printed On:\s*([\d\-A-Z:\s]+(?:AM|PM))', line)
                    if printed_match:
                        header_data["printed_on"] = printed_match.group(1).strip()
                    break
            
            # Cleanup temp file
            os.remove(temp_text_file)
            
            print("🎯 HEADER EXTRACTION RESULTS:")
            print(f"   📍 Territory: {header_data['territory_id']}")
            print(f"   👥 Group: {header_data['group']}")
            print(f"   📅 Period: {header_data['period_from']} to {header_data['period_to']}")
            print(f"   🖨️  Printed: {header_data['printed_on']}")
            
        else:
            print("❌ Failed to extract text from cut PDF")
            
    except Exception as e:
        print(f"❌ Header extraction error: {e}")
    
    return header_data

def save_header_to_json(header_data, json_path):
    """Save header data to JSON file"""
    try:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(header_data, f, indent=2, ensure_ascii=False)
        print(f"💾 Header data saved to: {json_path}")
        return True
    except Exception as e:
        print(f"❌ Error saving JSON: {e}")
        return False

def load_header_from_json(json_path):
    """Load header data from JSON file"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading JSON: {e}")
        return None

# Test function
def test_header_extraction():
    """Test header extraction on a cut PDF"""
    # Test with your actual cut PDF file
    cut_pdf_path = "/storage/emulated/0/SalesSource/temp_extracted_pages_339_to_345.pdf"
    
    if os.path.exists(cut_pdf_path):
        print("🧪 TESTING HEADER EXTRACTION ON CUT PDF")
        header_data = extract_header_from_cut_pdf(cut_pdf_path)
        
        # Save to JSON for debugging
        save_header_to_json(header_data, "test_header_cut_pdf.json")
        
        return header_data
    else:
        print("❌ Cut PDF not found - run the main analyzer first to create it")
        return None

if __name__ == "__main__":
    test_header_extraction()
